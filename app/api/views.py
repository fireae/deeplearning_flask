"""
views.py: api views used by Flask server.
"""

__author__      = "alverto"
__copyright__   = "Copyright 2019"


from flask import jsonify, request

from skimage.io import imread
import io

from . import api

import sys
sys.path.append("..")

from model import *

@api.route("/predictlabel", methods=["POST"])
def predict():
    # result dictionary that will be returned from the view
    result = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if request.method == "POST":
        if request.files.get("image"):
            # read image as grayscale
            image_req = request.files["image"].read()
            image = imread(io.BytesIO(image_req), as_gray=True)

            # preprocess the image for model
            preprocessed_image = preprocess_image(image)

            # classify the input image generating a list of predictions
            model = current_app.config["model"]
            preds = model.predict(preprocessed_image)
            
            # add generated predictions to result
            result["predictions"] = []

            for i in range(0,10):
                pred = {"label": str(i), "probability": str(preds[0][i])}
                result["predictions"].append(pred)

            result["most_probable_label"] = str(np.argmax(preds[0]))

            # indicate that the request was a success
            result["success"] = True

    # return result dictionary as JSON response to client
    return jsonify(result)