# pip install firebase_admin
import firebase_admin
from firebase_admin import credentials, db

from PIL import Image

cred = credentials.Certificate('./ServiceAccountKey.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jongproject-c30b3-default-rtdb.firebaseio.com/'
})


def resize(path, imgSize):
    img = Image.open(path)

    img_resize = img.resize((imgSize, imgSize), Image.LANCZOS)
    img_resize.save(path)


if __name__ == '__main__':
    print("Hello World")
    #resize('car/white_car.jpg', 416)
    ref = db.reference()
    ref.push({'company': 'google'})
