from setuptools import setup, find_packages


with open("README.md") as f:
    readme = f.read()

setup(
    name="closure-problem",
    version="0.1dev",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
    ],
    description=None,
    keywords=[
        "Closure problems",
        "Hochbaum's Normalized Cut",
        "HNC",
        "S-excess problem",
        "Parametric problems",
    ],
    url="",
    author="Quico Spaen",
    author_email="qspaen@berkeley.edu",
    license="Non-commercial license. Not an open-source license.",
    long_description=readme,
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["networkx", "pseudoflow"],  # required packages here
)
