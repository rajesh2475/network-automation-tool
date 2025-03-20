import paramiko
import time
import yaml
import logging

# Configure logging
logging.basicConfig(filename='network_automation.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def execute_commands(host, username, password, commands, validate_interface=None, ip_address=None, subnet_mask=None):
    """
    Connects to a network device via SSH and executes a list of commands.
    If validate_interface is provided, it checks if the interface configuration is successful.
    """
    try:
        # Initialize SSH client once
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        # Connect to the device
        ssh.connect(hostname=host, username=username, password=password)
        
        # Open a session
        shell = ssh.invoke_shell()
        
        # Execute all commands within the same session
        for command in commands:
            shell.send(command + "\n")
            time.sleep(2)  # Wait for command execution
            output = shell.recv(65535).decode('utf-8')
            
            # Check if command executed successfully
            exit_code = 0 if "Invalid input" not in output else 1
            
            if exit_code == 0:
                print(f"Command '{command}' executed successfully.\nOutput:\n{output}")
            else:
                print(f"Command '{command}' failed to execute.\nError:\n{output}")
                logging.error(f"Command '{command}' failed to execute. Error: {output}")
        
        # Validate interface configuration if required
        if validate_interface:
            validation_command = f"show ip interface {validate_interface}"
            shell.send(validation_command + "\n")
            time.sleep(2)
            validation_output = shell.recv(65535).decode('utf-8')
            
            if ip_address in validation_output and subnet_mask in validation_output:
                print(f"Interface {validate_interface} is correctly configured with IP {ip_address} {subnet_mask}.")
            else:
                print(f"Configuration validation failed for interface {validate_interface}.")
                logging.error(f"Configuration validation failed for interface {validate_interface}.")
        
        # Close the session and SSH connection
        shell.close()
        ssh.close()
    except paramiko.AuthenticationException:
        error_msg = "Authentication failed. Please check your credentials."
        print(error_msg)
        logging.error(error_msg)
    except paramiko.SSHException as ssh_error:
        error_msg = f"SSH error occurred: {ssh_error}"
        print(error_msg)
        logging.error(error_msg)
    except Exception as e:
        error_msg = f"An error occurred: {e}"
        print(error_msg)
        logging.error(error_msg)

def configure_interface(host, username, password, interface, ip_address, subnet_mask):
    """
    Configure an interface on the network device and validate the configuration.
    """
    commands = [
        f"configure terminal",
        f"interface {interface}",
        f"ip address {ip_address} {subnet_mask}",
        f"no shutdown",
        f"exit",
        f"exit"
    ]
    execute_commands(host, username, password, commands, validate_interface=interface, ip_address=ip_address, subnet_mask=subnet_mask)

def load_device_config(file_path):
    """
    Load device configuration from a YAML file.
    """
    try:
        with open(file_path, 'r') as file:
            config_data = yaml.safe_load(file)
            if not isinstance(config_data, dict):
                raise ValueError("Invalid YAML format: Expected a dictionary structure.")
        return config_data
    except FileNotFoundError:
        error_msg = f"Error: Configuration file '{file_path}' not found."
        print(error_msg)
        logging.error(error_msg)
    except yaml.YAMLError as e:
        error_msg = f"Error parsing YAML file: {e}"
        print(error_msg)
        logging.error(error_msg)
    except Exception as e:
        error_msg = f"Unexpected error loading YAML file: {e}"
        print(error_msg)
        logging.error(error_msg)
    return None

if __name__ == "__main__":
    # Load configuration from YAML
    config_file = "device_config.yaml"  # Specify your YAML file path
    device_config = load_device_config(config_file)
    
    if device_config:
        if "interface" in device_config and "ip_address" in device_config and "subnet_mask" in device_config:
            configure_interface(
                device_config["host"],
                device_config["username"],
                device_config["password"],
                device_config["interface"],
                device_config["ip_address"],
                device_config["subnet_mask"]
            )
        else:
            execute_commands(device_config["host"], device_config["username"], device_config["password"], device_config["commands"])
