# This file is part of rddlgym.

# rddlgym is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# rddlgym is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with rddlgym. If not, see <http://www.gnu.org/licenses/>.

# pylint: disable=missing-docstring


from collections import OrderedDict
import gym
from gym import spaces
import numpy as np
import tensorflow as tf

from rddl2tf.core.fluent import TensorFluent

import rddlgym


class RDDLEnv(gym.Env):
    """Gym wrapper for RDDL domains.

    Args:
        rddl (str): RDDL filename or rddlgym id.
    """

    # pylint: disable=too-many-instance-attributes

    def __init__(self, rddl):
        self._compiler = rddlgym.make(rddl, mode=rddlgym.SCG)
        self._compiler.init()

        self._sess = tf.Session(graph=self._compiler.graph)

        self.observation_space = self._create_observation_space()
        self.action_space = self._create_action_space()

        with self._compiler.graph.as_default():
            self._state_inputs = self._build_state_inputs()
            self._action_inputs = self._build_action_inputs()
            self._interms, self._next_state, self._reward = self._build_model_ops()

        self.state = None
        self.timestep = None

    @property
    def horizon(self):
        """Returns the RDDL instance horizon."""
        return self._compiler.rddl.instance.horizon

    def _create_observation_space(self):
        return spaces.Dict(
            {
                name: spaces.Box(
                    low=-np.inf, high=np.inf, shape=fluent.shape.fluent_shape
                )
                for name, fluent in self._compiler.initial_state_fluents
            }
        )

    def _create_action_space(self):
        return spaces.Dict(
            {
                name: spaces.Box(
                    low=-np.inf, high=np.inf, shape=fluent.shape.fluent_shape
                )
                for name, fluent in self._compiler.default_action_fluents
            }
        )

    def _build_state_inputs(self):
        with tf.compat.v1.name_scope("state_input"):
            state_inputs = OrderedDict(
                {
                    name: tf.compat.v1.placeholder(
                        fluent.dtype,
                        shape=fluent.shape.fluent_shape,
                        name=name.replace("/", "-"),
                    )
                    for name, fluent in self._compiler.initial_state_fluents
                }
            )

            return state_inputs

    def _build_action_inputs(self):
        with tf.compat.v1.name_scope("action_inputs"):
            action_inputs = OrderedDict(
                {
                    name: tf.compat.v1.placeholder(
                        fluent.dtype,
                        shape=fluent.shape.fluent_shape,
                        name=name.replace("/", "-"),
                    )
                    for name, fluent in self._compiler.default_action_fluents
                }
            )

            return action_inputs

    def _build_model_ops(self):
        state = tuple(
            TensorFluent(self._state_inputs[name], fluent.scope.as_list())
            for name, fluent in self._compiler.initial_state_fluents
        )

        action = tuple(
            TensorFluent(self._action_inputs[name], fluent.scope.as_list())
            for name, fluent in self._compiler.default_action_fluents
        )

        interms, next_state = self._compiler.cpfs(state, action)
        reward = self._compiler.reward(state, action, next_state)

        return interms, next_state, reward

    def reset(self):
        """Resets the environment state and timestep."""
        self.timestep = 0
        self.state = OrderedDict(
            {
                name: self._sess.run(fluent.tensor)
                for name, fluent in self._compiler.initial_state_fluents
            }
        )
        return self.state, self.timestep

    def step(self, action):
        """Execute `action` in the current state and timestep.
        Updates state and timestep and returns experience tuple
        (state, reward, done, info).

        Args:
            action (Dict[str, np.array])

        Returns:
            next_state (Dict[str, np.array]),
            reward (np.float32),
            done (bool),
            info (Dict[str, np.array])
        """
        interms = list(map(lambda fluent: fluent.tensor, self._interms))
        next_state = list(map(lambda fluent: fluent.tensor, self._next_state))

        interms_, next_state_, reward_ = self._sess.run(
            [interms, next_state, self._reward],
            feed_dict={
                **{
                    self._state_inputs[name]: self.state[name]
                    for name in self._state_inputs
                },
                **{
                    self._action_inputs[name]: action[name]
                    for name in self._action_inputs
                },
            },
        )

        interms_ = OrderedDict(
            zip(self._compiler.rddl.domain.intermediate_cpfs, interms_)
        )
        next_state_ = OrderedDict(zip(self._state_inputs, next_state_))
        reward_ = reward_[0]

        self.state = next_state_
        self.timestep += 1

        done = self.timestep == self.horizon
        info = interms_

        return next_state_, reward_, done, info

    def close(self):
        """Release resources by closing current tf.Session."""
        self._sess.close()

    def render(self, mode="human"):
        """Renders the current state of the environment."""
        return
