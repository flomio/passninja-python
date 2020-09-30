from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name = 'passninja',
    version = '1.0',
    author = 'PassNinja',
    license = 'MIT',
    description = 'PassNinja API library for python',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/flomio/passninja-python',
    packages = ['passninja'],
    install_requires = ['requests>=2.8.1'],
    classifiers = [
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=True
)
