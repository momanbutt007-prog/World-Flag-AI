from flask import (
    Blueprint,
    current_app,
    jsonify,
    render_template,
    request,
)


routes = Blueprint(
    "routes",
    __name__,
)


@routes.route("/")
def home():

    return render_template(
        "index.html"
    )


@routes.route(
    "/api/predict",
    methods=["POST"],
)
def predict():

    if "image" not in request.files:

        return jsonify(
            {
                "success": False,
                "error": "No image uploaded.",
            }
        ), 400

    image_file = request.files["image"]

    if not image_file.filename:

        return jsonify(
            {
                "success": False,
                "error": "No image selected.",
            }
        ), 400

    try:

        results = current_app.predictor.predict(
            image_file
        )

        return jsonify(
            {
                "success": True,
                "results": results,
            }
        )

    except Exception as error:

        return jsonify(
            {
                "success": False,
                "error": str(error),
            }
        ), 500