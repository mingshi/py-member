from wheezy.captcha.image import captcha

from wheezy.captcha.image import background
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text

from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp

def create() :
    import random
    import string
    captcha_image = captcha(drawings=[
        background(),
        text(fonts=[
            'fonts/VeraMoIt.ttf',
            'fonts/VeraMono.ttf'],
            drawings=[
                warp(),
                rotate(),
                offset()
            ]),
        curve(),
        noise(),
        smooth()
    ])

    _chars = string.uppercase + string.digits
    chars = random.sample(_chars, 4)
    image = captcha_image(chars)
    result = {}
    result['chars'] = chars
    result['image'] = image
    return result
