from setuptools import setup

setup(
    name="silhouette-cli",
    version="1.0.3",
    description= "Silhouette is a cli tool to bootstrap projects from templates published on Github",
    author= "Hamza EL KAROUI",
    author_email= "helkarou@gmail.com",
    url="https://github.com/sharek-org/Silhouette",
    license="MIT License",
    packages=["slh"],
    include_package_data=True,
    install_requires=[
        "click==7.1.2",
        "requests==2.24.0",
        "GitPython==3.1.12",
        "rich==9.7.0"      
        ],
    entry_points="""
        [console_scripts]
        slh=slh.cli:cli
    """,
)