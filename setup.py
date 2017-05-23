from setuptools import setup

setup(name='PollingServer',
      version='1.0',
      description='UK Polling Server',
      author='NicksTricks',
      author_email='nick@nickaltmann.net',
      install_requires=['pandas==0.18.0',
                        'Flask==0.10.1',
                        'xlrd==0.9.4',
                        'beautifulsoup4==4.4.1',
                        'requests==2.9.1',
                        'enum34==1.1.2',
                        'openpyxl==2.4.7',
                        ]
     )
