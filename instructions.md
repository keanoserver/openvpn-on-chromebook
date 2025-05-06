[VPN install on Chromebook]

For OpenVPN on Chromebook, you need an .onc file and a .p12 file, and we are going to make those.
First, to make a .onc and .p12 file, you have 2 choices: 
1. Make a client with the name "client".
2. Change the name of the vpn.py file.

If you chose option 1, you can skip this part. If you chose option 2, follow this:
Open vpn.py with:
```
sudo nano vpn.py
```
or
```
sudo vi vpn.py
```
Change the "client" in "/private/client.key" and "/issued/client.crt" on the lines 97,98,108 and 110.
Save an exit after you change the "client".

Now we continue. You need to have python3 installed you can do this with:
```
sudo apt install python3
```

First, update your system with:
```
sudo apt update && sudo apt full-upgrade -y
```
then
```
cd openvpn-on-chromebook-main
```
and after that
```
sudo python3 vpn.py
```
or
```
sudo python3 vpn.py -c /path/to/my/server.conf -k /path/to/my/keystore-directory
```

Now we have the .onc file and the .p12 file.

Second you need to get the .onc and the .p12 file on you're Chromebook. You can use: sftp, a usb stick or youre own method.
If you have youre 2 files on youre Chromebook open "Chrome" and search this in the search bar:
```
chrome://certificate-manager
```
then click import and bind and select the .p12 file and enter the password you maked.
After you did that you go to:
```
chrome://network/#general
```
scroll down until you find onc-file import. Chose the .onc file and it should say no file chosen. Then go to youre vpn options and you should see a new vpn connection.
Click on the vpn connection and click configure.
Make the hostname youre public ip with port, ddns or domain all of them with ":(youre port for the vpn)" after it.
Then scroll down and select the client certificate you imported.
After that you need to enter a password it can be anything you dont need to remember it. 
Then scroll down and click on "save identity and password".
After that click "save" and the connect.
If you did every ting correctly it should work.

Thank you for using this repositories.

