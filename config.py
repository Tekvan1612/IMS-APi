import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'd65an8igcere8l'),
        'USER': os.getenv('DB_USER', 'u3f38j7usj8elq'),
        'PASSWORD': os.getenv('DB_PASS', 'pa4a413c917aa64d30661725f17805fdce774b149cd5c741d9d7ccfd1825e0c63'),
        'HOST': os.getenv('DB_HOST', 'c5p86clmevrg5s.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}
