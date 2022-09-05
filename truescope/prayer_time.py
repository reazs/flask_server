import requests as http
import datetime as datetime
import time


class PrayerTime:
    def __init__(self):
        self.now = datetime.datetime.now()

    def todayPrayerTime(self, latitude, longitude):

        month = self.now.month
        day = self.now.day
        now_time = self.now
        year = self.now.year

        prayer_time_url = prayer_time_url = f"http://api.aladhan.com/v1/calendar?latitude={latitude}&longitude={longitude}&month={month}&year={year}"
        response = http.get(prayer_time_url)
        today_prayer_time = {}
        if response.status_code == 200:
            json_response = response.json()
            prayer_time = json_response['data'][day-1]

            def isActive(now, end):
                current_time = time.strftime("%I:%M %p")

                if time.strptime(current_time, "%I:%M %p") >= time.strptime(now, "%I:%M %p") and time.strptime(
                        current_time, "%I:%M %p") < time.strptime(end, "%I:%M %p"):
                    return True

                else:
                    return False

            fajr = datetime.datetime.strptime(prayer_time['timings']['Fajr'].split(" ")[0], "%H:%M").strftime(
                "%I:%M %p")
            sunrise = datetime.datetime.strptime(prayer_time['timings']['Sunrise'].split(" ")[0], "%H:%M").strftime(
                "%I:%M %p")
            dhuhr = datetime.datetime.strptime(prayer_time['timings']['Dhuhr'].split(" ")[0], "%H:%M").strftime(
                "%I:%M %p")
            asr = datetime.datetime.strptime(prayer_time['timings']['Asr'].split(" ")[0], "%H:%M").strftime("%I:%M %p")
            isha = datetime.datetime.strptime(prayer_time['timings']['Isha'].split(" ")[0], "%H:%M").strftime(
                "%I:%M %p")
            maghrib = datetime.datetime.strptime(prayer_time['timings']['Maghrib'].split(" ")[0], "%H:%M").strftime(
                "%I:%M %p")
            today_prayer_time = {
                "hijri": {
                    "date": prayer_time['date']['hijri']['date'].split("-")[0] + " " +
                            prayer_time['date']['hijri']['month']['en']
                            + ", " + prayer_time['date']['hijri']['date'].split("-")[2],
                    'month': prayer_time['date']['hijri']['month']['en'],
                    "weekday": prayer_time['date']['hijri']['weekday']['en']
                },
                "timings": {
                    "fajr": {"start": fajr, "end": sunrise.split(":")[0] + ":" + str(
                        int(sunrise.split(":")[1].split(" ")[0]) - 1) + " " + sunrise.split(" ")[1],
                             "is_active": isActive(fajr, dhuhr)},
                    "dhuhr": {"start": dhuhr,
                              "end": asr.split(":")[0] + ":" + str(int(asr.split(":")[1].split(" ")[0]) - 1) + " " +
                                     asr.split(" ")[1], "is_active": isActive(dhuhr, asr)},
                    "asr": {"start": asr, "end": maghrib.split(":")[0] + ":" + str(
                        int(maghrib.split(":")[1].split(" ")[0]) - 1) + " " + maghrib.split(" ")[1],
                            "is_active": isActive(asr, maghrib)},

                    "maghrib": {"start": maghrib,
                                "end": isha.split(":")[0] + ":" + str(int(isha.split(":")[1].split(" ")[0]) - 1) + " " +
                                       isha.split(" ")[1], "is_active": isActive(maghrib, isha)},
                    "isha": {"start": isha, "end": "11:59 PM", "is_active": isActive(isha, "11:59 PM")},
                    "sunrise": sunrise
                },
                "city": prayer_time['meta']['timezone'].split("/")[1]

            }
        return today_prayer_time

