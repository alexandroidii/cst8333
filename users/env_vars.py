import os

email_user = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASS')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'