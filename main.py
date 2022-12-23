from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
import secrets

SECRET_KEY = secrets.token_hex()

app = Flask(__name__)

# create db
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config['SQLALCHEMY_TRACk_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
app.config['CKEDITOR_PKG_TYPE'] = 'standard'
app.config['CKEDITOR_SERVE_LOCAL'] = True
db.init_app(app)


# define model
class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(1), nullable=False)
    title = db.Column(db.String, nullable=False)
    article = db.Column(db.String, nullable=False)


# create table
with app.app_context():
    db.create_all()

ckeditor = CKEditor(app)


# create form
class BlogForm(FlaskForm):
    author = StringField('作成者', validators=[DataRequired(message="作成者を入力してください")])
    title = StringField('タイトル', validators=[DataRequired(message="タイトルを入力してください")])
    article = CKEditorField("記事", validators=[DataRequired(message="記事内容を入力してください")])
    submit = SubmitField("登録")


@app.route("/")
def home():
    blogs = db.session.query(Blogs).all()
    return render_template('index.html', blogs=blogs)


@app.route("/new_post", methods=["GET", "POST"])
def new_post():
    form = BlogForm()
    if form.validate_on_submit() and request.method == "POST":
        rep = request.form
        print(rep)
        blog = Blogs(
            author=rep["author"],
            title=rep['title'],
            article=rep['article']
        )
        db.session.add(blog)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('new_post.html', form=form)


@app.route("/post/<int:post_id>")
def show_post(post_id):
    requested_post = Blogs.query.get(post_id)
    return render_template('post.html', post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
