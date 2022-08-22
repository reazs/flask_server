import json
from flask import jsonify


class Hadiths:
    def __init__(self):
        self.hadith_chapters_name = {}
        self.hadith = {}

    def get_chapters_name(self):
        with open("./truescope/hadiths/hadith_chapter_names.json", "r") as file:
            hadith_chapter_name = json.load(file)
            self.hadith_chapters_name = jsonify({"status":  "ok",
                                                 "code": 200,
                                                 "body": hadith_chapter_name})

    def get_hadith(self):
        with open("./truescope/hadiths/hadiths.json", "r") as file:
            hadtih = json.load(file)

            self.hadith = jsonify(
                {"status": "ok",
                 "code": 200,
                 "body": hadtih}
            )

