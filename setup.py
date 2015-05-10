from setuptools import setup, find_packages


install_required = [l.strip() for l in open('requestments.txt', 'r')]


metadata = {
    'name': 'narcissus',
    'version': '0.1',
    'packages': find_packages(),
    'author': 'shonenada',
    'author_email': 'shonenada@gmail.com',
    'install_requires': install_required,
}
