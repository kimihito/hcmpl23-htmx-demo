from flask import Flask, render_template, request

from tinydb import TinyDB, Query

db = TinyDB('db.json')
# initialize
db.truncate()

db.insert({"title": "沖縄の大学で育った学生がエンジニアになるまで(仮)", "presenter": "AnaTofuZ"})
db.insert({'title': "HTMX is not a typo", "presenter": "kimihito"})
db.insert({'title': "コードで季節を表現しよう", "presenter": "tompng"})


app = Flask(__name__)
@app.route("/")
def index():
  search_query = request.args.get("q") or None
  talks = None
  if search_query:
    TalkQuery = Query()
    talks = db.search((TalkQuery.title.search(search_query)) | (TalkQuery.presenter.search(search_query)))
  else:
    talks = db.all()

  if request.headers.get("HX-Trigger") == "search":
    return render_template("_rows.html", talks=talks)

  return render_template("index.html", talks=talks)


if __name__ == "__main__":
  app.run()
