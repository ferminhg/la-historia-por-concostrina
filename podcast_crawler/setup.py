from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

requirements = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0", 
    "requests>=2.28.0",
    "feedparser>=6.0.0",
    "ruff>=0.1.0"
]

setup(
    name="podcast-crawler",
    version="0.0.1",
    author="Fermin Hernandez",
    author_email="fermin.hdez@gmail.com",
    description="Aplicación para hacer crawling de podcasts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "podcast-crawler=main:main",
        ],
    },
)
