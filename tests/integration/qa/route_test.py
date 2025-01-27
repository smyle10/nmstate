# SPDX-License-Identifier: LGPL-2.1-or-later

import pytest
import yaml

import libnmstate
from libnmstate.schema import Route

from .qalib.env import rl_is_rhel

from ..testlib.genconf import gen_conf_apply
from ..testlib.route import assert_routes


def load_yaml(content):
    return yaml.load(content, Loader=yaml.SafeLoader)


@pytest.mark.skipif(rl_is_rhel("<", "9"), reason="Support since RHEL 9")
def test_gen_conf_special_routes():
    # TBD: gen_route_data
    desired_state = load_yaml(
        """---
        routes:
          config:
          - destination: 198.18.0.200
            route-type: blackhole
          - destination: 198.18.0.201
            route-type: unreachable
          - destination: 198.18.0.202
            route-type: prohibit
          - destination: 0.0.0.0/8
            route-type: blackhole
            metric: 240
            table-id: 240
          - destination: 0.0.0.0/8
            route-type: unreachable
            metric: 241
            table-id: 241
          - destination: 0.0.0.0/8
            route-type: prohibit
            metric: 242
            table-id: 242
          - destination: 3fff::200
            route-type: blackhole
          - destination: 3fff::201
            route-type: unreachable
          - destination: 3fff::202
            route-type: prohibit
          - destination: 3fff::203
            route-type: blackhole
            metric: 250
            table-id: 250
          - destination: 3fff::204
            route-type: unreachable
            metric: 250
            table-id: 250
          - destination: 3fff::205
            route-type: prohibit
            metric: 250
            table-id: 250
        """
    )
    with gen_conf_apply(desired_state):
        desired_routes = desired_state[Route.KEY][Route.CONFIG]
        for i in range(3):
            desired_routes[i][Route.DESTINATION] += "/32"
        # Linux kernel will automatically set next-hop-interface to lo for IPv6
        # special routes.
        for i in range(6, 12):
            desired_routes[i][Route.NEXT_HOP_INTERFACE] = "lo"
            desired_routes[i][Route.DESTINATION] += "/128"

        cur_state = libnmstate.show()
        # TBD: assert_routes has no metric verification
        assert_routes(desired_routes, cur_state, nic=None)
