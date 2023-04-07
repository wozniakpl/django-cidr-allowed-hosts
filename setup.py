from setuptools import setup, find_packages

setup(
    name='django-allow-cidr',
    version='1.0.0',
    description='Django middleware to allow access from specific CIDR ranges',
    url='https://github.com/wozniakpl/django-cidr-allowed-hosts.git',
    author="Barton Woźniak",
    author_email="bwozniakdev@protonmail.com",
    packages=find_packages(),
    install_requires=[
        "Django>=2.2",
    ],
)