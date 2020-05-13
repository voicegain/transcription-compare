import setuptools

# cli
REQUIRES = ["click", "inflect", "tqdm", "nltk", "metaphone", "bs4", "requests", "matplotlib", "seaborn"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transcription_compare",
    version="0.0.11",
    description="Compare transcription",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    scripts=['transcribe-compare'],
    include_package_data=True
)
