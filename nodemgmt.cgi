#!/bin/bash
#-------------------------------------------------------------------
#  TheBridge Echolink Conference Server User Management Utility 
#
#  2006/12/26 KC4YOZ - Original, ported to BASH from REXX.
#  2006/12/27 KDJ    - HELP Panel, cosmetics.
#  2006/12/31 KDJ    - Implement "Send a text message".
#  2007/01/02 KDJ      Implement QRZ lookups.
#                      Neater control buttons for Mozilla 5+
#  2007/02/01 KDJ    - Support for Location/Info string changes..
#  2010/06/30 VK5TRM - Added RX text support for Echolink
#  2010/07/22 VK5TRM - Added text box sysop email using format **(call)**
#  2010/08/08 VK5TRM - Added support for pic based temperature sensors
#  2012/1/02  VK5TRM - Added node status changeover
#  2013/10/08 VK5TRM - Added Radio control
#  2014/02/17 VK5TRM - Major re-write of radio control section
#  2014/02/19 VK5TRM - Added current status and current location string,tidyed up panel
#-------------------------------------------------------------------
#  Installation Default Settings
confname=VK5TRM-L             # name of this conference must be in Upper Case
admin=VK5TRM                  # admin's callsign must be in Upper Case
qrz=yes                          # leave blank to disable QRZ lookups
chginfo=yes                   # enable/disable Info/Location changes
tbdcmd=/usr/local/bin/tlbcmd  # path to "tbdcmd or tlbcmd" executable
tlbchat=/usr/local/bin/tlbchat # path to "tlbchat" executable
commport=/dev/ttyS1         # Comm Port for Temperature sensor & Radio control
#-------------------------------------------------------------------
#PATH=/var/www/cgi-bin/
echo 'Content-type: text/html'
echo ''
if [ "$QUERY_STRING" != "help" ]; then

#  Refresh Interval stuff..
 
  if [[ $QUERY_STRING == refresh=* ]]; then
#    Get the value, check the right button..
    IFS=$'='
    for rfp in $QUERY_STRING ; do rfin[r++]=$rfp ; done
    rftime=${rfin[1]}
    case $rftime in
      0)
        chk0=checked
        chk10=
        chk30=
        chk60=
        chk300=
        chk900=
        chk1800=
      ;;
      10)
        chk0=
        chk10=checked
        chk30=
        chk60=
        chk300=
        chk900=
        chk1800=
      ;;
      30)
        chk0=
        chk10=
        chk30=checked
        chk60=
        chk300=
        chk900=
        chk1800=
      ;;
      60)
        chk0=
        chk10=
        chk30=
        chk60=checked
        chk300=
        chk900=
        chk1800=
      ;;
      300)
        chk0=
        chk10=
        chk30=
        chk60=
        chk300=checked
        chk900=
        chk1800=
      ;;
      900)
        chk0=
        chk10=
        chk30=
        chk60=
        chk300=
        chk900=checked
        chk1800=
      ;;
      1800)
        chk0=
        chk10=
        chk30=
        chk60=
        chk300=
        chk900=
        chk1800=checked
      ;;
    esac
    IFS=$' \t\n'
  else    #  first time in, set default value and button..
    chk0=checked
    rftime=0
  fi

  echo '<html><head>'
  echo '<title>'$confname' Node Management</title>'
  echo '<!-- input parm ['$QUERY_STRING'] -->'
  if [ $rftime != 0 ]; then
    echo '<META HTTP-EQUIV="refresh"'
    echo ' content="'$rftime'; url=nodemgmt.cgi?refresh='$rftime'">'
  fi
  echo '</head><BODY LANG="en-AU" BACKGROUND="'$REFERRER'/fuzzy-lightgrey.jpg" DIR="LTR">'
  echo '<TABLE WIDTH=100% BORDER=0 CELLPADDING=0 CELLSPACING=0">'
  echo '	<TD WIDTH=30%>'
  echo '<P>'$(date "+%A %d/%m/%Y %T %Z")'</P></TD>'
  echo '<TD WIDTH=50%><P>'
  echo '<TD WIDTH=20%>'
  if [ $commport != " " ];then
  stty -F $commport raw ispeed 9600 ospeed 9600 cs8 -ignpar -cstopb eol 255 eof 255
  /bin/echo t1 > $commport
  read -r -n 10 -t 2 OneByte < $commport
  InStr=$InStr$OneByte
  fi
  if [ $InStr != "" ];then
  echo '<P>Node Temperature<BR>'  
  echo ' '$InStr' Degrees C</TR>'
  fi
  echo '</TABLE><br>'
  echo '<center><FONT FACE="Albany, sans-serif"><FONT SIZE=7 STYLE="font-size: 33pt"> '$confname' Node Management</FONT>'

#  Execute a command...

  if [ "$QUERY_STRING" != "" ]; then   #  we have a command...
    user=$(echo ${REMOTE_USER} |tr 'a-z' 'A-Z')
      if [ "$user" != "" ]; then

      if [[ $QUERY_STRING == infotxt=* ]]; then  

#  Console text message or "Info" string changes...
      IFS=$'='            #  separate out the message text..
      for tmsg in $QUERY_STRING ; do tmss[h++]=$tmsg ; done
      instr=${tmss[1]}    #  input string..
      outstr=             #  output string..
      len=${#instr}       #  length of input..
      i=0                 #  byte pointer..
      while [ $i -lt $len ]; do {       #  now examine each byte..
        thischar=${instr:$i:1}
        if [ $thischar == % ]; then     #  hex junk from the URI..
          xbyte=${instr:$i+1:2}             #  grab the byte..
          tword=$(echo "\x"$(echo $xbyte))  #  prefix it..
          abyte=$(echo -e "$tword")         #  translate to ASCII..
          outstr=$(echo $outstr$abyte)      #  append the buffer..
          i=$(($i+3))                       #  bump the pointer..
        else
          if [ $thischar == + ]; then   #  plus is really a space..
            outstr=$(echo $outstr' ')
          else                          #  just take the character..
            outstr=$(echo $outstr$thischar)
          fi
          i=$(($i+1))
        fi
        };
      done
          statusmsg=$($tbdcmd -s info $outstr)
else
      if [[ $QUERY_STRING == connect* ]]; then      # connect a station...
        IFS=$'='
        for tcmd in $QUERY_STRING ; do tcmd[h++]=$tcmd ; done
        if [ "${tcmd[1]}" != "" ]; then 
          statusmsg=$($tbdcmd -s connect ${tcmd[1]})       
        fi
else
       if [[ $QUERY_STRING == busy* ]]; then      # change node status...
        IFS=$'='
        for tcmd in $QUERY_STRING ; do tcmd[h++]=$tcmd ; done
        if [ "${tcmd[1]}" != "" ]; then
        statusmsg=$($tbdcmd busy ${tcmd[1]})
        fi
         
        else
 
        IFS=$'z'     # commands against a station in the list...
        for tcmd in $QUERY_STRING ; do tcmd[h++]=$tcmd ; done
        g=0
        while [ $g -lt $h ]; do {
          if [[ ${tcmd[g]} == =.* ]]; then  # --> separator
            statm=
            f=$(($g+1))  # --> command
            e=$(($g+2))  # --> callsign
            case ${tcmd[$f]} in
              mu)  # Mute
                statm=$($tbdcmd -s mute ${tcmd[$e]})
              ;;
              dc)  # Disconnect
                statm=$($tbdcmd -s disconnect ${tcmd[$e]})
              ;;
              db)  # Ban
                stata=$($tbdcmd -s disconnect ${tcmd[$e]})
                statb=$($tbdcmd -s ban add ${tcmd[$e]})
                statm=$(echo $stata$statb)
              ;;
              mp)  # Mute Persist
                statm=$($tbdcmd -s "mute -p ${tcmd[$e]}")
              ;;
              mo)  # Monitor
                statm=$($tbdcmd -s monitor ${tcmd[$e]})
              ;;
              um)  # Reset
                $tbdcmd -s delurk ${tcmd[$e]} >/dev/null
                stat1=$(echo ${tcmd[$e]}' de-lurked')
                stat2=$($tbdcmd -s monitor disable ${tcmd[$e]})
                stat3=$($tbdcmd -s unmute ${tcmd[$e]})
                $tbdcmd -s "unmute -p ${tcmd[$e]}" >/dev/null
                statm=$(echo $stat1$stat2$stat3)
              ;;
              qr)  # QRZ Lookup
                if [ "$qrz" != "" ]; then
                  callsign=${tcmd[$e]}
                  if [[ "${callsign:0:1}" == "*" ]]; then
                    statm=$(echo $callsign' cannot be looked up on QRZ.')
                  else
                    if [[ $callsign == *-* ]]; then
                      IFS=$'-'
                      for this in $callsign ; do tcall[a++]=$this ; done
                      qrzpop=${tcall[0]}
                    else
                      qrzpop=${tcmd[$e]}
                    fi
                    statm=$(echo 'QRZ query issued for '$qrzpop)
                  fi
                fi
              ;;
            esac
            statusmsg=$(echo $statusmsg$statm)
          fi
          g=$(($g+1))
        };
        done
       fi
      fi
      IFS=$' \t\n'
     fi
  fi
fi
#  Status text goes here...

  if [ "$statusmsg" == "" ]; then 
     echo '<p><br>'
    fi
   else
    echo '<p>'$statusmsg
 fi
 
#  QRZ PopUp Call..

  if [ "$qrz" != "" ]; then
    if [ "$qrzpop" != "" ]; then
      echo '<script type="text/javascript">'
      echo '<!--'
      echo 'window.open("http://www.qrz.com/db/'$qrzpop'","QRZ",'
      echo '"toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes,width=800,height=600");'
      echo '//-->'
      echo '</script>'
    fi
  fi

#  Get and format the list of connected stations...
 if ps ax | grep -v grep | grep tlb > /dev/null
 then
     var1=$($tbdcmd -s users)
 else
 exit
 fi
   for this in $var1 ; do tbdu[i++]=$this ; done
  if [ $i == 1 ]; then  # no users, just a return code.
    echo '<p><br>'
  else  # got at least one.. make the table..
    echo '<form name="form">'
    echo 'Color Code: Normal '
    echo '/ <font color=blue>Conf</font> / <font color=green>Perm</font> '
    echo '/ <font color=brown>Muted</font> / <font color=gray>Kicked</font> '
    echo '/ <font color=purple>Monitor</font> / <font color=red>Talking</font>'
    echo '<table border="2" cellspacing="0"><tr><td align="center">Callsign</td>'
    echo '<td align="center">Command Options</td></tr>'

    j=1  # bump past the return code..
    while [ $j -lt $i ]; do {
      clr=black
      RFstn=NO ; lurker=NO  ; admin=NO  ; perm=NO    ; conf=NO 
      muted=NO ; talking=NO ; kicked=NO ; monitor=NO ; irlp=NO

      if [[ ${tbdu[j]} == *[0-9]. ]]; then  # --> user number
        k=$(($j+1))  # --> callsign
        l=$(($j+2))  # --> user flags
        if [[ ${tbdu[l]} == *C* ]]||[[ ${tbdu[l]} == *B* ]]; then   # Conference
          clr=blue
        fi
        if [[ ${tbdu[l]} == *P* ]]; then   # Permanent
          clr=green
        fi
        if [[ ${tbdu[l]} == *M* ]]||[[ ${tbdu[l]} == *m* ]]; then   # Muted
          clr=brown
        fi
        if [[ ${tbdu[l]} == *K* ]]; then   # Kicked
          clr=gray ; kicked=YES
        fi
        if [[ ${tbdu[l]} == *R* ]]; then   # Monitor
          clr=purple
        fi
        if [[ ${tbdu[l]} == *T* ]]; then   # Talking
          clr=red
        fi
        echo '<tr><td align="center"><font color='$clr'><b>'${tbdu[k]}'</b>'
        echo '</font></td><td align="center">'
        if [[ $kicked == NO ]]; then  # format the radio buttons..
          if [[ $HTTP_USER_AGENT == Mozilla/5* ]]; then
#  Firefox can handle Action Buttons...
            tdc='<td align="center"><button type="submit" name="'
            tdd='</button></td>'
          else
#  IE and Netscrape cannot..
            tdc='<td align="center"><input type=radio name="'
            tdd='</td>'
          fi
          echo '<table border="1" cellspacing="0"><tr>'
          echo $tdc'zdcz'${tbdu[k]}'z" value=.> Disc '$tdd
          echo $tdc'zdbz'${tbdu[k]}'z" value=.> Disc/Ban '$tdd
          echo $tdc'zmuz'${tbdu[k]}'z" value=.> Mute '$tdd
          echo $tdc'zmpz'${tbdu[k]}'z" value=.> Mute-P '$tdd
          echo $tdc'zmoz'${tbdu[k]}'z" value=.> Monitor '$tdd
          echo $tdc'zumz'${tbdu[k]}'z" value=.> Reset '$tdd
          if [ "$qrz" != "" ]; then
            echo $tdc'zqrz'${tbdu[k]}'z" value=.> QRZ '$tdd
          fi
          echo '</tr></table>'
        fi
      echo '</td></tr>'
      fi
      j=$(($j+1))
    };
    done
    echo '</table>'
#  Form Buttons...  for IE and Netscrape..

    if [[ $HTTP_USER_AGENT != Mozilla/5* ]]; then
      echo '<input type=reset value=" Clear ">'
      echo '<b><input type=submit value=" Enter "></b>'
    fi
    echo '</form>'
fi
#  Connect a station...
echo '<hr><TABLE WIDTH=843 BORDER=0 BORDERCOLOR="#000000" CELLPADDING=4 CELLSPACING=0>'
echo '	<COL WIDTH=300>'
echo '	<COL WIDTH=500>'
echo '	<TR VALIGN=TOP>'
echo '		<TD WIDTH=300><p><b>Connect a station:</b><br></p></td>'
  echo '<TD WIDTH=500>'
    echo '<form><input type=text size=10 name=connect>'
  echo '<input type=reset value=" Clear ">'
  echo '<b><input type=submit value=" Enter "></b>'
   echo '</form></td></table>'
#  Text Message..
echo '<hr><TABLE WIDTH=843 BORDER=0 BORDERCOLOR="#000000" CELLPADDING=4 CELLSPACING=0>'
echo '	<COL WIDTH=200>'
echo '	<COL WIDTH=600>'
echo '	<TR VALIGN=TOP>'
echo '		<TD WIDTH=200>'
echo '			<P><b>Recieved Text messages: </b><BR>'
echo '			</P>'
echo '		</TD>'
echo '		<TD WIDTH=600>'
echo '	<P> <iframe src="chat.html" name="RX chat" scrolling="no" frameborder="no" align="center"height = "400" width = "600px">'
echo '</iframe><BR></P>	</TD></TR>'
echo '	<TR VALIGN=TOP>'
echo '		<TD WIDTH=200>'
echo '			<P><form><p><b>Send a text message: </b><BR>'
echo '			</P></TD>'
echo '		<TD WIDTH=800>'
echo '	<P> <P> <iframe src="chat.cgi" name="TX chat" scrolling="no" frameborder="no" align="center"  height = "70" width = "800px">'
echo '</iframe><BR></P></TD></TR>'
echo '</TABLE>'

#  "Info" String..

  if [ $chginfo == yes ]; then 
    echo '<hr><TABLE WIDTH=843 BORDER=0 BORDERCOLOR="#000000" CELLPADDING=4 CELLSPACING=0>'
echo '	<COL WIDTH=300>'
echo '	<COL WIDTH=500>'
echo '	<TR VALIGN=TOP>'
echo '		<TD WIDTH=300><p><b>Change Location String: </b><br></p></td>'
echo '		<TD WIDTH=500>'
    echo '<form><input type=text size=26 name=infotxt>'
    echo '<input type=reset value=" Clear ">'
    echo '<b><input type=submit value=" Enter "></b>'
    echo '</form></td></table>'
    info=`($tbdcmd -s info) | grep "location" `
  echo '<p><b>'$info'</p></b></td>'
  fi
  # " Busy" Status..
 echo '<hr><TABLE WIDTH=843 BORDER=0 BORDERCOLOR="#000000" CELLPADDING=4 CELLSPACING=0>'
echo '	<COL WIDTH=300>'
echo '	<COL WIDTH=500>'
echo '	<TR VALIGN=TOP>'
echo '		<TD WIDTH=300><p><b>Change Conference Status:</b><br></p></td>'
echo '		<TD WIDTH=500>'
echo '   <form action="nodemgmt.cgi" method="get">'
echo '                                <INPUT TYPE=HIDDEN NAME="busy" value="on">'
echo '                                <input type="submit" value="Busy">'
echo '                                </form>'
echo '   <form action="nodemgmt.cgi" method="get">'
echo '                                <INPUT TYPE=HIDDEN NAME="busy" value="off">'
echo '                                <input type="submit" value="Available">'
echo '                                </form></table>'
 bs=`($tbdcmd -s busy) | grep "conference" `
  echo '<br><center><b>Current Busy Status: '$bs'</b></center>'
# Radio control
 if [ $InStr != "" ]; then
echo '<hr><center><TABLE WIDTH=843 BORDER=0 BORDERCOLOR="#000000" CELLPADDING=4 CELLSPACING=0>'
echo '  <COL WIDTH=150>'
echo '  <COL WIDTH=700>'
echo '  <TR VALIGN=TOP>'
echo '          <TD WIDTH=150>'
echo '                  <P><b>Radio Control: </b><BR>'
echo '                  </P>'
echo '          </TD>'
echo '          <TD WIDTH=700>'
echo '  <P> <iframe src="radiocontrol.php" name="Radiocontrol" scrolling="no" frameborder="no" align="center"height = "275" width ="600px">'
echo '</iframe></center><BR></P> </TD></TR>'
echo '</TABLE>'
   fi
#  Refresh Interval

  echo '<hr><form><center><table><tr><td><b>Refresh Interval:</b>'
  echo '<td><table border="2" cellspacing="4"><tr>'
  echo '<td><input type=radio name=refresh value=0 '$chk0'>None</td>'
  echo '<td><input type=radio name=refresh value=10 '$chk10'>10 sec</td>'
  echo '<td><input type=radio name=refresh value=30 '$chk30'>30 sec</td>'
  echo '<td><input type=radio name=refresh value=60 '$chk60'>1 min</td>'
  echo '<td><input type=radio name=refresh value=300 '$chk300'>5 min</td>'
  echo '<td><input type=radio name=refresh value=900 '$chk900'>15 min</td>'
  echo '<td><input type=radio name=refresh value=1800 '$chk1800'>30 min</td>'
  echo '</table><td><input type=submit value=" Set / Refresh ">'
  echo '</table></form></center>'
  
   echo '<HR><center><table border="0" CELLPADDING=4 cellspacing="5"><tr>'
  if [ $InStr != "" ]; then
  echo '<td align="center">'
  curl=channeldata.html 
  wop=toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes,width=500,height=500
  if [[ $HTTP_USER_AGENT == Mozilla/5* ]]; then
  #  Firefox can handle Action Buttons... 
  echo '<form><input type=button value=" Radio Control Channel Data"'
  echo 'onClick=window.open("'$curl'","'$wop'")></form>'
      else
#  IE and Netscrape cannot..
echo '<a href="'$curl'"target="_blank">Radio Control Channel Data</a>.'
  fi
  echo '</td>'
fi
  echo '<td align="center">'
  lurl=logviewer.cgi  
   wop=toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes,width=500,height=500
   if [[ $HTTP_USER_AGENT == Mozilla/5* ]]; then
  #  Firefox can handle Action Buttons...  
  echo '<form><input type=button value=" Node Log Book "'
   echo 'onClick=window.open("'$lurl'","'$wop'")></form>'
   else
#  IE and Netscrape cannot..
echo '<a href="'$lurl'"target="_blank">Node Log Book</a>.'
    echo '</td>'
    fi
    echo '<td align="center"><center>'
 hurl=README.html
  wop=toolbar=no,location=no,status=no,resizable=yes,scrollbars=yes,width=500,height=500
   if [[ $HTTP_USER_AGENT == Mozilla/5* ]]; then
  #  Firefox can handle Action Buttons... 
  echo '<form><input type=button value=" Help file "'
  echo 'onClick=window.open("'$hurl'","'$wop'")>' 
   else
#  IE and Netscrape cannot..
echo '<a href="'$hurl'"target="_blank">Help File</a>.'
  fi
  echo '</form></td></center></table>'
  
 
echo '<font size="-1">&copy;2006, 2007 <i>Crafted by KC4YOZ</i><br>'
echo '<font size="-1">Modified 2010, 2012, 2013 2014 <i>by Rob, VK5TRM</i><br>'
echo 'Distributed under the terms of the'
echo '<a href="http://www.gnu.org/licenses/gpl.html">GNU General Public License</a>.'
echo '</font><tr></center>'

#  Debug only...
#echo '<pre>'
#set
#echo '</pre>'

echo '</body></html>'
exit 0
