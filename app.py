import json
import os

import bios
import pandas as pd
import requests
from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)
config = bios.read("config.yaml")
app.config["UPLOAD_FOLDER"] = config["UPLOAD_FOLDER"]
app.config["SECRET_KEY"] = config["SECRET_KEY"]


def allowed_file(filename):
    extension = filename.rsplit(".", 1)[1].lower()
    return "." in filename and extension in config["ALLOWED_EXTENSIONS"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            flash(filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            session["current_filename"] = filename
            return redirect(url_for("predict"))
    else:
        flash("NO POST")
        return render_template("index.html", warning="Please select a file")


@app.route("/predict", methods=["GET"])
def predict():
    try:
        data = pd.read_csv(
            "{}/{}".format(config["UPLOAD_FOLDER"], session["current_filename"])
        )
        body = json.dumps({"data": data.to_json()})
        res = pd.read_json(requests.post(config["URL"], body, config["HEADERS"]).json())
        return render_template(
            "index.html",
            column_names=res.columns.values,
            row_data=list(res.values.tolist()),
            link_column="CustomerID",
            zip=zip,
        )
    except:
        return "Error handling the file", 400


if __name__ == "__main__":
    app.run()
