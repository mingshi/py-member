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
    image = captcha_image(random.sample(string.uppercase + string.digits, 4))
    return image
