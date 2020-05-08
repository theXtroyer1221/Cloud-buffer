from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()
absolute_image_paths = response.download({
    "keywords": "London city",
    "format": "jpg",
    "limit": 4,
    "print_urls": True,
    "size": "medium"
})
