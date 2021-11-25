# pip install firebase_admin
import firebase_admin
from firebase_admin import credentials, db, storage

from PIL import Image, ImageOps
import urllib.request

cred = credentials.Certificate('./ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jongproject-c30b3-default-rtdb.firebaseio.com/',
    'storageBucket': "jongproject-c30b3.appspot.com"
})
ref = db.reference('Image')
bucket = storage.bucket()


def resize(path, imgSize):
    img = Image.open(path)
    img_resize = img.resize((imgSize, imgSize), Image.LANCZOS)
    img_resize.save(path)


def rotate(path):
    img = Image.open(path)
    rotate_img = img.rotate(90)
    rotate_img.save(path)


def getCountFromDB():
    return len(ref.get())


def getImgFromDB():
    # read from Realtime Database
    snapshot = ref.order_by_key().get()
    first_item = snapshot.popitem(last=True)
    img_info = first_item[1]
    img_url = img_info.get('url')
    #img_location = img_info.get('location')
#    print(img_url)

    # download image from Storage using URL
    urllib.request.urlretrieve(img_url, 'car/download.jpg')

    # Resize image to 416X416
    resize('car/download.jpg', 416)

    # Show Image
    # image = Image.open('car/download.jpg')
    # image.show()


# Upload image to storage and realtime db for testing
def UploadImage(file):
    blob = bucket.blob(file)
    blob.upload_from_filename(filename=file, content_type='image/jpeg')
    blob.make_public()

    ref = db.reference('Image/202111241211')
    ref.set({'url': blob.public_url,
            'size_x': 3840, 'size_y': 4160})


def showImage(path):
    img = Image.open(path)
    img.show()
