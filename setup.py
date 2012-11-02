import os
from setuptools import setup, find_packages
from setuptools.dist import Distribution
import pkg_resources
import upy

add_django_dependency = True
try:
    pkg_resources.get_distribution('Django')
    add_django_dependency = False
except pkg_resources.DistributionNotFound:
    try:
        import django
        if django.VERSION[0] >= 1 and django.VERSION[1] >= 2 and django.VERSION[2] >= 0:
            add_django_dependency = False
    except ImportError:
        pass

Distribution({
    "setup_requires": add_django_dependency and  ['Django >=1.4.0'] or []
})

setup(name='UPY',
    version=upy.__version__,
    description='Open-source platform built on top of Django Web Framework, provides useful apps and tools for the most common features to save your time and let you focus just on your specific needs.',
    author='20tab srl: Raffaele Colace - Gabriele Giaccari',
    author_email='info@20tab.com',
    url='http://upyproject.com/',
    license='MIT License',
    platforms=['OS Independent'],
    classifiers=[
        #'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    install_requires=[
        'Django >=1.4.0',
        'django_mptt >=0.5.4',
        'django_imagekit >=2.0.2',
    ],
    requires=[
        'PIL (>1.1.7)',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    package_data = {
        '': ['*.html', '*.css', '*.js', '*.gif', '*.png',],
    },
    scripts= ['upy/bin/upy']
)


