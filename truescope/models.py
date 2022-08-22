from truescope import db
from flask_login import UserMixin, current_user
from truescope import admin
from flask_admin.contrib.sqla import ModelView
from flask import abort


class ModelSecureView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated is False:
            return abort(403)
        elif current_user.id == 1:
            return True
        else:
            return abort(403)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    l_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    posts = db.relationship('BlogPost', backref='user')
    questions = db.relationship("Question", backref="user")


class BlogPost(db.Model):
    __searchable__ = ['title', 'content']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    blog_post_comments = db.relationship("BlogPostComment", backref='blog_post')


class Question(db.Model):
    __searchable__ = ['question', 'name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship("QuestionAnswer", backref="question")


class QuestionAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    que_ans_comments = db.relationship("QuestionAnswerComment", backref="question_answer")


class QuestionAnswerComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question_answer.question_id"))
    ques_ans_id = db.Column(db.Integer, nullable=False)
    author_email = db.Column(db.String, nullable=False)


class BlogPostComment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("blog_post.id"))


class FavoriteSurahs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)


class FavoriteHadith(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    chapter_title = db.Column(db.String, nullable=False)
    narrator = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)


admin.add_view(ModelSecureView(FavoriteHadith, db.session))
admin.add_view(ModelSecureView(FavoriteSurahs, db.session))
admin.add_view(ModelSecureView(Question, db.session))
admin.add_view(ModelSecureView(QuestionAnswer, db.session))
admin.add_view(ModelSecureView(QuestionAnswerComment, db.session))
admin.add_view(ModelSecureView(User, db.session))

db.create_all()
