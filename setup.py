import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='score.mqtt',
    version='0.0.1',
    description='MQTT integration for The SCORE Framework based on paho-mqtt',
    long_description=README,
    author='nils mueller',
    author_email='nils@mueller.name',
    url='http://score-framework.org',
    keywords='score framework mqtt',
    packages=['score', 'score.mqtt'],
    namespace_packages=['score'],
    zip_safe=False,
    license='LGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General '
            'Public License v3 or later (LGPLv3+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: MQTT :: Client',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'score.init >= 0.3',
        'score.ctx',
        'paho-mqtt'
    ]
)
