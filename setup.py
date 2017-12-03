from setuptools import setup

setup(name='scrapy-s3pipeline',
      version='0.1',
      description='Scrapy pipeline to store chunked items into AWS S3 bucket',
      url='https://github.com/orangain/scrapy-s3pipeline',
      author='orangain',
      author_email='orangain@gmail.com',
      license='MIT',
      packages=['s3pipeline'],
      install_requires=[
          'Scrapy>=1.1',
          'boto3',
      ],
      zip_safe=False)
