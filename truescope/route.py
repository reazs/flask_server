from truescope import app
from flask import request, jsonify, redirect, url_for, render_template
from truescope.hadiths import Hadiths
from truescope.models import User, Question, QuestionAnswer, QuestionAnswerComment, FavoriteSurahs, \
    FavoriteHadith
from truescope.quran import AlQuran
from truescope import db
from truescope import bcrypt
import datetime
from flask_login import current_user, login_user, logout_user
from truescope import login_manager
from functools import wraps
from flask import abort
from flask import session
from flask_admin.contrib.sqla import ModelView

_hadiths = Hadiths()
_al_quran = AlQuran()
now = datetime.datetime.now()
date = now.strftime("%m/%d/%Y")


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # If id is not 1 then return abort with 403 error

        if current_user.id != 1:
            return abort(403)
        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login_admin", methods=["POST", "GET"])
def login_admin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return "your logged in"
            else:
                return abort(403)

    return render_template("admin_login.html")


@app.route("/")
def index():
    return "<h1> Hello World </h1>"


@app.route("/getHadithChapterInfo", methods=["GET"])
def getHadithChapterName():
    _hadiths.get_chapters_name()
    return _hadiths.hadith_chapters_name


@app.route("/get_hadith", methods=["GET"])
def get_hadith():
    _hadiths.get_hadith()
    return _hadiths.hadith


@app.route("/get_quran_chapter", methods=["GET", "POST"])
def get_quran_chapters():
    _al_quran.get_quran_chapters()
    return _al_quran.quran_chapters


@app.route("/get_en_quran_chapter", methods=["POST", "GET"])
def get_quran_chapter():
    _al_quran.get_quran_chapter(chapter_name=request.args.get("chapter_name"))
    return _al_quran.quran_chapter


@app.route("/quran_editions")
def quran_editions():
    _al_quran.get_quran_editions()
    return _al_quran.quran_editions


@app.route("/translated_quran", methods=["POST", "GET"])
def translated_quran():
    chapter_name = request.args.get("chapter_name")
    identifier = request.args.get("identifier")
    _al_quran.get_translated_quran(chapter_name=chapter_name, identifier=identifier)
    return _al_quran.translated_quran


@app.route("/sing_up", methods=["POST"])
def sign_up():
    f_name = request.args.get("f_name")
    l_name = request.args.get("l_name")
    f_name = f_name[0].upper() + f_name[1::]
    l_name = l_name[0].upper() + l_name[1::]
    email = request.args.get("email").lower()

    password = request.args.get("password")
    hashed_password = bcrypt.generate_password_hash(password=password).decode('utf-8')

    try:
        new_user = User(
            f_name=f_name, l_name=l_name,
            email=email, password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({
            "status": "not ok",
            "code": 400,
            "user": "user already exits"
        })

    return jsonify({
        "status": "ok",
        "code": 200,
        "user": "new user has been created"
    })


@app.route("/login", methods=["POST"])
def login():
    email = request.args.get("email")
    password = request.args.get("password")

    try:
        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.check_password_hash(password=password, pw_hash=user.password):

                login_user(user)
                return jsonify({
                    "status": "ok",
                    "code": 200,
                    "email": current_user.email,
                    "username": user.f_name + " " + user.l_name,

                })
            else:
                return jsonify({
                    "status": "bad",
                    "code": 400,
                    "user": "found"
                })
        else:
            return jsonify({
                "status": "bad",
                "code": 400,
                "user": "not found"
            })

    except Exception as e:
        print(e)


@app.route("/logout")
def logout():
    logout_user()
    return jsonify(
        {
            "user": "logout",
            "code": 200,
            "status": "ok"
        }
    )


@app.route("/create_question", methods=["POST"])
def crete_question():
    email = request.args.get("email")
    name = request.args.get('username')
    title = request.args.get("question")
    if title != "":
        user = User.query.filter_by(email=email).first()
        question = Question(
            name=name,
            question=title,
            date=date,
            user=user,
        )
        db.session.add(question)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "code": 200,
            "create": "success"
        })
    return jsonify({
        "status": "bad",
        "code": 300,

    })


@app.route("/delete_question", methods=["POST"])
def delete_question():
    id = request.args.get("question_id")
    que = Question.query.filter_by(id=id).first()
    que_ans = QuestionAnswer.query.filter_by(question_id=que.id)
    que_comments = QuestionAnswerComment.query.filter_by(question_id=id)

    for que_answer, comment in zip(que_ans, que_comments):
        db.session.delete(que_answer)
        db.session.delete(comment)
    db.session.delete(que)

    db.session.commit()
    return jsonify({
        "status": "ok",
        "code": 200
    })


@app.route("/delete_ans_comment", methods=["POST"])
def delete_ans_comment():
    id = request.args.get("comment_id")
    ans_comment = QuestionAnswerComment.query.filter_by(id=id).first()
    db.session.delete(ans_comment)
    db.session.commit()
    return jsonify({
        "status": "ok",
        "code": 200
    })


@app.route("/view_question", methods=["POST"])
def view_question():
    id = request.args.get("id")
    que = Question.query.filter_by(id=id).first()
    question = {
        "id": que.id,
        "question": que.question,
        "date": que.date,
        "email": que.user.email,
        "username": que.user.f_name + " " + que.user.l_name
    }

    return jsonify({
        "status": "ok",
        "code": 200,
        "body": question
    })


@app.route("/all_questions", methods=["GET"])
def all_questions():
    ques = Question.query.all()
    questions = []
    for que in ques:
        questions.append(
            {
                "id": que.id,
                "question": que.question,
                "date": que.date,
                "email": que.user.email,
                "username": que.user.f_name + " " + que.user.l_name

            }
        )
    return jsonify({
        "status": "ok",
        "code": 200,
        "body": questions[::-1]
    })


@app.route("/create_question_answer", methods=["POST"])
def create_question_answer():
    id = request.args.get('id')
    name = request.args.get('name')
    answer = request.args.get('answer')
    email = request.args.get("email")
    question = Question.query.filter_by(id=id).first()
    new_answer = QuestionAnswer(
        name=name,
        answer=answer,
        date=date,
        question=question,
        email=email
    )
    if answer != "":
        db.session.add(new_answer)
        db.session.commit()

        return jsonify(
            {
                "status": "ok",
                "code": 200,
                "create": "success"
            }
        )
    return jsonify({
        "status": "bad",
        "code": 300,

    })


@app.route("/view_question_answers", methods=['GET'])
def view_question_answers():
    question_id = request.args.get('question_id')
    question_answers = QuestionAnswer.query.filter_by(question_id=question_id).all()
    que_ans = []
    for answer in question_answers:
        que_ans.append({
            "name": answer.name,
            "id": answer.id,
            "date": answer.date,
            "answer": answer.answer,
            "question_id": answer.question_id,
            "email": answer.email
        })

    return jsonify({
        "status": "ok",
        "code": 200,
        "body": que_ans[::-1]
    })


@app.route("/create_answer_reply", methods=["POST"])
def create_answer_reply():
    id = request.args.get('id')
    question_id = request.args.get('question_id')
    name = request.args.get('name')
    reply = request.args.get("reply")
    email = request.args.get('email')
    if reply != "":
        question_ans = QuestionAnswer.query.filter_by(question_id=question_id, id=id).first()
        new_reply = QuestionAnswerComment(
            name=name,
            comment=reply,
            date=date,
            question_answer=question_ans,
            ques_ans_id=id,
            author_email=email

        )
        db.session.add(new_reply)
        db.session.commit()
        return jsonify({
            "status": "ok",
            "code": 200
        })
    return jsonify({
        "status": "bad",
        "code": 300,

    })


@app.route("/delete_answer", methods=["POST"])
def delete_answer():
    id = request.args.get("answer_id")
    answer = QuestionAnswer.query.filter_by(id=id).first()
    db.session.delete(answer)
    comments = QuestionAnswerComment.query.filter_by(ques_ans_id=id)
    for comment in comments:
        db.session.delete(comment)

    db.session.commit()
    return jsonify({
        "status": "ok",
        "code": 200
    })


@app.route("/view_answer_reply", methods=["GET"])
def view_answer_reply():
    que_id = request.args.get("question_id")
    replies = QuestionAnswerComment.query.filter_by(question_id=que_id)
    json_replies = []
    for reply in replies:
        json_replies.append(
            {
                "id": reply.id,
                "name": reply.name,
                "date": reply.date,
                "question_id": reply.question_id,
                "answer_id": reply.ques_ans_id,
                "email": reply.author_email,
                "reply": reply.comment
            }
        )
    return jsonify({
        "status": "ok",
        "code": 200,
        "body": json_replies
    })


@app.route("/post_favorite_surahs", methods=["POST"])
def post_favorite_surah():
    surah_name = request.args.get("name")
    email = request.args.get("email")
    new_surah = FavoriteSurahs(name=surah_name, email=email)
    db.session.add(new_surah)
    db.session.commit()
    return jsonify({
        "status": "ok",
        "code": 200
    })


@app.route("/get_favorite_surahs", methods=["GET"])
def get_favorite_surahs():
    email = request.args.get("email")
    fav_surahs = FavoriteSurahs.query.filter_by(email=email)
    json_fav_surahs = []
    for surah in fav_surahs:
        json_fav_surahs.append({
            "name": surah.name,
            "email": surah.email,
            "id": surah.id
        })
    return jsonify({
        "status": "ok",
        "code": 200,
        "body": json_fav_surahs
    })


@app.route("/remove_favorite_surah", methods=["POST"])
def remove_favorite_surah():
    name = request.args.get("name")
    email = request.args.get("email")
    surah = FavoriteSurahs.query.filter_by(name=name, email=email).first()
    db.session.delete(surah)
    db.session.commit()
    return jsonify({
        "status": "ok",
        "code": 200
    })


@app.route("/post_favorite_hadith", methods=["POST"])
def post_favorite_hadith():
    chapter_title = request.args.get("chapter_title")
    narrator = request.args.get("narrator")
    content = request.args.get("content")
    email = request.args.get("email")
    new_fav_hadith = FavoriteHadith(
        email=email,
        chapter_title=chapter_title,
        narrator=narrator,
        content=content
    )
    db.session.add(new_fav_hadith)
    db.session.commit()
    return jsonify({
        "status": "ok",
        "code": 200
    })


@app.route("/get_favorite_hadiths", methods=["GET"])
def get_favorite_hadiths():
    email = request.args.get("email")
    fav_hadiths = FavoriteHadith.query.filter_by(email=email)
    favorite_hadiths = []
    for hadith in fav_hadiths:
        favorite_hadiths.append({
            "id": hadith.id,
            "email": hadith.email,
            "chapter_title": hadith.chapter_title,
            "narrator": hadith.narrator,
            "En_Sanad": hadith.narrator,
            "En_Text": hadith.content,
        })
    return jsonify({
        "status": "ok",
        "code": 200,
        "body": favorite_hadiths
    })


@app.route("/remove_favorite_hadith", methods=["POST"])
def remove_favorite_hadith():
    email = request.args.get("email")
    content = request.args.get("content")
    fav_hadith = FavoriteHadith.query.filter_by(email=email, content=content).first()
    db.session.delete(fav_hadith)
    db.session.commit()

    return jsonify({
        "status": "ok",
        "code": 200
    })
