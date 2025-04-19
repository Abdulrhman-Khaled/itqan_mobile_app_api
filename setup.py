from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in itqan_mobile_app/__init__.py
from itqan_mobile_app import __version__ as version

setup(
	name="itqan_mobile_app",
	version=version,
	description="Mobile App",
	author="Itqan",
	author_email="info@itqan-kw.net",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
