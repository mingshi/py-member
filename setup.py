from setuptools import find_packages, setup

setup(name='member',
    version='0.1',

    package_dir={'': 'member'},
    packages=find_packages('member'),

    install_requires=[
            'python-memcached',
            'Flask',
            'sqlalchemy',
            'Flask-SQLAlchemy',
            'oursql',
            'wheezy.captcha.image'
        ]
        
)
