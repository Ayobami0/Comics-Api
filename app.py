from flask import Flask, request, jsonify

import scrapper

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'


@app.route("/api/v1/comics/all/", defaults={'page': 1, 'order': ''})
@app.route("/api/v1/comics/all/<int:page>", defaults={'order': ''})
@app.route("/api/v1/comics/all/<order>/<int:page>/", methods=['GET'])
async def all_comics(page, order):
    data = await scrapper.extract_meta_data(scrapper.format_url(orby=order, page=page))
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
