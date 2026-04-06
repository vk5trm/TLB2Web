The Link Box Node or The Bridge Conference Server Management Web CGI
This software permits you to be able to control a “The Link Box Node” or The Bridge Conference Server from a standard web page
.It is an add on to “The Link Box RF node” and “The Bridge conference server” written by Skip WB6YMH
It also includes the ability to use the Text chat over the Echolink System. 
Optional Module 1 – Email from Echolink Text Box
If there is a problem with your node the sysop can be emailed directly from the text box on echolink by using the format
**(node-call) **(message) i.e. **VK5TRM-L** This is a test message
The callsign must be all upper case, include the -L or -R and you can't use the .quote command
This is comparable with Peter EI4JR's Echo Producer program and his other Windows Echolink add ons
Optional Module 2 Temperature Sensor/Radio Control 
I have also added the ability to get temperature readings using a PIC based serial port device It gives you inside temperature on the page and if there is hardware setup the ability to control the radio on/off and channel change from the webpage.
The kit is available from kitsrus.com. worldwide
I am using the K190 Which is available from one of there distributors here in Australia Oztronics




Requirements:

A working TLB node with the Command Port and event script enabled within the tlb.conf
A working Apache Web server with PHP,Perl enabled on the same computer with the CGI execution enabled and Basic Authentication also enabled. 
Install
All setups:
Download the TLB to Web CGI and put it into a temp directory on the Linux computer.
Issue the command "tar xzf TLBtoWeb.tgz"to uncompress the files.
Copy these files into your cgi-bin enabled directory (on my Apache server it is /var/www/cgi-bin)
and set permissions as follows using chmod 

chat.html (RW-R--R-- or 644)
nodemgmt.cgi (RWXR-XR-X or 755)
chat.txt (RW-RW-RW- or 666)
fuzzy-lightgrey.jpg (RW--R--R-- or 644)
chat.cgi (RWXR-XR-X or 755) 
logviewer.cgi (RWXR-XR-X or 755) 
htpasswd.cgi (RWXR-XR-X or 755) 
index.html (RW-R--R-- or 644) 
README.html (RW-R--R-- or 644) 

Extra files required for Radio Control (also put in the CGI-Bin Dir)
php_serial.class.php (RW-R--R-- or 644)
radiocontrol.php (RW-R--R-- or 644)
channeldata.html (RW-R--R-- or 644)
Configuration
BASIC SETUP: or basic setup with only Temperature Sensor/Radio control
Either Add the following lines to your eventscript file or if you don't have one create a file called eventscript in /usr/local/bin/ and enable it within your tlb.conf file
You may need to change you file paths if you computer has the files in a different place

----snip--------

if [ "$1" = "chat" ]; then
echo "$2 <br>" >> /var/www/cgi-bin/chat.txt
elif [ "$1" = "sent_chat" ]; then
echo "$2 <br>" >> /var/www/cgi-bin/chat.txt
fi
/usr/bin/tail -n 21 /var/www/cgi-bin/chat.txt > /tmp/chat.txt
/bin/cp /tmp/chat.txt /var/www/cgi-bin/chat.txt
/bin/rm /tmp/chat.txt

----snip-------

Nodemgmt.cgi with Email from Echolink Text Box enabled or Email from Echolink Text Box and Temperature Sensor/Radio control
Copy the sendEmail file to your /usr/bin Directory and set the permissions to RWXR-XR-X or 755 using chmod 755 sendEmail
Either Add the following lines to your eventscript file or if you don't have one create a file called eventscript in /usr/local/bin/ and enable it within your tlb.conf file
You may need to change you file paths if you computer has the files in a different place

----snip--------

if [ "$1" = "chat" ]; then
nodecall=`cat /usr/local/etc/tlb.conf | /bin/grep "ConferenceCall = " | cut -d' ' -f3`
nodeEmail=`cat /usr/local/etc/tlb.conf | /bin/grep "EmailAdr = " | cut -d' ' -f3`
IFS=$'**' 
/bin/echo "$2" | /bin/grep -w "$nodecall"
if [ $? -eq 0 ]; then
/usr/bin/sendEmail -f "$nodeEmail" -t "$nodeEmail" -u Message from "$nodecall" -m "$2" 
/usr/local/bin/tlbcmd message "$nodecall>Message recieved and Emailed to sysop"
else
echo "$2 <br>" >> /var/www/cgi-bin/chat.txt
fi
IFS=$' \t\n' 
elif [ "$1" = "sent_chat" ]; then
echo "$2 <br>" >> /var/www/cgi-bin/chat.txt
fi
/usr/bin/tail -n 21 /var/www/cgi-bin/chat.txt > /tmp/chat.txt
/bin/cp /tmp/chat.txt /var/www/cgi-bin/chat.txt
/bin/rm /tmp/chat.txt

----snip-------

All setups :
Apache web server setup
Set up Apache so the the root directory is the cgi-bin directory or set up a named virtual host container to your cgi-bin directory and point a sub domain to the virtual named host. The information on how to do this is here on the Apache Website
Use Basic Authentication on the webpage. The information on how to do that is on the Apache Website. Use callsigns as usernames as the login name is what is used on the sent text chat callsign from the website and if no user name is present it goes into demo mode and all control buttons are disabled automaticly. This is to protect the network from non- Amateurs. It is up to you to make sure no non-Amateurs gain access to the Echolink system though your node.
Edit the top Installation Default Settings section of nodemgmt.cgi and chat.cgi file 

----snip-------

#-------------------------------------------------------------------
# Installation Default Settings
confname=VK5TRM-L # name of this conference must be in Upper Case
admin=VK5TRM # admin's callsign must be in Upper Case
qrz=yes # leave blank to disable QRZ lookups
chginfo=no # enable/disable Info/Location changes
tbdcmd=/usr/local/bin/tlbcmd # path to "tbdcmd or tlbcmd" executable
tlbchat=/usr/local/bin/tlbchat # path to "tlbchat" executable
commport=/dev/ttyS1 # Comm Port for Temperature sensor & Radio control - set for option 2
#-------------------------------------------------------------------

----snip-------

Nodemgmt.cgi with Email from Echolink Text Box enabled 
Set up your email SMTP server in the top section of the SendEmail Script in the ##Network section of the script. You should only need to set you SMTP server and port. Be careful not to delete any of the , and '

----snip-------

## Network
"server" => 'localhost', ## Default SMTP server (set your server here between the ' ')
"port" => 25, ## Default port (set you SMTP server port here between the ' ')
"bindaddr" => '', ## Default local bind address
"alarm" => '', ## Default timeout for connects and reads, this gets set from $opt{'timeout'}
"tls_client" => 0, ## If TLS is supported by the client (us)
"tls_server" => 0, ## If TLS is supported by the remote SMTP server

----snip-------

Also edit the SMTP user name and password in the SendEmail script further down

----snip-------

## eSMTP
"username" => '', ## Username used in SMTP Auth (set your SMPT server user name here between the ' ')
"password" => '', ## Password used in SMTP Auth (set you SMPT server password here between the ' ')
"tls" => 'auto', ## Enable or disable TLS support. Options: auto, yes, no

----snip-------

Radio Control (radiocontrol.php)
Edit radiocontrol.php if you want to use it and have the hardware for it. Set port device, port speed, data bits, stopbit, and flow control according to the manual that came with the hardware 
This needs to be done in 2 places of the script

----snip-------

$serial->deviceSet("/dev/ttyUSB0");

// We can change the baud rate, parity, length, stop bits, flow control
$serial->confBaudRate(9600);
$serial->confParity("none");
$serial->confCharacterLength(8);
$serial->confStopBits(1);
$serial->confFlowControl("none");

----snip-------

All setups:
Log Viewer (logviewer.cgi)
Edit logviewer.cgi and set the path to your TLB log file.
----snip-------

$LOG = "/home/tlb/tlb.log"

----snip-------
Point you web browser to http://(server name and cgi-bin dir path)/nodemgmt.cgi

What all the commands do (Help):

You'll see a colour-coded list of station call signs and a row of control buttons corresponding to each station. When you click on a control button then and click the "Enter" button, your command will take effect immediately. 
You can also connect more stations to the conference, or send and received text messages using this panel. 
The status of your commands will be shown on the panel just above the station list.
Note: This panel was designed for a screen resolution of 1024x768. 
The Station List 
The call signs are highlighted with color to give you an indication of each station's status. Here are the details: 
    • Normal: Just a normal Echolink station, nothing special about it. It may be a repeater, an RF link or a user on a PC. 
    • Admin: The station is logged in to this conference server as an Administrator or a Sysop. 
    • Conf: The station is itself a conference, either a TBD server, like this one, or an Echolink station with multiple connections. 
    • Perm: A permanent connection is the result of an outbound connect request. If the station's connection times out, the conference will attempt to re-connect. 
    • Muted: The station is muted, it will hear any activity on the conference but is not able to transmit. 
    • Kicked: The station has been disconnected by the conference. 
    • Monitor: The station can transmit to the conference, but the conference will not transmit to the station. 
    • Lurking: The station invoked the lurk command to remove his call sign from the station lists on the Echolink clients, but is still connected and can participate in the conference as if it were a normal user. 
    • Talking: The station is currently transmitting to the conference. 
    • Playing: The station is playing a file; either listening to a bulletin or using the .test command to play back its own audio. If the conference is set up to play a "welcome"' echo "message to connecting stations, they'll show up in pink momentarily" just after they connect. 
What the Control Buttons do 
    • Disc: Disconnects a station from the conference. The station can re-connect back in if it wants to. 
    • Disc/Ban: Disconnects a station and bans it so it cannot re-connect. Bans can only be reversed by the conference 
    • Mute: Stops a station from transmitting to the conference. The station can disconnect and re-connect to un-mute itself. 
    • Mute-P: Mutes a station persistently, that is, the station will stay muted even if it disconnects and re-connects. 
    • Monitor: The opposite of "Mute". The conference will receive what the station transmits, but cannot talk back to that station. This is useful for monitoring nets and space shuttle missions. If a repeater station needs to disconnect, it will not disrupt the rest of the net. 
    • Reset: This function cancels the "Mute" and "Monitor" functions, and also de-lurks (un-hides) a station which is lurking (connected, but not appearing in the Echolink echo "clients' station lists)." echo "
    • About: Shows the station operator's information. 
    • QRZ: Performs a callsign lookup on the QRZ database. The QRZ information will pop up in a separate window. The conference administrator can disable QRZ lookups. 
Outbound Connections 
You may connect a station to the conference by typing the station's" call sign into the text field following "Connect a station:"' and clicking the "Enter" button. 
If the station does not immediately show up in the station list, it is either off-line or not accepting connections. 
Send a Text Message 
Whatever you type into this text field will be displayed in the text box of all connected Echolink clients' 
Received a Text Messages' 
Displays all the EchoLink text messages received by your station. It is refreshed automaticly even if the main page refresh is set to "None " . 
Change Location String 
You can modify the text shown next to the conference server's name on" the Echolink client. Your change will take effect until the conference server is restarted. 
Set/Change Conference Status: 
Busy - Puts your node status to busy so as to prevent in-bound connections
Available - Turns your node status to available and allows in-bound connections 
Radio Control: 
The radio control changes channels by using the control lines of a Motorola GM 300 radio
By pressing the numbered on buttons on the page you switch on the relays of the K190 to select the channel number required
By pressing the Radio off button on the page you switch off all the relays of the K190
There is also a status under the buttons with reads the currant status from the K190 
Refresh Interval 
For your convenience, the panel may be configured to refresh itself "at certain time intervals, so you'll always have an up-to-date status" display. Any commands or messages that you issue will reset the automatic refresh interval back to "None" (which is the default when you first load the utility). 
To change the refresh interval, click the radio button corresponding to your desired rate (for example, every 30 seconds) and click the "Set / Refresh" button. 
You may click the "Set / Refresh" any time to refresh the information in the panel, even when automatic refresh is disabled (set to "None"). 
Radio Channel Data: 
Opens a Radio channel data file in a new tab of your browser You need to edit this file and save it using any word proccessing program. Most surpport html editing in some form or another 
Node Log book: 
Opens the node log book in a new tab of your browser using the logviewer.cgi 

Acknowlgements
This Web interface uses modified code from the following sources
KC4YOZ's Conference interface CGI (usermngmt.cgi)
Distributed under the terms of the
GNU General Public License

Most Simple Ajax Chat Script - (chris[at]linuxuser.at) 
Distributed under the terms of the
GNU General Public License

sendEmail - Brandon Zehm <caspian[at]dotconf.net>
Distributed under the terms of the
GNU General Public License

php serial by Rémy Sanchez <thenux[at]gmail.com>
Distributed under the terms of the
GNU General Public License

Copyright (C) 2010 Robert VK5TRM email: vk5trm[at]gmail.com
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details at http://www.gnu.org/licenses/


