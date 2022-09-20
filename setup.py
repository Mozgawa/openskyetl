"""Install this Python package."""

import setuptools


with open("README.md", "r", encoding="utf-8") as fp:
    long_description = fp.read()

with open("requirements.txt", encoding="utf-8") as fp:
    requires = [x.strip() for x in fp if x.strip()]


setuptools.setup(
    name="openskyetl",
    version="0.0.1",
    author="Mateusz Mozgawa",
    author_email="mateusz.mozgawa@gmail.com",
    description="Openskyetl.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"openskyetl": ["py.typed"]},
    packages=setuptools.find_packages(exclude=["docs*", "tests*", "envs", "mysql"]),
    include_package_data=True,
    entry_points={"console_scripts": ["openskyetl = openskyetl.pipeline:main"]},
    python_requires=">=3.7, <3.11",
    install_requires=requires,
)
