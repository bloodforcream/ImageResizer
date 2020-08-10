from PIL import Image as Pillow
from io import BytesIO
import mimetypes
import requests
import shutil
import base64

from core.models import Image

VALID_IMAGE_MIMETYPES = [
    'image'
]

VALID_IMAGE_EXTENSIONS = [
    '.jpg',
    '.jpeg',
    '.png',
    '.gif',
]


def valid_url_mimetype(url, mimetype_list=VALID_IMAGE_MIMETYPES):
    mimetype, encoding = mimetypes.guess_type(url)
    if mimetype:
        return any([mimetype.startswith(mimetype) for mimetype in mimetype_list])
    else:
        return False


def valid_url_extension(url, extension_list=VALID_IMAGE_EXTENSIONS):
    return any([url.endswith(extension) for extension in extension_list])


def get_image_format(string):
    return string.split('.')[-1]


def image_created(add_image_form, slug):
    url = add_image_form.cleaned_data.get('url')
    if url:
        image_format = get_image_format(url)
        if image_downloaded(url, slug, image_format):
            Image.objects.create(image=f'images/{slug}.{image_format}', slug=slug)
            return True
        return False
    Image.objects.create(image=add_image_form.cleaned_data.get('image'), slug=slug)
    return True


def image_downloaded(url, slug, image_format):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(f'media/images/{slug}.{image_format}', 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
        return True
    return False


def resized_image_as_str(instance, resize_image_form):
    image = Pillow.open(instance.image.path)
    resized_image = resize_image(resize_image_form, image)
    current_image_format = get_image_format(instance.image.path)
    with BytesIO() as bytesio:
        resized_image.save(bytesio, format='jpeg' if current_image_format == 'jpg' else current_image_format)
        bytesio.seek(0)
        encoded_string = base64.b64encode(bytesio.read())

    image_as_str = encoded_string.decode()
    return image_as_str


def resize_image(resize_image_form, image):
    width_to_apply = resize_image_form.cleaned_data.get('width')
    height_to_apply = resize_image_form.cleaned_data.get('height')
    if width_to_apply and height_to_apply:
        image = image.resize((width_to_apply, height_to_apply))
    elif width_to_apply:
        new_width_percentage = (width_to_apply / image.width)
        image = image.resize((width_to_apply, int(image.height * new_width_percentage)))
    else:
        new_height_percentage = (height_to_apply / image.height)
        image = image.resize((int(image.width * new_height_percentage), height_to_apply))
    return image
