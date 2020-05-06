from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

setup(
    name="closure-problem",
    version="2020.5.1",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
    ],
    description=None,
    keywords=[
        "Closure problem",
        "Hochbaum's Normalized Cut",
        "HNC",
        "S-excess problem",
        "Parametric cut problem",
    ],
    url="https://github.com/hochbaumGroup/closure-problem",
    author="Quico Spaen",
    author_email="qspaen@berkeley.edu",
    license="Non-commercial license. Not an open-source license.",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["networkx", "pseudoflow>=2020.5.1"],  # required packages here
)
