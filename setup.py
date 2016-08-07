from setuptools import setup, find_packages
setup(
    name="Flight Searcher",
    version="0.1",
    url="https://github.com/YuriyTimoshenkov/FlightSearcher",
    author="Yuriy Timoshenkov",
    author_email="xsamadhix@gmail.com",
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['tornado','pycrypto', 'momoko'],
)