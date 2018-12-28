from setuptools import find_packages
from setuptools import setup


setup(
    name='wiki',
    version="1.0.0",
    description='Guillotina server application python project',
    long_description="A store for Wikipedia entries",
    install_requires=[
        'guillotina'
    ],
    author='LD',
    author_email='',
    url='',
    packages=find_packages(exclude=['demo']),
    include_package_data=True,
    tests_require=[
        'pytest',
    ],
    extras_require={
        'test': [
            'pytest'
        ]
    },
    classifiers=[],
    entry_points={
    }
)
