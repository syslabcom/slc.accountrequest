from setuptools import setup, find_packages

version = '0.1'

setup(
    name='slc.accountrequest',
    version=version,
    description="Account request management product",
    long_description=open("README.txt").read(),
    # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Plone",
        ],
    keywords='CMFEditions flexbox',
    author='Izak Burger, Syslab.com GmbH',
    author_email='isburger@gmail.com',
    url='https://github.com/syslabcom/slc.accountrequest',
    license='GPL',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['slc'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'plone.behavior',
        'plone.dexterity',
        'plone.directives.form',
        'zope.schema',
        'zope.interface',
        'zope.component',
        'rwproperty',
        'Products.CMFPlone',
        'five.grok'
    ],
    entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
    """
    )
