from setuptools import setup, find_packages

setup(
    name="LionAPI",            
    version="0.1.0",          # Version number
    description="A FastAPI-based soccer data API",
    author="Calvin Zheng",    
    author_email="calvin.zhng12@gmail.com",  # Your email
    packages=find_packages(),   
    include_package_data=True,   
    install_requires=[
        "fastapi",
        "uvicorn",
        "mysql-connector-python",
        "requests",            
    ],
    entry_points={
        'console_scripts': [
            'lion-api=app.main:app',  
        ],
    },
)
