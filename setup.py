from setuptools import setup, find_packages

setup(
    name='LionAPI',  
    version='0.1.3',  
    packages=['LionAPI', 'LionAPI.app', 'LionAPI.routers', 'LionAPI.services'],
    install_requires=[
        'fastapi',
        'uvicorn',
        'mysql-connector-python',
        'requests'
    ],
    author='Calvin Zheng',
    description='A FastAPI for soccer data',
    url='https://github.com/Calvinzheng123/Soccer-api',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: FastAPI',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  
)
