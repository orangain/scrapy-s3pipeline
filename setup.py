from setuptools import setup
from pathlib import Path

readme_path = Path(__file__).absolute().parent.joinpath('README.md')
long_description = readme_path.read_text(encoding='utf-8')

setup(name='scrapy-s3pipeline',
      version='0.5.0',
      description='Scrapy pipeline to store chunked items into AWS S3 bucket',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Framework :: Scrapy',
      ],
      keywords='scrapy pipeline aws s3 serverless',
      url='https://github.com/orangain/scrapy-s3pipeline',
      author='orangain',
      author_email='orangain@gmail.com',
      license='MIT',
      packages=[
          's3pipeline',
          's3pipeline.strategies',
      ],
      install_requires=['Scrapy>=1.1'],
      extras_require={
          's3': ['boto3'],
          'gcs': ['google-cloud-storage'],
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
