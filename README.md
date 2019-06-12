# checkpoint-management-server

Provides a wrapper for the CheckPoint Management Server in order to retrieve status information

## Requirements

- Ansible Tower

- CheckPoint Managment Server account

- Firewall access enabled to the Checkpoint Management Server

- Python modules
  - json
  - shlex
  - sqlalchemy

## Role Variables

```yaml
cpms_host: cp-01 #CheckPoint Managment Server

cpms_fingerprint: D9:73:57:B9:3C:23:4D:ED:88:19:1B:56:A2:1D:4E:AE:45:24:72:6D #CheckPoint Management Server API Fingerprint https://community.checkpoint.com/t5/API-CLI-Discussion-and-Samples/Management-API-Login-with-certificates/td-p/27410

cpms_username: admin #CheckPoint Management Server username

cpms_password: 12345 #CheckPoint Management Server password/secret
```

## Example Playbook

Presuming that you are using this role within Ansible Tower with inventory groups named CHECKPOINT-Firewalls and CHECKPOINT-Management-Servers, Replace CP-01, CP-02 and CP-MS with valid host names if you wish to run this playbook standalone outside of Tower.

```yaml
- name: CheckPoint Blades Checker

  hosts: localhost

  vars:
    CheckPoints:
      - CP-01
      - CP-03
      - CP-02
    CheckPoint_Management_Servers:
      - CP-MS
    checkpoints_results: {}
    passed_devices: []
    failed_devices: []
    mgmt_task: status

  tasks:
    - name: Set hosts
      set_fact:
        CheckPoints: "{{ groups['CHECKPOINT-Firewalls'] }}"
        CheckPoint_Management_Servers: "{{ groups['CHECKPOINT-Management-Servers'] }}"
      when: groups['CHECKPOINT-Firewalls'] is defined and groups['CHECKPOINT-Management-Servers'] is defined

    - name: CheckPoints we will be querying
      debug:
        var: CheckPoints

    # talk to management server and get CP FW data
    - include_role: name=checkpoint-management-server

    - name: debug results
      debug:
        var: item
      with_items: "{{ checkpoints_results }}"
```

## License

GPL-2.0-or-later

## Author Information

For feedback and comments please contact me via:

mark.baldwin.nz@gmail.com
