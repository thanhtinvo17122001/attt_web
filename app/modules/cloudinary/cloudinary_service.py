from cloudinary import config, uploader, CloudinaryImage
from datetime import datetime

config(
  cloud_name = 'dvz75ocsa', 
  api_key = '155458469486756', 
  api_secret = 'IW4-nfGPPU0Ddn-WmjZfHmU35ug',
  secure=True
)

def upload_image(file):
  file_name = 'attt/' + datetime.now().strftime('%Y%m%d%H%M%S')
  uploader.upload(file, public_id=file_name, unique_filename = False, overwrite=True)

  return CloudinaryImage(file_name).build_url()
