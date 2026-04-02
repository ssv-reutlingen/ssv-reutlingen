from setuptools import setup, find_packages
import re
from pathlib import Path


# get version from __version__ variable in ssv_reutlingen/__init__.py
def get_version():
	init_py = Path("ssv_reutlingen/__init__.py")
	if init_py.exists():
		content = init_py.read_text()
		match = re.search(r"^__version__\s*=\s*['\"]([^'\"]*)['\"]", content, re.M)
		if match:
			return match.group(1)
	return "0.1.0"


setup(
	name="ssv_reutlingen",
	version=get_version(),
	description="ERP system for SSV Reutlingen football club",
	author="Phamos GmbH",
	author_email="support@phamos.eu",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=[],
)
