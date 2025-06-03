from setuptools import setup, find_packages

setup(
    name='my_little_snake_helpers',
    version='0.1.20',
    packages=find_packages(),
    install_requires=[],
    description='My toolkit of little python helpers.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Weston Forbes',
    url='https://github.com/westonforbes/my_little_snake_helpers.git',
    python_requires='>=3.11.2',
)
