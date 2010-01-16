from setuptools import setup, find_packages

import sys
sys.path.insert(0, '.')
from shksprdata import __version__
from shksprdata import __doc__ as __long_description__

setup(
    name='shksprdata',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,

    install_requires=[
        ],
    test_suite='nose.collector',
    entry_points='''
    [paste.app_factory]
    main = shakespeare.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [paste.paster_command]
    load-shkspr = shksprdata.cli:LoadTexts
    moby-download = shksprdata.cli:MobyDownload
    moby = shksprdata.cli:Moby
    ''',

    # metadata for upload to PyPI
    author = "Open Knowledge Foundation",
    author_email = 'info@okfn.org',
    description = 'A package of Shakespeare data, that is texts and ancillary materials.',
    long_description = __long_description__,
    license = "MIT",
    keywords = "open shakespeare data texts",
    url = "http://www.openshakespeare.org/", 
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'],
)
