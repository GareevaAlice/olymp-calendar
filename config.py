import os
import random

rand = random.SystemRandom()


def get_random_key(length=50):
    characters = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(rand.choice(characters) for _ in range(length))


# Секретный ключ для валидации формы.
SECRET_KEY = get_random_key()

# База данных
basedir = os.path.abspath(os.path.dirname(__name__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Где разворачиваем приложение.
host = 'localhost'
port = 5000
debug = True

# Путь к OAuth информации (!!!)
# (https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps)
CLIENT_SECRET = 'keys/client_secret.json'
