from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in ssv_reutlingen/__init__.py
from ssv_reutlingen import __version__ as version

setup(
	name="ssv_reutlingen",
	version=version,
	description="ERP sy",
	author="phamos.eu",
	author_email="support@phamos.eu",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
