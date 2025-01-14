# rddlgym [![Py Versions][py-versions.svg]][pypi-project] [![PyPI version][pypi-version.svg]][pypi-version] [![Build Status][travis.svg]][travis-project] [![Documentation Status][rtd-badge.svg]][rtd-badge] [![License: GPL v3][license.svg]][license]

A toolkit for working with RDDL domains in Python3. Its main purpose is to wrap a RDDL domain/instance planning problem as an OpenAI Gym environment.

# Quickstart

```text
$ pip3 install -U rddlgym
```

# Features

`rddlgym` implements the OpenAI Gym API for RDDL problems. It uses `pyrddl` to parse RDDL files. Additionally, in order to simulate RDDL domains, it uses `rddl2tf` to compile RDDL operations and expressions to *TensorFlow 1.X* ops.

For further details, please refer to the documentation of the following packages:

- [pyrddl](https://github.com/thiagopbueno/pyrddl): RDDL lexer/parser in Python3.
- [rddl2tf](https://github.com/thiagopbueno/rddl2tf): RDDL2TensorFlow compiler.

---
**NOTE**

Please note that `rddl2tf` (and consequently `rddlgym`) has been mainly developed to support continuous state-action domains. It may not currently work for discrete MDPs.

If you tried to use `rddlgym` with your own RDDL files and encounter errors due (probably) to the RDDL-to-TensorFlow compilation, please do not hesitate to open an issue or contact me.
---

# Usage

`rddlgym` can either be used as a standalone CLI app or it can be integrated with your code in order to implement customized agent-environment interaction loops.

## CLI

```text
$ rddlgym --help
Usage: rddlgym [OPTIONS] COMMAND [ARGS]...

  rddlgym: A toolkit for working with RDDL domains in Python3.

Options:
  --help  Show this message and exit.

Commands:
  info   Print metadata for a `rddl` domain/instance.
  ls     List all RDDL domains and instances available.
  parse  Check RDDL file parsing.
  run    Run random policy in `rddl` domain/instance.
  show   Print `rddl` file.
```

## API

```python
import rddlgym

# create RDDLGYM environment
<<<<<<< HEAD
rddl_id = "Navigation-v3" # see available RDDL with "$ rddlgym ls" command
env = rddlgym.make(rddl_id, mode=rddlgym.GYM) # See all RDDL problems available via `rddlgym ls`
=======
rddl_id = "Navigation-v3" # see available RDDL domains/instances with `rddlgym ls` command
env = rddlgym.make(rddl_id, mode=rddlgym.GYM)
>>>>>>> 0cb07dd (chore(readme): add information about pyrddl and rddl2tf)

# you can also wrap your own RDDL files (domain + instance)
# env = rddlgym.make("/path/to/your/domain_instance.rddl", mode=rddlgym.GYM)

# define random policy
policy = lambda state, t: env.action_space.sample()

# initialize environament
state, t = env.reset()
done = False

# create a trajectory container
trajectory = rddlgym.Trajectory(env)

# sample an episode and store trajectory
while not done:

    action = policy(state, t)
    next_state, reward, done, info = env.step(action)

    trajectory.add_transition(t, state, action, reward, next_state, info, done)

    state = next_state
    t = env.timestep

print(f"Total Reward = {trajectory.total_reward}")
print(f"Episode length = {len(trajectory)}")

filepath = f"/tmp/rddlgym/{rddl}/data.csv"
df = trajectory.save(filepath) # dump episode data as csv file
print(df) # display dataframe
```

# License

Copyright (c) 2018-2020 Thiago Pereira Bueno All Rights Reserved.

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

[py-versions.svg]: https://img.shields.io/pypi/pyversions/rddlgym.svg?logo=python&logoColor=white
[pypi-project]: https://pypi.org/project/rddlgym

[pypi-version.svg]: https://badge.fury.io/py/rddlgym.svg
[pypi-version]: https://badge.fury.io/py/rddlgym

[travis.svg]: https://img.shields.io/travis/thiagopbueno/rddlgym/master.svg?logo=travis
[travis-project]: https://travis-ci.org/thiagopbueno/rddlgym

[rtd-badge.svg]: https://readthedocs.org/projects/rddlgym/badge/?version=latest
[rtd-badge]: https://rddlgym.readthedocs.io/en/latest/?badge=latest

[license.svg]: https://img.shields.io/badge/License-GPL%20v3-blue.svg
[license]: https://github.com/thiagopbueno/rddlgym/blob/master/LICENSE
