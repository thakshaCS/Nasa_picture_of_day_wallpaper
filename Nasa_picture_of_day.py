import os
import schedule
import pathlib
import subprocess
import time
from bs4 import BeautifulSoup
import requests
from datetime import date

SET_WALLPAPER_OSASCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{}"
end tell
END"""

PICTURE_URL_BEGINNING = "https://apod.nasa.gov/apod/ap220430"
IMAGE_INFO_URL = "https://apod.nasa.gov/apod/"


class SpecificDateClass:
    day = "02"


def get_wallpaper():
    today = date.today()
    curr_year = today[2:4]
    curr_month = today[5:7]
    curr_day = today[8:]

    picture_url = PICTURE_URL_BEGINNING + curr_year + curr_month + curr_day \
                  + ".html "
    request = requests.get(picture_url)
    soup = BeautifulSoup(request.text, "html.parser")
    images = soup.find_all('img')
    for image in images:
        name = str(today) + '.jpg'
        link = image['src']
        with open(name, 'wb') as f:
            image_info = requests.get(IMAGE_INFO_URL + link)
            f.write(image_info.content)
    return str(today)


def set_wallpaper():
    name_of_image = get_wallpaper()
    wallpaper_path = os.path.join(
        pathlib.Path().absolute(),
        name_of_image + ".jpg"
    )
    subprocess.Popen(SET_WALLPAPER_OSASCRIPT.format(wallpaper_path), shell=True)


def change_wallpaper():

    schedule.every(24).hours.do(set_wallpaper)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    change_wallpaper()
