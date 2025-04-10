import unittest
from app import create_app, db
from app.models.models import User, Source, Article, Favorite, Preference
from werkzeug.security import generate_password_hash
import datetime


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

        # 创建测试数据
        self._create_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def _create_test_data(self):
        # 创建测试用户
        user = User(username='testuser', email='test@example.com')
        user.password_hash = generate_password_hash('password')
        db.session.add(user)

        # 创建测试源
        source1 = Source(name='Test Source 1',
                         url='http://example.com/feed1.xml',
                         description='Test source 1 description',
                         logo_url='http://example.com/logo1.png')

        source2 = Source(name='Test Source 2',
                         url='http://example.com/feed2.xml',
                         description='Test source 2 description',
                         logo_url='http://example.com/logo2.png')

        db.session.add_all([source1, source2])
        db.session.commit()

        # 创建测试文章
        article1 = Article(title='Test Article 1',
                           content='Test content 1',
                           url='http://example.com/article1',
                           published_at=datetime.datetime.utcnow(),
                           image_url='http://example.com/image1.jpg',
                           source_id=source1.id)

        article2 = Article(title='Test Article 2',
                           content='Test content 2',
                           url='http://example.com/article2',
                           published_at=datetime.datetime.utcnow(),
                           image_url='http://example.com/image2.jpg',
                           source_id=source2.id)

        db.session.add_all([article1, article2])
        db.session.commit()

        # 创建测试收藏
        favorite = Favorite(user_id=user.id, article_id=article1.id)
        db.session.add(favorite)

        # 创建测试偏好
        preference = Preference(user_id=user.id, source_id=source1.id)
        db.session.add(preference)

        db.session.commit()


class UserModelTestCase(BaseTestCase):
    def test_password_setter(self):
        u = User(username='test', email='test@example.com')
        u.set_password('cat')
        self.assertTrue(u.password_hash is not None)

    def test_password_verification(self):
        u = User(username='test', email='test@example.com')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_is_favorite(self):
        user = User.query.filter_by(username='testuser').first()
        article = Article.query.filter_by(title='Test Article 1').first()
        self.assertTrue(user.is_favorite(article.id))

        article2 = Article.query.filter_by(title='Test Article 2').first()
        self.assertFalse(user.is_favorite(article2.id))


class AuthRoutesTestCase(BaseTestCase):
    def test_login_page(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_register_page(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_logout(self):
        # 使用正确的凭据登录
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Latest News', response.data)

        # 登出
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'You have been logged out', response.data)

    def test_login_with_wrong_password(self):
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'wrongpassword',
            'remember_me': False
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)

    def test_register_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpassword',
            'password2': 'newpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Congratulations, you are now a registered user', response.data)

        # 检查用户是否已创建
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'new@example.com')


class NewsRoutesTestCase(BaseTestCase):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Latest News', response.data)
        self.assertIn(b'Test Article 1', response.data)
        self.assertIn(b'Test Article 2', response.data)

    def test_sources_page(self):
        response = self.client.get('/sources')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'News Sources', response.data)
        self.assertIn(b'Test Source 1', response.data)
        self.assertIn(b'Test Source 2', response.data)

    def test_source_articles_page(self):
        source = Source.query.filter_by(name='Test Source 1').first()
        response = self.client.get(f'/source/{source.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Source 1', response.data)
        self.assertIn(b'Test Article 1', response.data)

    def test_article_detail_page(self):
        article = Article.query.filter_by(title='Test Article 1').first()
        response = self.client.get(f'/article/{article.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Article 1', response.data)
        self.assertIn(b'Test content 1', response.data)

    def test_search_functionality(self):
        response = self.client.get('/search?q=Test')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Search Results', response.data)
        self.assertIn(b'Test Article 1', response.data)
        self.assertIn(b'Test Article 2', response.data)

        response = self.client.get('/search?q=nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No articles found', response.data)

    def test_favorites_page_requires_login(self):
        response = self.client.get('/favorites', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please log in to access this page', response.data)

    def test_favorites_page_with_login(self):
        # 先登录
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password',
            'remember_me': False
        })

        response = self.client.get('/favorites')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'My Favorites', response.data)
        self.assertIn(b'Test Article 1', response.data)

    def test_favorite_article_functionality(self):
        # 先登录
        self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password',
            'remember_me': False
        })

        article = Article.query.filter_by(title='Test Article 2').first()

        # 添加到收藏
        response = self.client.post(f'/favorite/{article.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'added')

        # 检查是否已添加
        user = User.query.filter_by(username='testuser').first()
        self.assertTrue(user.is_favorite(article.id))

        # 从收藏中移除
        response = self.client.post(f'/favorite/{article.id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'removed')

        # 检查是否已移除
        user = User.query.filter_by(username='testuser').first()
        self.assertFalse(user.is_favorite(article.id))


if __name__ == '__main__':
    unittest.main()
