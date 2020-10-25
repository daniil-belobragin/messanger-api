from setuptools import setup, find_packages


requires = [
    'sqlalchemy-serializer',
    'marshmallow',
    'psycopg2',
    'flask-cors',
    'eventlet',
    'python-socketio',
    'werkzeug'
]

setup(
    name='messenger-api',
    version='0.0.1',
    url='https://github.com/daniil-belobragin',
    packages=find_packages(),
    install_requires=requires
)
