"""
Django settings for linux_test_system project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+v@0g@=l-tyg)=43-elo#t8coy96-rob8#-v1%pjo(7^@a1qjg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/login/'

LOGOUT_REDIRECT_URL = '/login/'  # Sau khi đăng xuất, chuyển hướng về trang chủ
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'admins',
    'questions',
    'exams',
    'results',
    'certificates',
    'user_panel',
    'django_bootstrap_icons',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'linux_test_system.urls'
APP_DIRS = True
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'admins', 'templates'),  # Thêm đường dẫn này
            os.path.join(BASE_DIR, 'templates'),
        ],
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



WSGI_APPLICATION = 'linux_test_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'linux_test_db',
        'USER': 'root', 
        'PASSWORD': '',   
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
# Database Configuration
# DATABASES = {
#     'default': {
#         'ENGINE': 'mysql.connector.django',
#         'NAME': os.environ.get('MYSQL_DATABASE'), 
#         'USER': os.environ.get('MYSQL_USER'),     
#         'PASSWORD': os.environ.get('MYSQL_PASSWORD'), 
#         'HOST': os.environ.get('MYSQL_HOST'),     
#         'PORT': os.environ.get('MYSQL_PORT', '3306'), 
#         'OPTIONS': {
#             'autocommit': True,
#         }
#     }
# }
# DATABASES = {
#     'default': dj_database_url.config(
#         default=os.environ.get('DATABASE_URL'), # Railway sẽ inject biến này
#         conn_max_age=600, # Giữ kết nối mở để cải thiện hiệu suất
#         conn_health_checks=True, # Tùy chọn: kiểm tra sức khỏe kết nối
#     )
# }
# Rất quan trọng: Thêm dòng này để đảm bảo Django biết đây là MySQL khi dùng dj_database_url
# DATABASES['default']['ENGINE'] = 'django.db.backends.mysql'

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# settings.py
CSRF_TRUSTED_ORIGINS = [
    "https://web-production-68b65.up.railway.app",
]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Thư mục tập hợp file tĩnh
STATIC_URL = '/static/'

# Chỉ định các thư mục chứa file tĩnh
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    
]
# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',  # Chỉ sử dụng JSON, tránh lỗi template
    ),
}

# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')