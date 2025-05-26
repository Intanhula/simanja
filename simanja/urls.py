from simanja.controllers.auth_views import auth_bp

def register_routes(app):
    app.register_blueprint(auth_bp)

