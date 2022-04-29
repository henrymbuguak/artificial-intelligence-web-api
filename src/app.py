from urllib import request
from wsgiref import headers
import requests, os, uuid, json
from flask import Flask, redirect, url_for, render_template, session
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def index_post():
    # Read the values from the user input
    original_text = request.form["text"]
    target_language = request.form["language"]

    # Load the values from .env
    key = os.environ["KEY"]
    endpoint = os.environ["ENDPOINT"]
    location = os.environ["LOCATION"]

    # Indicate that we want to translate, the API version and the target language
    path = "/translate?api-version=3.0"

    # Add target language
    target_language_param = "&to=" + target_language

    # Create full URL
    constructed_url = endpoint + path + target_language_param

    # Set up the header information, which include the subscription key
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "Application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    # Create the body of the request with text to be translated
    body = [{"text": original_text}]

    # make the call using post
    translator_request = requests.post(
        constructed_url, headers=headers, json=body
    )

    # Retrieve the JSON response
    translator_response = translator_request.json()

    # Retrieve the translation
    translated_text = translator_response[0]["translations"][0]["text"]
    # Call render template, passing the translated text
    # Original text, and target language to the template
    return render_template(
        "results.html",
        translated_text=translated_text,
        original_text=original_text,
        target_language=target_language,
    )
