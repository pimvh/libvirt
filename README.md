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
libvirt_pools:
  - name: nfs
    dir: "....."
    xml: '....'
# ...

libvirt_networks:
  - name: ...
    xml: '....'

# Variables to pass to underlying cloud_init role
libvirt_cloud_init_enable_ssh_ca: true
libvirt_cloud_init_enable_ansible_pull: false
libvirt_cloud_init_register_github_key: false
libvirt_cloud_init_add_to_known_hosts: true
libvirt_cloud_init_reboot_on_finish: true

libvirt_virtual_machines:
  # - name: guest-01
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
- Check if required variables are defined for a VM
- Fetch required image.
- Generating a cloud-init config (see underlying role)
- Add the required networks and pools
- Create VM.

# Future Improvements

- Improve asserting around conditional variables
- Fix issue where VM does not reboot, after cloud_init is finished
