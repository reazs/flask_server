from truescope import app

# _hadiths = Hadiths()
# _al_quran = AlQuran()
#
#
#
# @app.route("/")
# def index():
#     return "<h1> Hello World </h1>"
#
#
# @app.route("/getHadithChapterInfo", methods=["GET"])
# def getHadithChapterName():
#     _hadiths.get_chapters_name()
#     return _hadiths.hadith_chapters_name
#
#
# @app.route("/get_hadith", methods=["GET"])
# def get_hadith():
#     _hadiths.get_hadith()
#     return _hadiths.hadith
#
#
# @app.route("/get_quran_chapter", methods=["GET", "POST"])
# def get_quran_chapters():
#     _al_quran.get_quran_chapters()
#     return _al_quran.quran_chapters
#
#
# @app.route("/get_en_quran_chapter", methods=["POST", "GET"])
# def get_quran_chapter():
#     _al_quran.get_quran_chapter(chapter_name=request.args.get("chapter_name"))
#     return _al_quran.quran_chapter
#
#
# @app.route("/quran_editions")
# def quran_editions():
#     _al_quran.get_quran_editions()
#     return _al_quran.quran_editions
#
#
# @app.route("/translated_quran", methods=["POST", "GET"])
# def translated_quran():
#     chapter_name = request.args.get("chapter_name")
#     identifier = request.args.get("identifier")
#     _al_quran.get_translated_quran(chapter_name=chapter_name, identifier=identifier)
#     return _al_quran.translated_quran
#
#
# @app.route("/sing_up", methods=["POST"])
# def sign_up():
#     f_name = request.args.get("f_name")
#     l_name = request.args.get("l_name")
#     email = request.args.get("email")
#     password = request.args.get("password")
#
#     new_user = User(
#         f_name=f_name, l_name=l_name,
#         email=email, password=password
#     )
#     db.session.add(new_user)
#     db.session.commit()
#     return jsonify({
#         "status": "ok",
#         "code": 200,
#         "user": "new user has been created"
#     })


if __name__ == "__main__":
    app.run(debug=True)
