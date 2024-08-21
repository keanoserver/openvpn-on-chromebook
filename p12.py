import subprocess
import os

# Define the directory where OpenVPN files are stored
keystore = '/etc/openvpn/easy-rsa/pki'

# Define the server name for the .p12 file
server_name = input("Client's name: ")

# Define the password for the .p12 file
password = input("New password: ")

# Get the save location from the user
save_location = input("Enter file path to save (e.g., /home/user/): ")

# Ensure the save location ends with a slash
if not save_location.endswith('/'):
    save_location += '/'

# Build the full path to the output file
output_file = os.path.join(save_location, f"{server_name}.p12")

# Build the OpenSSL command
command = (
    f"openssl pkcs12 -export "
    f"-out {output_file} "
    f"-inkey {keystore}/private/{server_name}.key "
    f"-in {keystore}/issued/{server_name}.crt "
    f"-certfile {keystore}/ca.crt "
    f"-passout pass:{password}"
)

# Run the command using subprocess.Popen
try:
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode != 0:
        print(f"Error: {stderr.decode('utf-8')}")
    else:
        print(f"Success: The .p12 file has been saved to {output_file}")
except Exception as e:
    print(f"Exception occurred: {str(e)}")
