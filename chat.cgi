#!/bin/bash
#-------------------------------------------------------------------
#  Installation Default Settings
confname=VK5TRM-L             # name of this conference (ex *LINUX*)
tbdcmd=/usr/local/bin/tlbcmd  # path to "tbdcmd or tlbcmd" executable
#-------------------------------------------------------------------
echo 'Content-type: text/html'
echo ''
  echo '<html><head>'
  echo '<title>'$confname' Node Management</title>'
  echo '<!-- input parm ['$QUERY_STRING'] -->'
    echo '</head><BODY LANG="en-AU" BACKGROUND="fuzzy-lightgrey.jpg" DIR="LTR">'

#  Console text message 
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
      if [[ $QUERY_STRING == msgtxt=* ]]; then
          user=$(echo ${REMOTE_USER} |tr 'a-z' 'A-Z')
          if [ "$user" != "" ]; then
                 prefix=$(echo $user">")
             statusmsg=$($tbdcmd -s message $prefix$outstr)
         
     fi
         fi
#  Text Message..
echo '	<P><form><P> <input type=text size=70 name=msgtxt><input type=reset value=" Clear ">'
echo '<b><input type=submit value=" Enter "></b>'
echo '</form><BR></P>'
echo '</body></html>'
exit 0
