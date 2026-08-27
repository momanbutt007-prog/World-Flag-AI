from flask import Flask

from app.predictor import WorldFlagPredictor


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="../static",
    )

    app.config["MAX_CONTENT_LENGTH"] = (
        10 * 1024 * 1024
    )

    predictor = WorldFlagPredictor()

    app.predictor = predictor

    from flask_app.routes import routes

    app.register_blueprint(routes)

    return app