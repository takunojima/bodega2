from app import create_app, db
from app.models import User

def init_db():
    app = create_app()
    with app.app_context():
        # データベースの作成
        db.create_all()

        # マネージャーアカウントが存在しない場合は作成
        manager = User.query.filter_by(username='manager').first()
        if not manager:
            manager = User(
                username='manager',
                email='manager@example.com',
                is_manager=True
            )
            manager.set_password('manager123')  # 本番環境では強力なパスワードを使用してください
            db.session.add(manager)
            db.session.commit()
            print('マネージャーアカウントが作成されました。')
        else:
            print('マネージャーアカウントは既に存在します。')

if __name__ == '__main__':
    init_db() 