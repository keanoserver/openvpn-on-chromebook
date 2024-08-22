[VPN install on Chromebook]

For OpenVPN on Chromebook, you need an .onc file and a p12 file, and we are going to make those.
First, to make a .onc file, you have 2 choices: 
1. Make a client with the name "client".
2. Change the name of the onc.py file.

If you chose option 1, you can skip this part. If you chose option 2, follow this:
Open onc.py with:
```
sudo nano onc.py
```
or
```
sudo vi onc.py
```
Change the "client" in "/private/client.key" and "/issued/client.crt".
Save an exit after you change the "client".

Now we continue. You need to install an older version of python for the "onc.py" the version you need is "python 2.7.16" you can install it on this [website](https://www.python.org/downloads/release/python-2716/).
After you install Python 2.7.16 on your device, we can continue.

First, update your system with:
```
sudo apt update && sudo apt upgrade -y
```
then
```
cd openvpn-on-chromebook-main
```
and after than
```
sudo python onc.py
```
or
```
sudo python ovpnoncorator.py -c /path/to/my/server.conf -k /path/to/my/keystore-directory
```

Now we have the .onc file, We only need the .p12 file .

To make the .p12 file, you need to follow these steps:
```
sudo apt install python3
```
then
```
cd openvpn-on-chromebook-main
```
then
```
sudo python3 p12.py
```
After that, follow the instructions of the program.
If you're save path didn't end with a "/" it will automatically save in "/".

Now you need to get the .onc and the .p12 file on you're Chromebook. You can use: sftp, a usb stick or youre own method.
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

