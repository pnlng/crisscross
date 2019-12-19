from setuptools import setup, find_packages


import crisscross.metadata

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='crisscross',
    version=crisscross.metadata.version,
    author='pnlng',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/pnlng/crisscross',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
      ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'chevron',
        'poyo'
    ],
    entry_points='''
        [console_scripts]
        crisscross=crisscross.cli:cli
    ''',
    python_requires='>=3.5'
)
