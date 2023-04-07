from setuptools import setup, find_packages

setup(
    name='django-cidr-allowed-hosts',
    version='1.0.0',
    description='Django middleware to allow access from specific CIDR ranges',
    long_description=open('README.md').read(),
    url='https://github.com/wozniakpl/django-cidr-allowed-hosts.git',
    author="Barton Woźniak",
    author_email="bwozniakdev@protonmail.com",
    packages=find_packages(),
    install_requires=[
        "Django>=2.2",
    ],
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)