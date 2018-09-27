# iatisplit - split IATI activity files into smaller chunks

This is a Python command-line utility that allows splitting [IATI Activity files](http://reference.iatistandard.org/activity-standard/overview/activity-file/) into smaller chunks, limiting the maximum number of activities in each file.

## Requirements

Requires Python3.

## Installation

1. From PyPi:

```
$ pip install iatisplit
```

or (if you have both Python2 and Python3 on your system)

```
$ pip3 install iatisplit
```

2. From the source code:

```
$ python setup.py install
```

or (if you have both Python2 and Python3 on your system)

```
$ python3 setup.py install
```

## Usage

Split into files containing a maximum of 100 activities each:

```
$ iatisplit -n 100 input-data.xml
```

## Output

The output will appear in a number of files in the current working directory, each with an additional 3-digit number before the original extension. For example, splitting the input file ``input-data.xml`` will produce the following output files

* input-data.001.xml
* input-data.002.xml
* input-data.003.xml

etc.

## Source code and bug reporting

The source code is available at https://github.com/davidmegginson/iatisplit/

Please report bugs or feature requests at https://github.com/davidmegginson/iatisplit/issues

## Author and license

This code was started by David Megginson, and is released into the Public Domain with no warranty of any kind. See UNLICENSE.md for details.

