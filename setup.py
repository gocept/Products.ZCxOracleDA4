from setuptools import find_packages
from setuptools import setup


setup(
    name='Products.ZCxOracleDA',
    version='4.0.dev0',
    description="ZCxOracleDA 0.6 ported to Zope 4+",
    long_description=(open("README.rst").read() + "\n" +
                      open("CHANGES.rst").read()),
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Web Environment',
        'Framework :: Zope :: 4',
        'Framework :: Zope :: 5',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    author="Andy Hird, Ryan Hughes",
    author_email="ryan@linuxbox.com",
    maintainer="gocept",
    maintainer_email="mail@gocept.com",
    keywords="zope cx_oracle database",
    license="ZPL 2.0",
    url="https://github.com/gocept/Products.ZCxOracleDA4",
    project_urls={
        'Issue Tracker':
            'https://github.com/gocept/Products.ZCxOracleDA4/issues',
        'Sources': 'https://github.com/gocept/Products.ZCxOracleDA4',
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['Products'],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=[
        'cx_Oracle',
        'Products.ZSQLMethods',
        'setuptools',
        'Zope >= 4.3',
    ],
    entry_points="""
        [zope2.initialize]
        Products.ZCxOracleDA = Products.ZCxOracleDA:initialize
        """,
)
