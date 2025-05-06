import uuid
import re
import subprocess
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='OpenVPNenstein - builds ovpn and onc file for OpenVPN clients')
parser.add_argument('-c', '--config', help='Provide path and filename of server config', required=False)
parser.add_argument('-k', '--keystore', help='Enter keystore if not /etc/openvpn/easy-rsa/pki', required=False)
args = parser.parse_args()

conf_file = args.config if args.config else "/etc/openvpn/server.conf"
keystore = args.keystore.rstrip('\\') if args.keystore else "/etc/openvpn/easy-rsa/pki"

# Get the CA name from OpenVPN's cert
CN = subprocess.Popen(
    ['openssl', 'x509', '-noout', '-subject', '-in', keystore + "/ca.crt"],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

server_name = None
for line in CN.stdout:
    parts = line.decode('utf-8').strip().split("=")
    if len(parts) > 2:
        server_name = parts[2].lstrip()

if not server_name:
    print("Error: Unable to determine server name from CA certificate.")
    sys.exit(1)

print("\nUsing {} as server.conf and {} as keystore folder.\n".format(conf_file, keystore))

# Wake up output file
ovpn_out = open(server_name + ".ovpn", "w")

# Get our key locations and set variables
server_conf = open(conf_file, encoding='utf-8').readlines()
server_conf_keys = {}

for line in server_conf:
    line = line.strip()
    if line.startswith("#") or line.startswith(";") or line == "":
        continue
    if line.startswith("dev"):
        ovpn_out.write(line + "\n")
        dev = line.split(' ')[1]
    if line in ("proto udp", "proto tcp"):
        ovpn_out.write(line + "\n")
        proto = line.split(' ')[1]
    if line.startswith("port"):
        ovpn_out.write(line + "\n")
        port = line.split(' ')[1]
    if line.startswith("cipher"):
        ovpn_out.write(line + "\n")
        cipher = line.split(' ')[1]
    if line.startswith("tls-version"):
        ovpn_out.write(line + "\n")
    if line.startswith("auth"):
        ovpn_out.write(line + "\n")
        auth = line.split(' ')[1]
    if line.startswith("comp-lzo"):
        ovpn_out.write(line + "\n")
        complzo = "false" if line == "comp-lzo false" else "true"
    if line.startswith("tls-auth"):
        ta_loc = line.split(' ')[1]
        if line.split(' ')[2] == "0":
            ovpn_out.write("key-direction 1\n")
            keydir = "1"
        elif line.split(' ')[2] == "1":
            ovpn_out.write("key-direction 0\n")
            keydir = "0"
    if line.startswith("ca"):
        ca_loc = line.split(' ')[1]
    if line.startswith("cert"):
        cert_loc = line.split(' ')[1]
    if line.startswith("username"):
        ovpn_out.write(line + "\n")
        username = line.split(' ')[1]
    if line.startswith("plugin") and "login" in line:
        ovpn_out.write("auth-user-pass\n")

# Write client-specific options that don't change
ovpn_out.write("client\n")
ovpn_out.write("remote-cert-tls server\n")
ovpn_out.write("resolv-retry infinite\n")
ovpn_out.write("redirect-gateway def1\n")
ovpn_out.write("nobind\n")
ovpn_out.write("persist-key\n")
ovpn_out.write("persist-tun\n")
ovpn_out.write("verb 3\n")

# Build a p12 for Chrome
subprocess.Popen(
    [
        'openssl', 'pkcs12', '-export', '-out', server_name + '.p12',
        '-inkey', keystore + '/private/client.key',
        '-in', keystore + '/issued/client.crt',
        '-certfile', keystore + '/ca.crt',
        '-passout', 'pass:chrome'
    ],
    stdout=subprocess.PIPE, stderr=subprocess.PIPE
)

ovpn_out.write("remote " + server_name + "\n")

# Pull keys into vars
with open(keystore + '/issued/client.crt', encoding='utf-8') as f:
    clientcert_in = f.read()
with open(keystore + '/private/client.key', encoding='utf-8') as f:
    clientkey_in = f.read()
with open(ca_loc, encoding='utf-8') as f:
    ca_in = f.read()
with open(ta_loc, encoding='utf-8') as f:
    takey_in = f.read()

clientcert_out = re.search(r'.(--.*)$', clientcert_in, re.DOTALL)
clientkey_out = re.search(r'(--.*)$', clientkey_in, re.DOTALL)
ca_out = re.search(r'(--.*)$', ca_in, re.DOTALL)
takey_out = re.search(r'(--.*)$', takey_in, re.DOTALL)

cakey = ca_out.group(1).replace('\n', '').replace('\r', '')
cakey = cakey.replace('-----BEGIN CERTIFICATE-----', '').replace('-----END CERTIFICATE-----', '')
takey = takey_out.group(1).replace('\n', '\\n').replace('\r', '')

# Write keys
ovpn_fmt = """
<ca>\n%s</ca>
<cert>\n%s</cert>
<key>\n%s</key>
<tls-auth>\n%s</tls-auth>
"""
ovpn_out.write(ovpn_fmt % (ca_out.group(1), clientcert_out.group(1), clientkey_out.group(1), takey_out.group(1)))

# Generate UUIDs
caguid = str(uuid.uuid4())
clientcertguid = str(uuid.uuid4())
netconfigguid = str(uuid.uuid4())

name = server_name
username = username if 'username' in locals() else "User"

try:
    with open("ChromeTemplate.onc", encoding='utf-8') as oncfile:
        onc = oncfile.read()
        onc = onc.replace('$cacert', cakey)
        onc = onc.replace('$takey', takey)
        onc = onc.replace('$remote', server_name)
        onc = onc.replace("$port", port)
        onc = onc.replace("$proto", proto)
        onc = onc.replace("$cipher", cipher)
        onc = onc.replace("$auth", auth)
        onc = onc.replace("$username", username)
        onc = onc.replace("$keydir", keydir)
        onc = onc.replace("$name", server_name)
        onc = onc.replace("$caguid", caguid)
        onc = onc.replace("$clientcertguid", clientcertguid)
        onc = onc.replace("$netconfigguid", netconfigguid)

        if 'complzo' in locals():
            onc = onc.replace("$complzo", complzo)
        else:
            onc = re.sub(r"\"CompLZO.*?,", "", onc)

    with open(server_name + '.onc', 'w+', encoding='utf-8') as outf:
        outf.write(onc)

except IOError:
    print("\nWARNING! Missing ChromeTemplate.onc. Not creating ONC file.\n")

ovpn_out.close()

generated = subprocess.Popen(['ls'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print("Generated:\n")
for line in generated.stdout:
    print("\t- " + line.decode('utf-8').strip())
