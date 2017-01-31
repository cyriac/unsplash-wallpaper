from appscript import app, mactypes
import urllib.request, urllib.parse, urllib.error
import datetime
import hashlib
import os
import glob
import sys

RANDOM_IMAGE = 'https://source.unsplash.com/random'
CATEGORY_IMAGE = 'https://source.unsplash.com/category/{}'
EMPTY_VALUES = (None, '', [], (), {})

def get_image_url(category):
    url = RANDOM_IMAGE
    if category not in EMPTY_VALUES:
        url = CATEGORY_IMAGE.format(category)
    return url

def get_image(url, target_location):
    return urllib.request.urlretrieve(url, target_location)

def set_wallpaper(location):
    app('Finder').desktop_picture.set(mactypes.File(location))

def clean_old_wallpapers(_target_location):
    for f in glob.glob(_target_location.format("*")):
        os.unlink(f)

now = datetime.datetime.now().isoformat()
hexval = hashlib.md5(now.encode('utf-8')).hexdigest()
_target_location = "/tmp/unsplash-random-wallpaper-{}.jpg"
target_location = _target_location.format(hexval)

clean_old_wallpapers(_target_location)

try:
    category = sys.argv[1]
except IndexError:
    category = None

url = get_image_url(category)
try:
    get_image(url, target_location)
except urllib.error.HTTPError:
    url = get_image_url(None)
    get_image(url, target_location)

set_wallpaper(target_location)
