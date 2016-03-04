from setuptools import setup

setup(
    name='django-session-token',
    version='0.0',
    description='cookieless sessions for Django',
    author='Ryan Hiebert',
    author_email='ryan@ryanhiebert.com',
    url='https://github.com/ryanhiebert/django-session-token',
    package_dir={'': 'src'},
    packages=[
        'session_token',
        'session_token.templatetags',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=1.9',
        'djangorestframework>=3.0',
    ],
)
