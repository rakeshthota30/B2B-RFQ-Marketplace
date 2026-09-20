from flask import Flask, redirect, url_for
from config import Config
from extensions import db
from routes.auth_routes import auth_bp
from routes.buyer_routes import buyer_bp
from routes.supplier_routes import supplier_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(buyer_bp)
    app.register_blueprint(supplier_bp)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))

    @app.errorhandler(404)
    def not_found(error):
        return "Page not found", 404

    @app.errorhandler(500)
    def server_error(error):
        return "Internal server error", 500

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
