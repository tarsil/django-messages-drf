from setuptools import find_packages, setup

from django_messages_drf import __version__

def read(fname):
    with open(fname) as fp:
        content = fp.read()
    return content

setup(
    author="Tiago A. Silva",
    author_email="tiago.arasilva@gmail.com",
    description="a reusable private user messages application for Django with Django Rest Framework",
    name="django-messages-drf",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    version=__version__,
    url="https://github.com/tiagoarasilva/django-messages-drf",
    license="MIT",
    packages=find_packages(),
    package_data={
        "django_messages_drf": []
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        "django>=2.2",
        "django-appconf>=1.0.2",
        "djangorestframework>=3.11.1",
    ],
    tests_require=[
        "django-nose>=1.4.6",
        "factory-boy>=3.0.1",
        "django-webtest>=1.9.7"
    ],
    test_suite="tests.runtests",
    zip_safe=False
)
