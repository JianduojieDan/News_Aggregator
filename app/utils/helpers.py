import os
from datetime import datetime
import requests
import feedparser
from bs4 import BeautifulSoup
import logging
from flask import render_template, current_app
from flask_login import current_user

logger = logging.getLogger(__name__)


def get_news_from_sources():
    """从数据库中的所有源获取新闻并保存到文章表。
    返回添加的新文章数量。"""
    from app import db
    from app.models.models import Source, Article

    sources = Source.query.all()
    new_articles_count = 0

    for source in sources:
        try:
            # 检查源URL是否为RSS源
            if source.url.endswith('.xml') or 'rss' in source.url or 'feed' in source.url:
                new_count = _parse_rss_feed(source)
            else:
                new_count = _scrape_website(source)

            new_articles_count += new_count
            logger.info(f"Added {new_count} new articles from {source.name}")
        except Exception as e:
            logger.error(f"Error fetching news from {source.name}: {str(e)}")
            continue

    return new_articles_count


def _parse_rss_feed(source):
    """解析RSS源并将文章保存到数据库。
    返回添加的新文章数量。"""
    from app import db
    from app.models.models import Article

    feed = feedparser.parse(source.url)
    new_count = 0

    for entry in feed.entries[:20]:  # 限制为20篇最新文章
        # 检查文章是否已存在
        existing = Article.query.filter_by(url=entry.link).first()
        if existing:
            continue

        # 解析发布日期
        if hasattr(entry, 'published_parsed'):
            published_at = datetime(*entry.published_parsed[:6])
        else:
            published_at = datetime.utcnow()

        # 获取图片URL（如果有）
        image_url = None
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if 'url' in media:
                    image_url = media['url']
                    break
        elif hasattr(entry, 'links'):
            for link in entry.links:
                if link.get('type', '').startswith('image/'):
                    image_url = link.get('href')
                    break

        # 提取内容
        content = entry.get('summary', '')
        if hasattr(entry, 'content'):
            for content_item in entry.content:
                if content_item.get('type') == 'text/html':
                    content = content_item.value
                    break

        # 创建新文章
        article = Article(
            title=entry.title,
            content=content,
            url=entry.link,
            published_at=published_at,
            image_url=image_url,
            source_id=source.id
        )

        db.session.add(article)
        new_count += 1

    db.session.commit()
    return new_count


def _scrape_website(source):
    """抓取网站获取新闻文章。
    返回添加的新文章数量。"""
    from app import db
    from app.models.models import Article

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    response = requests.get(source.url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    new_count = 0

    # 查找文章元素 - 这是一个简单的实现
    # 实际应用中需要针对每个网站定制
    articles = soup.find_all('article') or soup.find_all('div', class_=['article', 'post', 'news-item'])

    if not articles:
        # 尝试查找可能是文章的链接
        articles = soup.find_all('a', href=True)

    processed_urls = set()

    for article_elem in articles[:20]:  # 限制为20篇文章
        # 尝试提取文章URL
        url = None
        if article_elem.name == 'a' and article_elem.has_attr('href'):
            url = article_elem['href']
        else:
            link = article_elem.find('a', href=True)
            if link:
                url = link['href']

        if not url:
            continue

        # 如果URL是相对路径，转换为绝对URL
        if not url.startswith(('http://', 'https://')):
            if url.startswith('/'):
                base_url = '/'.join(source.url.split('/')[:3])  # http(s) ://domain.com
                url = base_url + url
            else:
                url = source.url.rstrip('/') + '/' + url

        # 如果已处理过此URL或不是来自同一域名，则跳过
        source_domain = source.url.split('/')[2]
        if url in processed_urls or source_domain not in url:
            continue

        processed_urls.add(url)

        # 检查数据库中是否已存在此文章
        existing = Article.query.filter_by(url=url).first()
        if existing:
            continue

        # 尝试提取标题和图片
        title = None
        image_url = None

        # 查找标题
        title_elem = article_elem.find(['h1', 'h2', 'h3'])
        if title_elem:
            title = title_elem.get_text().strip()
        elif article_elem.has_attr('title'):
            title = article_elem['title']

        # 查找图片
        img = article_elem.find('img', src=True)
        if img and img.has_attr('src'):
            image_url = img['src']
            # 如果图片URL是相对路径，转换为绝对URL
            if not image_url.startswith(('http://', 'https://')):
                if image_url.startswith('/'):
                    base_url = '/'.join(source.url.split('/')[:3])
                    image_url = base_url + image_url
                else:
                    image_url = source.url.rstrip('/') + '/' + image_url

        # 如果无法提取标题，则跳过
        if not title:
            continue

        # 创建新文章
        article = Article(
            title=title,
            content='',  # 需要获取实际文章页面才能获取内容
            url=url,
            published_at=datetime.utcnow(),  # 我们不知道实际发布日期
            image_url=image_url,
            source_id=source.id
        )

        db.session.add(article)
        new_count += 1

    db.session.commit()
    return new_count


def get_user_recommendations(user_id, limit=10):
    """基于用户收藏获取文章推荐。"""
    from app.models.models import Article, Favorite

    # 获取用户收藏的文章
    user_favorites = Favorite.query.filter_by(user_id=user_id).all()

    if not user_favorites:
        # 如果用户没有收藏，返回最新文章
        return Article.query.order_by(Article.published_at.desc()).limit(limit).all()

    # 从用户收藏中获取源ID
    favorite_source_ids = set()
    for favorite in user_favorites:
        article = Article.query.get(favorite.article_id)
        if article:
            favorite_source_ids.add(article.source_id)

    # 获取这些源的最新文章，排除已收藏的文章
    favorited_article_ids = [f.article_id for f in user_favorites]

    recommended_articles = Article.query.filter(
        Article.source_id.in_(favorite_source_ids),
        ~Article.id.in_(favorited_article_ids)
    ).order_by(Article.published_at.desc()).limit(limit).all()

    # 如果推荐不足，添加一些最新文章
    if len(recommended_articles) < limit:
        additional_count = limit - len(recommended_articles)
        existing_ids = [a.id for a in recommended_articles] + favorited_article_ids

        additional_articles = Article.query.filter(
            ~Article.id.in_(existing_ids)
        ).order_by(Article.published_at.desc()).limit(additional_count).all()

        recommended_articles.extend(additional_articles)

    return recommended_articles


def format_datetime(value, format='medium'):
    """将datetime对象格式化为字符串。"""
    if format == 'full':
        format = '%A, %B %d, %Y at %I:%M %p'
    elif format == 'medium':
        format = '%b %d, %Y at %I:%M %p'
    elif format == 'short':
        format = '%m/%d/%y %I:%M %p'
    elif format == 'date_only':
        format = '%b %d, %Y'
    return value.strftime(format)


def get_domain_from_url(url):
    """从URL中提取域名。"""
    if not url:
        return ''
    try:
        return url.split('/')[2]
    except:
        return url


def register_error_handlers(app):
    """为Flask应用注册错误处理器。"""

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('news/error.html',
                               error_title='Page Not Found',
                               error_message='The page you requested could not be found.',
                               error_description='Please check the URL or return to the home page.'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('news/error.html',
                               error_title='Server Error',
                               error_message='An internal server error occurred.',
                               error_description='Our team has been notified. Please try again later.'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('news/error.html',
                               error_title='Access Denied',
                               error_message='You do not have permission to access this resource.',
                               error_description='Please log in or contact the administrator if you believe this is an error.'), 403


def register_template_filters(app):
    """为Flask应用注册自定义模板过滤器。"""

    @app.template_filter('format_date')
    def format_date_filter(value, format='medium'):
        return format_datetime(value, format)

    @app.template_filter('truncate_text')
    def truncate_text(text, length=100):
        """将文本截断到指定长度。"""
        if not text:
            return ''

        if len(text) <= length:
            return text

        return text[:length].rsplit(' ', 1)[0] + '...'

    @app.template_filter('domain_from_url')
    def domain_from_url_filter(url):
        return get_domain_from_url(url)


def register_context_processors(app):
    """为Flask应用注册上下文处理器。"""

    @app.context_processor
    def inject_globals():
        """注入全局变量到模板。"""
        return {
            'current_year': datetime.now().year,
            'app_name': 'News Aggregator',
            'app_version': '1.0.0'
        }

    @app.context_processor
    def inject_user_favorites():
        """注入用户收藏到模板。"""
        favorites = []
        if current_user.is_authenticated:
            from app.models.models import Favorite
            favorites = [f.article_id for f in Favorite.query.filter_by(user_id=current_user.id).all()]
        return {'user_favorites': favorites}
