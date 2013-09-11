from setuptools import setup, find_packages
import upy

setup(name='UPY',
      version=upy.__version__,
      description='''Open-source platform built on top of Django Web Framework, provides useful apps and tools for
                    the most common features to save your time and let you focus just on your specific needs.''',
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
          'Django >=1.5',
          'django_mptt >=0.5.5',
          'django_imagekit >=3',
          'django-modeltranslation >=0.6'
      ],
      requires=[
          'PIL (>1.1.7)',
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      package_data={
          '': ['*.html', '*.css', '*.js', '*.gif', '*.png', ],
      },
      scripts=['upy/bin/upy']
)
