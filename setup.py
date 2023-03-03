from setuptools import find_packages, setup
from netbox_reservations.util.version import __version__

setup(
    name='netbox-reservations',
    version=__version__,
    description='',
    install_requires=[],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
