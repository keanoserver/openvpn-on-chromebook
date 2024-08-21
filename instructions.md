[vpn install on chromebook]

For openvpn on chromebook you need an .onc file and a .p12 file and we are gonna make that.
First to make a .onc file you have 2 choices: 
1. Make a client with the name "client".
2. Change the name the onc.py file.

If you chosed option 1 you can skip this part. If you chosed option 2 follow this:
Open onc.py with:
```
sudo nano onc.py
```
or
```
sudo vi onc.py
```
Change the "client" in "/private/client.key" and "/issued/client.crt".
Save an exit after you changed the "client".

Now we continue, You need to install an older version of python for the "onc.py" the version you need is "python 2.7.16" you can install it on this [website](https://www.python.org/downloads/release/python-2716/).
After you instaled python 2.7.16 for youre device we can continue.

First update youre system with:
```
sudo apt update && sudo apt upgrade -y
```
then
```
cd openvpn-on-chromebook
```
and after than
```
sudo python onc.py
```
or
```
sudo python ovpnoncorator.py -c /path/to/my/server.conf -k /path/to/my/keystore-directory
```

Now we have the .onc file, We only need the .p12 file now.

To make the .p12 file you need to follow these steps:
```
sudo apt install python3
```
then
```
cd openvpn-on-chromebook
```
then
```
sudo python3 p12.py
```
After that follow the instructions of the program.
If youre save path didn't end with a "/" it wil automaticly save in "/".

Now you need to get the .onc and the .p12 file on coure chromebook. You can use: sftp, a usb stick or youre own methode.
If you have youre 2 files on youre cromebook open "Chrome" and search this in the search bar:
```
chrome://certificate-manager
```
then click import and bind and select the .p12 file and enter the password you maked.
After you did that you go to:
```
chrome://network/#general
```
scroll down until you find onc-file import. Chose the .onc file and it shuld say no file chosen. Then go to youre vpn options and you shuld see a new vpn connection.
Click on the cpn connection and click configure.
Make teh hostname youre public ip with port, ddns or domain all of them with ":(youre port for the vpn)" after it.
Then scrol down and select the client certificate you imported.
After that you need to enter a password it can be anything you dont need to remember it. 
Then scroll down and click on "save indentity and password".
After that click "save" and the connect.
If you did evry ting corectly it shuld work.

Thank you for useing this repositorie.


