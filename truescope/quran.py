import json
from flask import jsonify


class AlQuran:
    def __init__(self):
        self.quran_chapters = {}
        self.quran_chapter = {}
        self.quran_editions = {}
        self.translated_quran = {}

    def get_quran_chapters(self):
        with open("./truescope/al_quran_editions/en_edition.json", "r") as file:
            al_quran = json.load(file)
            chapters = al_quran["data"]["surahs"]

            chapters_info = [

            ]
            for chapter in chapters:
                chapters_info.append({
                    "englishName": chapter['englishName'],
                    "englishNameTranslation": chapter["englishNameTranslation"],
                    "arabicName": chapter["name"]
                }
                )

            self.quran_chapters = jsonify({
                "status": "ok",
                "code": 200,
                "quran_chapters": chapters_info
            })

    def get_quran_chapter(self, chapter_name):
        with open("./truescope/al_quran_editions/en_edition.json", "r") as file:
            al_quran = json.load(file)
            quran_chapter = {}
            chapters = al_quran['data']['surahs']
            for chapter in chapters:
                if chapter_name == chapter['englishName']:
                    quran_chapter = chapter
                    break
        with open("./truescope/al_quran_editions/ar_edition.json", "r") as file:
            ar_quran = json.load(file)
            ar_quran_chapter = {}
            chapters = ar_quran['data']['surahs']
            for chapter in chapters:
                if chapter_name == chapter["englishName"]:
                    ar_quran_chapter = chapter
                    break
        with open("./truescope/al_quran_audio.json", "r") as file:
            quran_audio = json.load(file)
            quran_audio_chapter = {}
            quran_audio_chapters = quran_audio['data']['surahs']

            for chapter in quran_audio_chapters:
                if chapter['englishName'] == chapter_name:
                    quran_audio_chapter = chapter

            self.quran_chapter = jsonify({
                "ar_quran": ar_quran_chapter,
                "en_quran": quran_chapter,
                "quran_audio": quran_audio_chapter
            })

    def get_quran_editions(self):
        with open("./truescope/al_quran_editions/editions.json", "r") as file:
            editions_data = json.load(file)
            languages = []
            for language in editions_data:
                languages.append({
                    "language": language.split(".")[0].upper(),
                    "identifier": language
                })

            self.quran_editions = jsonify({
                "status": "ok",
                "code": 200,
                "body": languages
            })

    def get_translated_quran(self, chapter_name, identifier):
        chapter_name = chapter_name
        identifier = identifier
        with open(f"./truescope/al_quran_editions/{identifier}_edition.json", "r") as file:
            translation_of_quran = json.load(file)
        surahs = translation_of_quran['data']['surahs']
        for surah in surahs:
            if chapter_name == surah['englishName']:
                self.translated_quran = jsonify({
                    "status": "ok",
                    "code": 200,
                    "body": surah
                })
