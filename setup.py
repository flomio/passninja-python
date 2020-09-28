from setuptools import setup

setup(
    name = 'passninja',
    version = '1.0',
    description = 'PassNinja API library for python',
    author = 'PassNinja',
    packages = ['passninja'],
    install_requires = ['requests>=2.8.1'],
    classifiers = [
        'Topic :: Software Development :: Libraries',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    zip_safe=True
)
