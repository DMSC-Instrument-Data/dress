import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dress",
    version="0.0.2",
    author="Neil Vaytet",
    author_email="neil.vaytet@esss.se",
    description="Data Reduction for ESS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ess-dmsc-dram/dress",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=["matplotlib", "numpy", "h5py", "scipy"],
)
