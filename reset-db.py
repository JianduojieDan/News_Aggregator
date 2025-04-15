from app import create_app, db
from app.models.models import Article, Source, Favorite, Preference

app = create_app()

with app.app_context():
    Favorite.query.delete()
    Preference.query.delete()
    Article.query.delete()
    Source.query.delete()
    db.session.commit()
    print("所有新闻和相关数据已清空 ✅")
