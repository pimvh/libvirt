# Requirements

1. Ansible installed:

```
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

2. Requirements.yaml installed (this role uses [pimvh.cloud_init](https://github.com/pimvh/cloud_init)):

```
ansible-galaxy install -r requirements.yaml
```

## Required variables

Review the variables as shown in defaults.

```
libvirt_pools: []
# libvirt_pools: # Example
#   default:
#     dir: "/var/lib/libvirt/images"
#     xml: ....

libvirt_networks: []
# libvirt_networks: # Example
#   vrbr1:
      xml: ....

# Variables to pass to underlying cloud_init role
libvirt_cloud_init_enable_ssh_ca: true
libvirt_cloud_init_enable_ansible_pull: false
libvirt_cloud_init_register_github_key: false
libvirt_cloud_init_add_to_known_hosts: true
libvirt_cloud_init_reboot_on_finish: true

libvirt_virtual_machines:
  []
  # guest-01: # Example config
  #   name: guest-01
  #   ram: 2048
  #   disksize: 20
  #   vcpus: 2
  #   networks:
  #     - vrbr1
  #   os: ubuntujammy
  #   pool: default
  #   image:
  #     url: https://cloud-images.ubuntu.com/daily/server/jammy/current/jammy-server-cloudimg-amd64-disk-kvm.img
  #     hashes_url: https://cloud-images.ubuntu.com/daily/server/jammy/current/SHA256SUMS
  #   cloud_init_userdata: # This will be passed to underlying cloudinit role
  #     hostname: guest-01
  #     fqdn: guest-01.example.com
  #     groups: []
  #     users:
  #       - name: johndoe
  #         gecos: John Doe
  #         shell: /bin/bash
  #         sudo: ALL=(ALL) NOPASSWD:ALL # Passwordless sudo, can be omitted
  #         groups: sudo # for sudo access
  #         lock_passwd: false
  #         passwd: "passwordhash" # I recommend to use ansible filters for this: {{ guest01_password | password_hash('sha512') }}
  #     runcmd: []
  #   cloud_init_networkdata: # This will be passed to underlying cloudinit role
  #     # Either define IPs
  #     ipv4: << ipv4 >>
  #     ipv6: << ipv6 >>
  #     # --- OR ---
  #     # dump an entire netplan
  #     # like the following
  #     netplan:
  #       network:
  #         version: 2
  #         ethernets:
  #           enp1s0:
  #             dhcp4: false
  #             addresses:
  #               - << addr >>
  #             gateway4: << addr >>
  #             gateway6: << addr >>
  #             nameservers:
  #               addresses:
  #               - << dns_server ip >>
```

Data within `cloud_init_userdata` and `cloud_init_networkdata` is passed directly to the underlying role pimvh.cloud_init.

See [the README.md of that repository](https://github.com/pimvh/cloud_init) for more information.

# Example playbook

```
hosts:
  - foo
roles:
  - pimvh.libvirt

```

# TLDR - What will happen if I run this

- Assert required variables are defined

# Future Improvements

- Improve asserting around conditional variables
- Fix issue where VM does not reboot, after cloud_init is finished

# License

The GPLv3 License (GPLv3)

Copyright (c) 2022 Author

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
