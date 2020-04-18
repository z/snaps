import os

from setuptools import setup
from setuptools import find_packages

from src.snaps import __author__, __email__, __url__, __license__, __version__, __summary__, __keywords__, __package_name__

in_venv = bool(os.getenv("VIRTUAL_ENV"))

with open('requirements.in') as f:
    install_requires = f.read().splitlines()
    if in_venv:
        install_requires.append('vext.gi')
    else:
        install_requires.append('PyGObject')
with open('README.md') as f:
    readme_contents = f.read()
with open('CHANGELOG.md') as f:
    changelog_contents = f.read()

long_description = '{}\n{}'.format(readme_contents, changelog_contents)

setup(
    name=__package_name__,
    version=__version__,
    description=__summary__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    author_email=__email__,
    url=__url__,
    license=__license__,
    package_dir={'': 'src'},
    packages=find_packages(exclude=('tests', 'docs')),
    package_data={'': ['LICENSE', 'README.md', 'CHANGELOG.md', 'config/*', 'resources/*']},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'snaps = cli:main'.format(__package_name__)
        ]
    },
    keywords=__keywords__,
    classifiers=[
        'Intended Audience :: End Users/Desktop',

        'License :: MIT License',

        'Environment :: Console',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
