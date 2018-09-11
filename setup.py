import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
    'oauthlib',
    'plaster_pastedeploy',
    'pyramid',
    'pyramid_jinja2',
    'waitress',
]

setup(
    name='potemkin',
    version='0.0',
    description='A pretend LMS for testing LTI apps',
    long_description=README,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
    ],
    author='Sean Hammond',
    url='https://github.com/seanh/potemkin',
    keywords='web pyramid pylons LTI',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = potemkin:main',
        ],
    },
)
