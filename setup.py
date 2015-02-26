from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksGISVector',
    version='0.0.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    description='Geobricks library to process vector layers.',
    install_requires=[
        'flask',
        'flask-cors',
        # TODO: is it really needed? (right now it just check for bbox)
        'fiona',
        'GeobricksCommon'

    ],
    url='http://pypi.python.org/pypi/GeobricksGISVector/',
    keywords=['geobricks', 'geoserver', 'gis', 'vector']
)
