from setuptools import setup

setup(
    name="silhouette",
    version="1.0.0",
    packages=["silhouette"],
    include_package_data=True,
    install_requires=[
        "click==7.1.2",
        "requests==2.24.0",
        "GitPython==3.1.12"      
        ],
    entry_points="""
        [console_scripts]
        slh=silhouette.cli:cli
    """,
)