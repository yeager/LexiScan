"""Setup script for LexiScan."""

from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", encoding="utf-8") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="lexiscan",
    version="1.0.0",
    description="System-wide popup dictionary with Swedish-English support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="LexiScan Team",
    license="GPL-3.0",
    url="https://github.com/yeager/LexiScan",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "gui_scripts": [
            "lexiscan=lexiscan.__main__:main",
        ],
    },
    data_files=[
        ("share/applications", ["data/com.github.lexiscan.desktop"]),
    ],
    package_data={
        "lexiscan": ["../data/style.css"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: X11 Applications :: GTK",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Education",
    ],
)
