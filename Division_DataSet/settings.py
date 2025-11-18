# Rutas y Configuración Base.
import os
from pathlib import Path

# Define el directorio raíz del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta, modo de depuración y hosts permitidos.
SECRET_KEY = '123456'
DEBUG = False
ALLOWED_HOSTS = ['*']

# Lista de aplicaciones de Django y la aplicación del proyecto.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_nsl',
]

# Componentes que procesan las peticiones.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URLS de entrada para las rutas y el servidor WSGI.
ROOT_URLCONF = 'Division_DataSet.urls'
WSGI_APPLICATION = 'Division_DataSet.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Directorios donde se buscan los archivos HTML.
        'DIRS': [os.path.join(BASE_DIR, 'app_nsl', 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            # Variables globales disponibles en todas las plantillas.
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'app_nsl', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'