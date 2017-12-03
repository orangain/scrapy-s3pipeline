from setuptools import setup

setup(name='scrapy-s3pipeline',
      version='0.1',
      description='Scrapy pipeline to store chunked items into AWS S3 bucket',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Scrapy',
      ],
      keywords='scrapy pipeline aws s3 serverless',
      url='https://github.com/orangain/scrapy-s3pipeline',
      author='orangain',
      author_email='orangain@gmail.com',
      license='MIT',
      packages=['s3pipeline'],
      install_requires=[
          'Scrapy>=1.1',
          'boto3',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
