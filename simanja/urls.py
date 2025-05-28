from simanja.controllers.auth_views import auth_bp
from simanja.controllers.item_views import item_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
def item_routes(app):
    app.register_blueprint(item_bp)

