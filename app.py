from flask import Flask, request, jsonify

import scrapper

app = Flask(__name__)


@app.route("/", methods=['GET'])
def home():
    return 'Hello World'


@app.route("/api/v1/comics/all/")
async def all_comics():
    page = request.args.get('page')
    order = request.args.get('sortby')
    search = request.args.get('s')
    data = await scrapper.extract_meta_data(scrapper.format_url(orby=order, page=page, keyw=search))
    return jsonify(data)


@app.route("/api/v1/comic/read/chapters/<string:id>")
async def comic_chapter(id):
    chapter = request.args.get('chap')
    data = await scrapper.extract_comic_pages(id, chapter)
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
