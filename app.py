from bottle import Bottle, request, response, static_file, abort, jinja2_template as template
from markdown.extensions.fenced_code import FencedCodeExtension
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.admonition import AdmonitionExtension
from markdown.extensions.smarty import SmartyExtension
from markdown.extensions.meta import MetaExtension
from markdown import Markdown
import os

app = Bottle()
app.config["SECRET_KEY"] = "fpw9jeu9"


@app.route("/static/<file>")
def static(file):
    return static_file(file, root="./static")


@app.route("/content/<folder>/<file>")
def content(folder, file):
    return static_file(file, root=f"./content/{folder}")


@app.route("/")
def home():
    with open("templates/md/index.md", "r") as f:
        data = f.read()
        f.close()
    md = Markdown(extensions=[MetaExtension()])
    html = md.convert(data)
    return template("templates/index.html", html=html, meta=md.Meta)


@app.route("/posts")
@app.route("/posts/")
def post_list():
    return template("templates/posts.html", title="Posts", list=os.listdir("content/posts"))


@app.route("/posts/<name>")
def posts(name):
    try:
        try:
            with open(f"content/posts/{name}.md") as f:
                data = f.read()
                f.close()
        except:
            with open(f"content/posts/{name}.mkd") as f:
                data = f.read()
                f.close()
        md = Markdown(extensions=[FencedCodeExtension(), CodeHiliteExtension(), MetaExtension(), SmartyExtension(), AdmonitionExtension()])
        html = md.convert(data)
    except FileNotFoundError:
        abort(404, text=f"Post \"{name}\" does not exist.")
    return template("templates/post.html", html=html, meta=md.Meta)


app.run(debug=True, reloader=True, interval=2, port=9000)
