import os
from pathlib import Path



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v7q-tm-lbuwi#+8t-(^_2ym)78b=c6n59i*wb0e2m4glfm5m35'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'home',  # Thêm ứng dụng home của bạn vào đây
    'ckeditor',
    'social_django',  # Thêm ứng dụng social-auth vào đây
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'my_website.urls'

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', 'pk_test_51RNRPKPcxDzDx167NZxBDZomshzvIEpfoVGMDlvemlJBgzsSmHXl8cGVvA3foLQs0btTiZmijBqwyIUbAKj7Ckkq00UI1v9q43')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51RNRPKPcxDzDx167h13xDdFfY4qS2oZT1Cm5ryBq7y8vsat602KNPud4N7NyfnfnfJ6RmDogr8iU5sDKlfI1pjHb004kop9uni')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['home/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_website.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Google OAuth2 configuration
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '380385195968-nktm6mu5jr9k7docq4huoelc7q2mqcfd.apps.googleusercontent.com'  # Thay thế bằng Client ID của bạn
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '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'  # Thay thế bằng Client Secret của bạn

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2', 
    'django.contrib.auth.backends.ModelBackend',  
)

# Login URLs
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ductrungnguyen30@gmail.com'  # Thay thế bằng email của bạn
EMAIL_HOST_PASSWORD = 'lgjd aahh bdcb suyq'  # Thay thế bằng mật khẩu email của bạn

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = "/image/download/"
MEDIA_ROOT = BASE_DIR

# Social Auth URLs configuration (add to urls.py)
SOCIAL_AUTH_URL_NAMESPACE = 'social'

# Other settings for your project...
