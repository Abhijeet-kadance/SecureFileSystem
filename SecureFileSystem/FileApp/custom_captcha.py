
# from gtts import gTTS
from captcha.image import ImageCaptcha
import random
import string
from django.conf import settings

# generate captcha image
def captcha_img_generator(captcha_value):
  # audio = AudioCaptcha()
  image = ImageCaptcha(width=240, height=80)
#   audio = gTTS(text=captcha_value, lang='en', slow=False)
  # print(image.generate(captcha_value))
  print("captch value ", captcha_value)
  image.write(captcha_value, settings.BASE_DIR /'media/captcha_images/CAPTCHA.png')
#   audio.save(settings.BASE_DIR /'media/captcha_audio/CAPTCHA.wav')
  # audio.generate(captcha_value)
  # audio.write("6552", settings.BASE_DIR /'media/captcha_audio/CAPTCHA.wav')
  
# generate random captcha values (letters + digits)
def random_captcha_generator():
  N = 5
  ret = ''.join(random.choices(string.ascii_uppercase + string.digits, k=N))
  return ret