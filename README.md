# Network Automation Using Paramiko and Ansible

### Overview

This project provides two different approaches to automate network device configuration:

### Using Paramiko (Python): 
* Establishes an SSH connection to network devices.
* executes configuration commands.
* validates the configuration.
* Logs errors for troubleshooting.
*  Using HashiCorp Vault - to get secrets
    ```python
        import hvac
        client = hvac.Client(url="http://127.0.0.1:8200", token="root")
        secret = client.secrets.kv.read_secret_version(path="ise")
        print(secret["data"]["data"]["password"])
    ```

### Using Ansible: 
* Uses Ansible playbooks to configure network devices.
* Ensures configurations are applied and validated.

## 1. Network Automation with Paramiko

### Features:

* Connects to a network device via SSH.

* Configures network interfaces (IP address and subnet mask).

* Validates if the configuration was successful.

* Logs errors for troubleshooting.

### How to Use:

* Install dependencies:
    ```
        pip install paramiko pyyaml
    ```

* Update the device_config.yaml file with your device details.

* Run the Python script:
    ```
        python network_automation.py
    ```

## 2. Network Automation with Ansible

### Features:

* Connects to network devices defined in an inventory file.

* Configures an interface with an IP address and subnet mask.

* Validates if the configuration was applied successfully.

### How to Use:

* Install Ansible:
    ```
    sudo apt install ansible  # For Ubuntu
    brew install ansible  # For Mac
    ```

* Update the inventory.ini file with your network devices.

* Update device_config.yaml with the required interface and IP details.

* Run the Ansible playbook:
    ```
        ansible-vault encrypt_string 'YourPassword' --name 'ansible_password' --vault-password-file vault_password.txt
        ansible-playbook -i inventory.ini configure_network.yml --vault-password-file vault_password.txt

    ```

### 3. Files Included:

#### Supported Device Configurations:

This automation supports configurations for various network devices, including:

* Cisco ISE (Identity Services Engine)
    * User and device authentication policies
    * Network access control settings
* Cisco DNA Center (DNAC)
    * Automation of network provisioning
    * Policy-based network configuration

* Cisco ACI (Application Centric Infrastructure)
    * Tenant and VRF configurations
    * Contract and endpoint group automation

* network_automation.py - Python script using Paramiko.

* configure_network.yml - Ansible playbook.

* device_config.yaml - YAML file containing device configuration.

* inventory.ini - Ansible inventory file.

* README.md - Documentation of the project.

