![Molecule test](https://github.com/pimvh/libvirt/actions/workflows/test.yaml/badge.svg)
# Requirements

1. Ansible installed:

```bash
sudo apt install python3
python3 -m ensurepip --upgrade
pip3 install ansible
```

2. Requirements.yaml installed (this role uses [pimvh.cloud_init](https://github.com/pimvh/cloud_init) for templating a cloud-init configuration):

```bash
ansible-galaxy install -r requirements.yaml
```

## Required variables

Review the variables as shown in defaults.

```yaml

# additional libvirt pools to created with XML definition
libvirt_pools:
  - name: nfs
    dir: ""
    xml: ""

# additional libvirt networks to create
libvirt_networks:
  - name: ""
    xml: ""

# Variables to pass to underlying cloud_init role
# Cannot be set per VM
libvirt_cloud_init_add_to_known_hosts: true
libvirt_cloud_init_reboot_on_finish: true

# do not pass when you do not want ansible pull
ansible_pull_config:
  enabled: true # to enable ansible pull
  repo_owner: ""
  repo_name: ""
  playbook_name: ""
  deploy_key_name: "Ansible-pull deploy key" # name of the deploy as shown in Github

# do no pass when you do not want an SSH CA
ssh_ca_config:
  enabled: true
  host_ca_privatekey: "" # remember to check whether this has the correct line endings
  host_ca_privatekey_pass: "" # the passphrase of this private key of the host ca
  host_ca_publickey: "" # public key of the host ca
  user_ca_publickeys:
    - "" # list of public keys

libvirt_virtual_machines:
  - name: guest-01
    ansible_user_passwd_hash: "{{ vault_passwords.ansible }}"
    ram: 2048
    disksize: 20
    vcpus: 2
    networks:
      - vrbr1
    os: ubuntujammy
    pool: default
    image:
      url: https://cloud-images.ubuntu.com/daily/server/jammy/current/jammy-server-cloudimg-amd64-disk-kvm.img
      hashes_url: https://cloud-images.ubuntu.com/daily/server/jammy/current/SHA256SUMS

    # see nested config above
    ansible_pull: "{{ ansible_pull_config }}"
    ssh_ca: "{{ ssh_ca_config }}"

    cloud_init_userdata: # This will be passed to underlying cloudinit role
      hostname: guest-01
      fqdn: guest-01.example.com
      groups: []
      users:
        - name: johndoe
          gecos: John Doe
          shell: /bin/bash
          sudo: ALL=(ALL) NOPASSWD:ALL # Passwordless sudo, can be omitted
          groups: sudo # for sudo access
          lock_passwd: false
          passwd: "passwordhash" # I recommend to use ansible filters for this: {{ guest01_password | password_hash('sha512') }}
      runcmd: []
    cloud_init_networkdata: # This will be passed to underlying cloudinit role
      # Either define IPs
      ipv4: << ipv4 >>
      ipv6: << ipv6 >>
      # --- OR ---
      # dump an entire netplan
      # like the following
      # netplan:
      #   network:
      #     version: 2
      #     ethernets:
      #       enp1s0:
      #         dhcp4: false
      #         addresses:
      #           - << addr >>
      #         gateway4: << addr >>
      #         gateway6: << addr >>
      #         nameservers:
      #           addresses:
      #           - << dns_server ip >>
```

Data within `cloud_init_userdata` and `cloud_init_networkdata` is passed directly to the underlying role pimvh.cloud_init.

See [the README.md of that repository](https://github.com/pimvh/cloud_init) for more information.

# Example playbook

```yaml
hosts:
  - foo
roles:
  - pimvh.libvirt

```

# TLDR - What will happen if I run this

- Assert required variables are defined
- Check if required variables are defined for a VM
- Fetch required image.
- Add the required networks and pools
- Generating a cloud-init config (see underlying role)
- Create VM.
- Reboot the VM when requested.

# Future Improvements

- Improve asserting around conditional variables
- consider making the ansible_pull options pass to underlying cloudinit role passable per VM
