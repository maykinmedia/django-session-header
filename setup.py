from setuptools import setup, find_packages

setup(
    name='django-session-header',
    version='0.0',
    description='Identify the session through a header',
    author='Ryan Hiebert',
    author_email='ryan@ryanhiebert.com',
    url='https://github.com/ryanhiebert/django-session-header',
    package_dir={'': 'src'},
    packages=find_packages('src'),
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
