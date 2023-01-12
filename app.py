from flask import Flask, request, jsonify

import scrapper

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'


@app.route("/v1/comics/all/", defaults={'order': None, 'page': 1})
@app.route("/v1/comics/all/<string:order>/<int:page>", methods=['GET', 'POST'])
def all_comics(page, order):
    return jsonify(scrapper.extract_meta_data(scrapper.extract_url_data(orby=order, page=page)))


if __name__ == "__main__":
    app.run(debug=True)
