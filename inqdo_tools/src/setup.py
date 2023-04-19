from setuptools import find_packages, setup

setup(
    name="inqdo-tools",
    description="InQdo Tools Python library",
    url="https://github.com/inqdocloud/inqdo-tools-public",
    version="1.3.6",
    author="InQdo",
    license='LICENSE.txt',
    author_email="barry.buitelaar@inqdo.com",
    packages=find_packages(),
    install_requires=[
        "boto3 >= 1.16.59",
    ],
)
