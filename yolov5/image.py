# pip install firebase_admin
import firebase_admin
from firebase_admin import credentials, db, storage

from PIL import Image
import io

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


def getCountFromDB():
    return len(ref.get())


def getImgFromDB():
    # snapshot = ref.order_by_key().get()
    # first_item = snapshot.popitem(last=True)
    # img_info = first_item[1]
    # img_data = img_info.get('image')
    # img_size_x = img_info.get('size_x')
    # img_size_y = img_info.get('size_y')

    # image = Image.frombytes('RGBA', (img_size_x, img_size_y), img_data, 'raw')
    # image.show()
    blob = bucket.blob()
    blob.download_to_filename('car')


def UploadImage(file):
    blob = bucket.blob(file)
    # upload file
    blob.upload_from_filename(filename=file, content_type='image/jpeg')
    # print(blob.public_url)

    ref = db.reference('Image/202111241211')
    ref.set({'url': blob.public_url,
            'size_x': 3840, 'size_y': 4160})


if __name__ == '__main__':
    print("Hello World")
    # resize('car/white_car.jpg', 416)

    path = 'car/red_Car.jpg'

    UploadImage(path)

    # getImgFromDB()
    # getCountFromDB()
