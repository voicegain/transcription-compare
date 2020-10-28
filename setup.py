import setuptools

# cli
REQUIRES = ["click", "inflect", "tqdm", "nltk", "metaphone", "bs4", "requests", "matplotlib", "seaborn"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="transcribe-compare",
    version="0.1.0",
    author="Huishen Zhan, Kuo Zhang, Jacek Jarmulak",
    author_email="huishen@voicegain.ai, kuo@voicegain.ai, jacek@voicegain.ai",
    description="Voicegain Compare transcription",
    download_url='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=REQUIRES,
    scripts=['transcribe-compare'],
    include_package_data=True
)
