from flask import Flask
from flask import render_template
from flask import Response
import pandas as pd
import os
import io
import base64
import PIL.Image
import argparse

app = Flask(__name__)

df = pd.read_csv("image_preds.csv", index_col=0)
df = df[~df.index.duplicated(keep='first')]
filenames = list(df.index)
max_imgs = 50

# State dict
state = {
    "class": 0,
    "reverse": True
}


@app.route("/", methods=["GET", "POST"])
def index():
    colname = df.columns[state["class"]]
    sorted_filename = sorted(filenames, key=lambda x: df[colname][x], reverse=state["reverse"])
    sorted_filename = [i+".jpg" for i in sorted_filename]
    return render_template("index.html", current_class=colname, state=state, images=sorted_filename[:max_imgs], classes=df.columns)


@app.route("/next", methods=["GET", "POST"])
def next():
    next_class = state["class"]
    next_class += 1
    if next_class >= 20:
        next_class = 0
    state["class"] = next_class

    return index()


@app.route("/prev", methods=["GET", "POST"])
def prev():
    next_class = state["class"]
    next_class -= 1
    if next_class < 0:
        next_class = 19
    state["class"] = next_class
    return index()


@app.route("/reverse", methods=["GET", "POST"])
def reverse():
    state["reverse"] = not state["reverse"]
    return index()


@app.route("/<img>.jpg")
def render_image(img):
    image = PIL.Image.open(file_path+img+".jpg")
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")
    return Response(buffer.getvalue(), mimetype="image/jpeg")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", default="data/cluster_data/VOCdevkit/VOC2012/JPEGImages/")
    args = parser.parse_args()

    file_path = args.file_path

    app.run(debug=True)
