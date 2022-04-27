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

PICTURE_URL_BEGINNING = "https://apod.nasa.gov/apod/ap"
IMAGE_INFO_URL = "https://apod.nasa.gov/apod/"


def get_wallpaper() -> str:
    """ Creates the Nasa picture of the day and returns the name of the image
    that was created.
    """
    today = str(date.today())
    curr_year = today[2:4]
    curr_month = today[5:7]
    curr_day = today[8:]

    picture_url = PICTURE_URL_BEGINNING + curr_year + curr_month + curr_day \
                  + ".html"
    name = str(today) + '.jpg'
    request = requests.get(picture_url)
    soup = BeautifulSoup(request.text, "html.parser")
    images = soup.find_all('img')
    for image in images:
        link = image['src']
        with open(name, 'wb') as f:
            image_info = requests.get(IMAGE_INFO_URL + link)
            f.write(image_info.content)
    return today


def set_wallpaper():
    """
    Sets wallpaper to image with the name that is returned from get_wallpaper.
    """
    name_of_image = get_wallpaper()
    wallpaper_path = os.path.join(
        pathlib.Path().absolute(),
        name_of_image + ".jpg"
    )
    subprocess.Popen(SET_WALLPAPER_OSASCRIPT.format(wallpaper_path), shell=True)


def change_wallpaper():
    """
    Changes the wallpaper every 24 hours by calling set_wallpaper.
    """
    schedule.every(5).seconds.do(set_wallpaper)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    change_wallpaper()
