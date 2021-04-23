import os

email_user = os.environ.get('EMAIL_USER')
email_password = os.environ.get('EMAIL_PASS')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'webmaster@rlcs.com'
EMAIL_HOST = 'ns.lange.ca'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rlcs'
EMAIL_HOST_PASSWORD = 'cst8333'

print(email_user)
print(email_password)