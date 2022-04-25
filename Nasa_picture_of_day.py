
import os
import schedule
import pathlib
import subprocess
import time

SET_WALLPAPER_OSASCRIPT = """/usr/bin/osascript<<END
tell application "Finder"
set desktop picture to POSIX file "{}"
end tell
END"""


def set_wallpaper():
    wallpaper_path = os.path.join(
        # get file path of project
        pathlib.Path().absolute(),
        "M104_HST_final2_1024.jpg"
    )
    subprocess.Popen(SET_WALLPAPER_OSASCRIPT.format(wallpaper_path), shell=True)


def change_wallpaper():
    # schedule for desktop picture to change every 24 hours
    schedule.every(10).seconds.do(set_wallpaper)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    change_wallpaper()
