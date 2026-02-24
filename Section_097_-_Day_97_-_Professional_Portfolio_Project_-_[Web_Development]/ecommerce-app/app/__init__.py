from flask import Flask, render_template
from config import Config
from app.extensions import login_manager, jwt
from app.models import User, close_db, init_db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'

    jwt.init_app(app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp
    from app.routes.product import product_bp
    from app.routes.cart import cart_bp
    from app.routes.payment import payment_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(admin_bp)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(int(user_id))

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()
        admin_email = app.config['ADMIN_EMAIL']
        admin_pass = app.config['ADMIN_PASSWORD']
        if not User.get_by_email(admin_email):
            User.create(admin_email, admin_pass, is_admin=True)
            app.logger.info('Admin user created')

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    return app