from flask import Blueprint, request
import os, pyimgur
from jwthelper import gen_random_string

images = Blueprint('images', __name__)
imgur = pyimgur.Imgur(client_id=os.environ.get('IMGUR_CLIENT_ID'))

@images.route('/', methods=['POST'])
def upload_image():
    image = request.files['file']
    tmpfilename = gen_random_string(16)
    image.save(tmpfilename)
    uploadedImage = imgur.upload_image(tmpfilename)
    os.remove(os.path.join(os.getcwd(), tmpfilename))
    
    response = {
        'status': 200,
        'message': 'success',
        'data': {
            'url': uploadedImage.link
        }
    }
    return response, 200