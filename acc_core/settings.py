"""
Django settings for acc_core project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

##from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
##BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&m+iv9)krc8p4dsf^8s*e+_c702%j$@38rumo_2_rd$6ra%li='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'rlcis-env-dev.us-west-2.elasticbeanstalk.com',
    '127.0.0.1',
    ]

# Application definition

INSTALLED_APPS = [
    'rlcis.apps.RlcisConfig',
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'phone_field',
    'django.contrib.sites',
    'django_tables2',
    'django_ajax_tables',
    'django_filters',
    'bootstrap4',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
DJANGO_TABLES2_TEMPLATE = "django_tables2/bootstrap4.html"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'acc_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'acc_core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'rlcis',
            'USER': 'rlcisadm',
            'PASSWORD': '12345678',
            'HOST': 'localhost'

        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, ". .", "www", "static")
STATIC_URL = '/static/'

AUTH_USER_MODEL = 'users.Users' #tell django to utilize this model for users

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'acc_core.backends.CustomEmailAuthBackend.CaseInsensitiveAuth',
)

GOOGLE_RECAPTCHA_SECRET_KEY = '6LdWwV8aAAAAAAmPYinqHliRCDFGvQamTEuYbg2n'

MEDIA_ROOT = os.path.join(BASE_DIR,'media') 

MEDIA_URL = 'rlcis/media/'

LOGIN_REDIRECT_URL = 'users:home'
LOGIN_URL = 'users:login'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'ns.lange.ca'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

CRISPY_CLASS_CONVERTERS = {
    'textinput': "form-control cst__radius",
    'urlinput': "form-control cst__radius",
    'numberinput': "form-control cst__radius",
    'emailinput': "form-control cst__radius",
    'dateinput': "form-control cst__radius",
    'textarea': "form-control cst__radius",
    'passwordinput': "form-control cst__radius",
    'select': "form-control cst__radius",
}

SITE_ID=1   #for 127.0.0.1
#SITE_ID=2  #for rlcis.com



CRISPY_FAIL_SILENTLY = not DEBUG

from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}