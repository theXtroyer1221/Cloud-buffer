import json
from flask import request

from google_images_search import GoogleImagesSearch

gis = GoogleImagesSearch("AIzaSyDzlZD6DZWdqhsH__KaM_x5ohDqYJX7xrM",
                         "013299270315827120003:el8nk3thdun")
google_search_params = {
    'q': "bla",
    'num': 1,
    'safe': 'off',
    'fileType': 'jpg',
    'imgSize': 'xlarge'
}

gis.search(search_params=google_search_params)

for image in gis.results():
    img = image.url
    print(img)

print(request.access_route[-1])
