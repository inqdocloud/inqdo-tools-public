from setuptools import find_packages, setup

setup(
    name="inqdo-tools",
    description="InQdo Tools Python library",
    url="https://github.com/inQdo/aws_inqdo-tools",
    version="0.1",
    author="InQdo",
    license='LICENSE.txt',
    author_email="barry.buitelaar@inqdo.com",
    packages=find_packages(),
    install_requires=[
        "boto3 >= 1.16.59",
    ],
)
