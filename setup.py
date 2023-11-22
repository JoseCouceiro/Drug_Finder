from setuptools import setup

setup(
    name="drug_finder",
    version="2.0.1",
    packages=["drug_finder"],
    entry_points={
        "console_scripts": [
            "drug_finder = drug_finder.__main__:main"
        ]
    },
    install_requires=["requests"]
)