from setuptools import setup, find_packages

requires = [
    'argparse',
]

setup(
    name='pve-config-filedump',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=requires,
    entry_points={
        'console_scripts': ['pve-config-filedump=filedump:main']
    }
)
