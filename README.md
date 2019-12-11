# rddlgym [![Build Status](https://travis-ci.org/thiagopbueno/rddlgym.svg?branch=master)](https://travis-ci.org/thiagopbueno/rddlgym) [![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://github.com/thiagopbueno/rddlgym/blob/master/LICENSE)


A toolkit for working with RDDL domains in Python3.

# Quickstart

```text
$ pip3 install rddlgym
```

# Usage

rddlgym can be used as a standalone script or programmatically.


## Script mode

```text
$ rddlgym --help
usage: rddlgym [-h] [--rddl RDDL] [--filepath FILEPATH] [--logdir LOGDIR] [-v]
               {list,info,show,parse,run,viz}

rddl-gym: A toolkit for working with RDDL domains in Python3.

positional arguments:
  {list,info,show,parse,run,viz}
                        available commands

optional arguments:
  -h, --help            show this help message and exit
  --rddl RDDL           RDDL id
  --filepath FILEPATH   trajectory filepath
  --logdir LOGDIR       logdir
  -v, --verbose         verbosity mode
```


## Programmatic mode

```python
import rddlgym

model_id = 'Reservoir-8'

# Get raw RDDL model
raw = rddlgym.make(model_id, mode=rddlgym.RAW)
print(raw)

# Get a RDDL parser
parser = rddlgym.make(model_id, mode=rddlgym.AST)

# Get a RDDL2TensorFlow compiler
compiler = rddlgym.make(model_id, mode=rddlgym.SCG)
```


# License

Copyright (c) 2018-2019 Thiago Pereira Bueno All Rights Reserved.

rddlgym is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at
your option) any later version.

rddlgym is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser
General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with rddlgym. If not, see http://www.gnu.org/licenses/.
