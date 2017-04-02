from setuptools import setup, find_packages

setup(name='slack-bot-wrapper',
      version='0.0.1',
      description='Slack Bot Wrapper',
      long_description='Allows to create Slack bots and add features to them '
                       'very easily.',
      url='https://github.com/nicolastrres/slack-bot-wrapper',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      author='Nicolas Agustin Torres',
      author_email='nicolastrres@gmail.com',
      license='MIT',
      keywords='slack bot communication automate tasks',
      packages=find_packages(exclude=['scripts', 'tests']),
      install_requires=['slackclient'],
      zip_safe=False)