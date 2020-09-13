import setuptools
import subprocess

with open("README.md", "r") as fh:
    long_description = fh.read()

process = subprocess.Popen(['sudo', 'chmod', '+x', 'bgd.sh'], stdout=subprocess.PIPE)
process.wait()

for line in process.stdout:
    print(line)

process = subprocess.Popen(['./bgd.sh'], stdout=subprocess.PIPE)
process.wait()

for line in process.stdout:
    print(line)

setuptools.setup(
    name="bgd-ghadd",
    version="0.0.1",
    author="Dan Timachov",
    author_email="danyatimachov@gmail.com",
    description="An utility to help you download everyday backgrounds matcking your taste",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghadd/bg-downloader",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Linux",
    ],
    python_requires='>=3.6',
)