[![Latest](https://img.shields.io/pypi/v/silhouette-cli)](https://pypi.org/project/silhouette-cli/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

# Silhouette
Silhouette is a simple tool to generate projects from templates published on GitHub or any other Git repository. It's inspired from a great tool called [Giter8](http://www.foundweekends.org/giter8/index.html). It's written in python, but can produce files for any programming language.

# Install 
Prerequest : 
- Python 3.6 or above
- pip

To install using `pip` :
```shell
pip install silhouette-cli
```

# Usage
Template repositories must reside on GitHub and be named with the suffix `.slh` . We’re keeping a list of already published templates in the main branch of this project. 

## Generate a project 
To generate a project from an already published template (for example [helkaroui/simple-flask-server.slh](https://github.com/helkaroui/simple-flask-server.slh)), you can run the following command in shell :

```shell
slh new helkaroui/simple-flask-server.slh ./
```


## List referenced templates
We keep track of published templates on github and store them in a json file `ref/templates.json`.

To list the referenced templates, you can run the following command :
```shell
slh list
```


# Making your own templates

## Create a template layout
To create a template you should follow theses guidelines :
- the template should be published publically to github
- the repository name on github should ends with the prefix `.slh`


### Create a template manually
1- Create the `project` directory, this directory is where you should put your files
2- Create a file named `default.properties` at repositroy root. This file is used to declare the project varaibles. Properties are simple keys and values that replace them. 

default.properties file may be placed in project/ directory, or directly under the root of the template. Properties are simple keys and values that replace them. 

### Init a template from command line
use the following command to init an empty template directory :

```shell
slh init myTemplateName
```

## How to use properties
We use a simple engine that evaluates the template's properties declared in `default.properties` file, in all the project files and paths.

## Template properties
The template properties are bracketed with the $ character `$`. For example : a `classname` field might be referenced in the source as: 

```python
class $classname$:

    def __init__(self):
```

If in the interactive input we enter the property `$classname$` with value `MyModule`, the rendered file will contain :

```python
class MyModule:

    def __init__(self):
```

### Formatting template properties
Silhouette supports formatting property fields with built-in functions. For example, the `author` property can be formatted in upper case with :
```
$author;upper$
```

Here are all the formatting functions available :

    "upper" -> To upper case
    "lower" -> To lower case
    "capitalize" -> Converts the first character to upper case
    "casefold" -> Converts string into lower case
    "strip" -> Remove spaces in start and end of the text
    "swapcase" -> Make the lower case letters upper case and the upper case letters lower case
    "title" -> Converts the first character of each word to upper case


