from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app.models.models import Article, Source, Favorite, Preference
from app import db
from app.utils.helpers import get_news_from_sources, get_user_recommendations
import datetime

news = Blueprint('news', __name__)


@news.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ARTICLES_PER_PAGE']

    articles = Article.query.order_by(Article.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('news/index.html', title='Latest News',
                           articles=articles.items,
                           pagination=articles)


@news.route('/sources')
def sources():
    sources = Source.query.all()
    return render_template('news/sources.html', title='News Sources', sources=sources)


@news.route('/source/<int:id>')
def source_articles(id):
    source = Source.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ARTICLES_PER_PAGE']

    articles = Article.query.filter_by(source_id=id).order_by(
        Article.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('news/source_articles.html',
                           title=f'News from {source.name}',
                           source=source,
                           articles=articles.items,
                           pagination=articles)


@news.route('/article/<int:id>')
def article_detail(id):
    article = Article.query.get_or_404(id)
    return render_template('news/article_detail.html', title=article.title, article=article)


@news.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('news.index'))

    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ARTICLES_PER_PAGE']

    articles = Article.query.filter(
        Article.title.contains(query) | Article.content.contains(query)
    ).order_by(Article.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('news/search_results.html',
                           title=f'Search Results for "{query}"',
                           query=query,
                           articles=articles.items,
                           pagination=articles)


@news.route('/refresh_news')
@login_required
def refresh_news():
    try:
        count = get_news_from_sources()
        flash(f'Successfully fetched {count} new articles', 'success')
    except Exception as e:
        flash(f'Error refreshing news: {str(e)}', 'danger')

    return redirect(url_for('news.index'))


@news.route('/favorite/<int:article_id>', methods=['POST'])
@login_required
def favorite_article(article_id):
    article = Article.query.get_or_404(article_id)

    # 检查是否已收藏
    existing_favorite = Favorite.query.filter_by(
        user_id=current_user.id, article_id=article_id).first()

    if existing_favorite:
        db.session.delete(existing_favorite)
        db.session.commit()
        return jsonify({'status': 'removed'})
    else:
        favorite = Favorite(user_id=current_user.id, article_id=article_id)
        db.session.add(favorite)
        db.session.commit()
        return jsonify({'status': 'added'})


@news.route('/favorites')
@login_required
def favorites():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ARTICLES_PER_PAGE']

    favorites = Favorite.query.filter_by(user_id=current_user.id).order_by(
        Favorite.created_at.desc())

    article_ids = [f.article_id for f in favorites]

    articles = Article.query.filter(Article.id.in_(article_ids)).order_by(
        Article.published_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False)

    return render_template('news/favorites.html',
                           title='My Favorites',
                           articles=articles.items,
                           pagination=articles)


@news.route('/recommendations')
@login_required
def recommendations():
    recommended_articles = get_user_recommendations(current_user.id, limit=12)

    return render_template('news/recommendations.html',
                           title='Recommended For You',
                           articles=recommended_articles)


@news.route('/preferences', methods=['GET', 'POST'])
@login_required
def preferences():
    if request.method == 'POST':
        # 清除现有偏好
        Preference.query.filter_by(user_id=current_user.id).delete()

        # 从表单获取选定的源
        selected_sources = request.form.getlist('sources')

        # 添加新偏好
        for source_id in selected_sources:
            preference = Preference(user_id=current_user.id, source_id=int(source_id))
            db.session.add(preference)

        db.session.commit()
        flash('Your preferences have been updated.', 'success')
        return redirect(url_for('news.index'))

    # 获取所有源和用户当前偏好
    sources = Source.query.all()
    user_preferences = [p.source_id for p in Preference.query.filter_by(user_id=current_user.id).all()]

    return render_template('news/preferences.html',
                           title='News Preferences',
                           sources=sources,
                           user_preferences=user_preferences)
