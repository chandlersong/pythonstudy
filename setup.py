from setuptools import setup, find_packages

intall_requires = [

]

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='sparkstudy',
    packages=find_packages(exclude=['tests', 'tests.*', 'demo', 'demo.*', 'scripts', 'scripts.*']),
    version='0.1',
    license=license,
    author='Chandler Song',
    install_requires=intall_requires,
    author_email='chandler605@outlook.com',
    long_description=readme,
    description='spark learning'
)
