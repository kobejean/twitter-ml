from setuptools import setup

setup(name='tml',
      version='1.0',
      description='A python module for machine learning with twitter data.',
      url='http://github.com/kobejean/twitter-ml',
      packages=[
          'tml',
          'tml.collection',
          'tml.learning.character_prediction',
          'tml.learning.word_embeddings',
          'tml.utils',
      ],
      install_requires=[
          'tensorflow>=1.12.2',
          'tweepy>=3.7.0',
          'keras>=2.2.4',
      ],
      zip_safe=False)
