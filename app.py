import os
from flask import Flask
from models import db, login_manager, User 
from werkzeug.security import generate_password_hash

app = Flask(__name__)

app.config.update(
    SECRET_KEY='linkhub2026',
    SQLALCHEMY_DATABASE_URI='sqlite:///linkhub.db',
    UPLOAD_FOLDER='static/uploads/avatars',
    MAX_CONTENT_LENGTH=2 * 1024 * 1024
)

os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)


db.init_app(app)
login_manager.init_app(app)


from routes.react import like_comment_bp, reporte_bp, vote_bp
from routes.content import post_bp, home_bp, app_bp
from routes.users import dashboard_bp, admin_bp
from routes.auth import login_bp, logout_bp, profile_bp, register_bp

app.register_blueprint(like_comment_bp)
app.register_blueprint(reporte_bp)
app.register_blueprint(vote_bp)
app.register_blueprint(home_bp)
app.register_blueprint(app_bp)
app.register_blueprint(post_bp)
app.register_blueprint(dashboard_bp) 
app.register_blueprint(admin_bp)    
app.register_blueprint(register_bp)
app.register_blueprint(login_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(profile_bp)

with app.app_context():
    db.create_all()
    if not User.query.filter_by(role='admin').first():
        admin_user = User(
            username='Admin', 
            email='admin@linkhub.com', 
            password=generate_password_hash('admin123'), 
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True) 