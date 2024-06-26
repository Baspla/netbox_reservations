from setuptools import find_packages, setup

setup(
    name='netbox-reservations',
    version='1.2.1',
    description='',
    install_requires=[
        'django-tree-queries>=0.1.0',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
