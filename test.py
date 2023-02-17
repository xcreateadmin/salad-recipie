# This file is used to verify your http server acts as expected
# Run it with `python3 test.py``

import sys
import requests
import base64
import os
from io import BytesIO
from PIL import Image
import banana_dev as banana

TESTS = "tests"
FIXTURES = TESTS + os.sep + "fixtures"
OUTPUT = TESTS + os.sep + "output"


def b64encode_file(filename: str):
    with open(os.path.join(FIXTURES, filename), "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def output_path(filename: str):
    return os.path.join(OUTPUT, filename)


def test(name, json):
    print("Running test: " + name)
    # res = requests.post("http://localhost:8000/", json=json)
    api_key = "f35cfb9d-f410-4c00-93aa-64e459b42e58"
    model_key = "222c6e4c-25be-4103-8451-c12978c51e87"
    out = banana.run(api_key, model_key, json)
    modelOutputs = out.get("modelOutputs", None)
    print(modelOutputs)
    json = modelOutputs;
    print(json['modelOutputs'].keys())

    image_byte_string = json["modelOutputs"]

    image_encoded = image_byte_string.encode("utf-8")
    image_bytes = BytesIO(base64.b64decode(image_encoded))
    image = Image.open(image_bytes)
    fp = output_path(name + ".jpg")
    image.save(fp)
    print("Saved " + fp)
    print()


test(
    "RealESRGAN_x4plus_anime_6B",
    {
        "modelInputs": {
            "input_image": b64encode_file("cycle.png"),
        },
        "callInputs": {"MODEL_ID": "RealESRGAN_x4plus_anime_6B"},
    },
)

test(
    "RealESRGAN_x4plus",
    {
        "modelInputs": {
            "input_image": b64encode_file("Blake_Lively.jpg"),
            "face_enhance": True,
        },
        "callInputs": {"MODEL_ID": "RealESRGAN_x4plus"},
    },
)

api_key = "YOUR_API_KEY_HERE"
model_key = "YOUR_MODEL_KEY"
model_inputs = {
        "modelInputs": {
            "input_image": b64encode_file("Blake_Lively.jpg"),
            "face_enhance": True,
        },
        "callInputs": {"MODEL_ID": "RealESRGAN_x4plus"},
    }, # anything you want to send to your model

out = banana.run(api_key, model_key, model_inputs)