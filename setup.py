import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="check_https_utils",
    version="0.0.1",
    author="Catarina Silva",
    author_email="c.alexandracorreia@ua.pt",
    description="Utilities used in the check https project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/catarinaacsilva/check-https-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['psycopg2>=2.8.3'],
)
