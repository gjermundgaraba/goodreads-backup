import ez_setup
ez_setup.use_setuptools()

from setuptools import setup

setup(
    name='goodreads-backup',
    version='1.0',
    packages=['goodreads-backup'],
    url='https://github.com/bjaanes/goodreads-backup',
    license='MIT',
    author='Gjermund Bjaanes',
    author_email='bjaanes@gmail.com',
    description='Python application that backs up your Goodreads shelves',
    install_requires=[]
)
