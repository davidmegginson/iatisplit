# iatisplit - split IATI activity files into smaller chunks

This is an early beta version Python command-line utility that allows splitting [IATI Activity files](http://reference.iatistandard.org/activity-standard/overview/activity-file/) into smaller chunks, limiting the maximum number of activities in each file.

## Usage

Split into files containing a maximum of 100 activities each:

```
$ iatisplit -n 100 input-data.xml
```

### Command-line options

The only required option is --max-activities / -n.

--max-activities <num> / -n <num>

Required. Maximum number of IATI activities to include in each output file.
  
--output-directory <dir> / -d <dir>

Output directory for split IATI documents (defaults to ".", which may fail on non-Unix systems). The directory must already exist. iatisplit will overwrite existing files in the directory.
  
--output-stub <filename> / -o <filename>

Base filename for all output files (tries to guess from filename/URL if not provided)
  
--start-date <YYYY-MM-DD> / -s <YYYY-MM-DD>

Include only IATI activities that start on or after this date. Uses the actual start date if present, then falls back to the planned start date.
  
--end-date <YYYY-MM-DD> / - e <YYYY-MM-DD>

Include only IATI activities that end on or before this date. Uses the actual end date if present, then falls back to the planned end date.
  
--humanitarian-only / -h

Include only IATI activities with the humanitarian marker on the activity or one of its transactions (IATI 2.02 and above).
  
--verbose

Include a lot of debugging information about processing.
  
--quiet

Print only error messages.
  

## Output

The output will appear in a number of files in the current working directory, each with an additional 3-digit number before the original extension. For example, splitting the input file ``input-data.xml`` will produce the following output files

* input-data.001.xml
* input-data.002.xml
* input-data.003.xml

etc.


## Calling from Python code

Python code can call the function iatisplit.split.split directly. It
has the following signature (echoing the command-line parameters):

```
def split(
  file_or_url, 
  max, 
  output_dir=".", 
  output_stub=None, 
  start_date=None, 
  end_date=None, 
  humanitarian_only=False
)
```


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


## Source code and bug reporting

The source code is available at https://github.com/davidmegginson/iatisplit/

Please report bugs or feature requests at https://github.com/davidmegginson/iatisplit/issues


## Author and license

This code was started by David Megginson, and is released into the Public Domain with no warranty of any kind. See UNLICENSE.md for details.

