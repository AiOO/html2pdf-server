from __future__ import with_statement

try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup


def readme():
    try:
        with open('README.rst') as f:
            return f.read()
    except (IOError, OSError):
        pass


setup(
    name='html2pdf-server',
    description='HTTP server that renders HTML to PDF',
    long_description=readme(),
    url='https://github.com/spoqa/html2pdf-server',
    author='Spoqa',
    author_email='dev' '@' 'spoqa.com',
    maintainer='Spoqa',
    maintainer_email='dev' '@' 'spoqa.com',
    license='AGPLv3 or later',
    py_modules=['html2pdfd'],
    install_requires=[
        'waitress >= 0.8.9',
        'WeasyPrint >= 0.22',
        'Werkzeug >= 0.9'
    ],
    scripts=['html2pdfd.py'],
    entry_points='''
        [console_scripts]
        html2pdfd = html2pdfd:main
    ''',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved ::'
        ' GNU Affero General Public License v3 or later (AGPLv3+)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
        'Topic :: Printing'
    ]
)
