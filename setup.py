"""
Setup the package.
"""
from setuptools import find_packages, setup

DESCRIPTION = 'Python design kit: ' \
              'interfaces, declared exception throws, ' \
              'class members accessibility levels (private and protected methods for humans).'

with open('README.md', 'r') as read_me:
    long_description = read_me.read()

setup(
    version='0.3.1',
    name='accessify',
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/dmytrostriletskyi/accessify',
    license='MIT',
    author='Dmytro Striletskyi',
    author_email='dmytro.striletskyi@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
    ],
)
