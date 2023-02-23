#!/usr/bin/python3

from ansible.errors import AnsibleFilterError


class FilterModule:
    """custom filter to check if something is a list"""

    def filters(self):
        return {
            "get_networks": self.get_networks,
            "get_pool": self.get_pool,
        }

    def get_networks(self, networks: list[dict], names: list):
        """get network xml from list"""

        if not isinstance(networks, list):
            raise AnsibleFilterError("This only works on list")

        if not isinstance(names, list):
            raise AnsibleFilterError("name param should be a str")

        return [network for network in networks if network.get("name") in names]

    def get_pool(self, pools: list[dict], name: str):
        """get pool xml from list"""

        if not isinstance(pools, list):
            raise AnsibleFilterError("This only works on list")

        if not isinstance(name, str):
            raise AnsibleFilterError("name param should be a str")

        for pool in pools:
            if pool.get("name") == name:
                return pool
