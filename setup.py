from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setup(
    name='GPUQueue',
    version='0.0.2',
    packages=['gpu_queue'],
    url='https://github.com/jizongFox/GPUQueues',
    license='MIT',
    author='jizong',
    author_email='jizong.peng.1@etsmtl.net',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        'console_scripts': [
            'gpuqueue = gpu_queue.main:main',
        ]
    },

)
