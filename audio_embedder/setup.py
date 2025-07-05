from setuptools import setup, find_packages

setup(
    name="audio_embedder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "openai",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov",
            "ruff",
        ],
    },
    entry_points={
        "console_scripts": [
            "audio-embedder=app.main:main",
        ],
    },
    python_requires=">=3.9",
)