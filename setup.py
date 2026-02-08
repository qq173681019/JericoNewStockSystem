from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="siaps",
    version="0.1.0",
    author="Jerico",
    description="Stock Intelligent Analysis & Prediction System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qq173681019/JericoNewStockSystem",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python-dotenv>=1.0.0",
        "akshare>=1.12.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "requests>=2.31.0",
        "scikit-learn>=1.3.0",
        "torch>=2.0.0",
        "tensorflow>=2.13.0",
        "prophet>=1.1.5",
        "customtkinter>=5.2.0",
        "Pillow>=10.0.0",
        "matplotlib>=3.7.0",
        "sqlalchemy>=2.0.0",
        "python-dateutil>=2.8.2",
        "pytz>=2023.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.1.0",
        ],
    },
)
