from setuptools import setup, find_packages


setup(
    name='main',
    version='0.0.1',
    entry_points={
        'console_scripts': ['toolshed=toolshed.main:run']
    },
    packages=find_packages()
)
