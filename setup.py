from setuptools import setup, find_packages

import catcher


def get_requirements() -> list:
    with open('requirements.txt', 'r') as f:
        return f.readlines()


setup(name='catcher',
      version='1.21.1',
      description='Microservices automated test tool.',
      author='valerii tikhonov'
      author_email='valerii.tikhonov@gmail.com',
      url='https://github.com/comtihon/catcher',
      packages=find_packages(),
      install_requires=get_requirements(),
      include_package_data=True,
      package_data={'catcher': ['resources/*']},
      entry_points={
          'console_scripts': [
              'catcher=catcher.__main__:main'
          ]},
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Testing'
      ],
      extras={'compose': ["docker-compose==1.24.*"]}
      )
