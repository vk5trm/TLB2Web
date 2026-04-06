<?php


/*
Utilizes the PHP Serial class by Rémy Sanchez <thenux@gmail.com> (Thanks you rule!!)
to communicate with the QK108/CK1610 serial relay board!

*/

function microtime_float()
{
	list($usec, $sec) = explode(" ", microtime());
	return ((float)$usec + (float)$sec);
}

{
	//Load the serial port class
	require("php_serial.class.php");
	
	//Initialize the class
	$serial = new phpSerial();

	//Specify the serial port to use... in this case COM1
	$serial->deviceSet("/dev/ttyS1");
	
	//Set the serial port parameters. The documentation says 9600 8-N-1, so
	$serial->confBaudRate(9600); //Baud rate: 9600
	$serial->confParity("none");  //Parity (this is the "N" in "8-N-1")
	$serial->confCharacterLength(8); //Character length (this is the "8" in "8-N-1")
	$serial->confStopBits(1);  //Stop bits (this is the "1" in "8-N-1")
	$serial->confFlowControl("none"); //Device does not support flow control of any kind, so set it to none.

	//Now we "open" the serial port so we can write to it
       $serial->deviceOpen();
//check the GET action var to see if an action is to be performed
if (isset($_GET['action']))
if (isset($_SERVER['PHP_AUTH_USER']))
	{
	$command = htmlspecialchars($_GET['action']);
		$serial->sendMessage(f0);
		$commandx= explode (" ",$command);
		//to turn relay on, we issue the command 
		if ($commandx[3]== "1") $serial->sendMessage(n1);
		if ($commandx[2]== "1") $serial->sendMessage(n2);
		if ($commandx[1]== "1") $serial->sendMessage(n3);
		if ($commandx[0]== "1") $serial->sendMessage(n4);
 }
	//We're done, so close the serial port again
	$serial->deviceClose();

}
        //Initialize the class
        $serial = new phpSerial();

        //Specify the serial port to use... in this case COM1
        $serial->deviceSet("/dev/ttyS1");

        //Set the serial port parameters. The documentation says 9600 8-N-1, so
        $serial->confBaudRate(9600); //Baud rate: 9600
        $serial->confParity("none");  //Parity (this is the "N" in "8-N-1")
        $serial->confCharacterLength(8); //Character length (this is the "8" in "8-N-1")
        $serial->confStopBits(1);  //Stop bits (this is the "1" in "8-N-1")
        $serial->confFlowControl("none"); //Device does not support flow control of any kind, so set it to none.

        //Now we "open" the serial port so we can write to it

  $serial->deviceOpen();
// To write into
$serial->sendMessage("s0");
// Or to read from
$read1 = '';
$theResult1 = '';
$start = microtime_float();

while ( ($read1 == '') && (microtime_float() <= $start + 0.5) ) {
        $read1 = $serial->readPort();
        if ($read1 != '') {
                $theResult1 .= $read1;
                $read1 = '';
                $result1 = substr ($theResult1, 2, 5);
                $resultt1 = hexdec ($result1);
                if ($resultt1=="0")$status = "switched off";
                else ($status = "on channel $resultt1");
         } else 
                                  
       $serial->deviceClose();
}
?><!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>GM300 Radio Controller</title>
</head>
<body>
<body BACKGROUND='fuzzy-lightgrey.jpg'><div id='newrequestbox'>
<center><TABLE BORDER=0 CELLSPACING=15>
		<TR>
			<TD>
				<form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 0 0 1">
				<input type="submit" value="Channel 1">
				</form>
				<P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 0 1 0">
                                <input type="submit" value="Channel 2">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 0 1 1">
                                <input type="submit" value="Channel 3">
                                </form>

			</TD>
			<TD>
				<form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 1 0 0">
                                <input type="submit" value="Channel 4">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 1 0 1">
                                <input type="submit" value="Channel 5">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 1 1 0">
                                <input type="submit" value="Channel 6">
                                </form>

			</TD>
			<TD>
			 	<form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="0 1 1 1">
                                <input type="submit" value="Channel 7">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 0 0 0">
                                <input type="submit" value="Channel 8">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 0 0 1">
                                <input type="submit" value="Channel 9">
                                </form>

			</TD>
			<TD>
			 	<form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 0 1 0">
                                <input type="submit" value="Channel 10">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 0 1 1">
                                <input type="submit" value="Channel 11">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 1 0 0">
                                <input type="submit" value="Channel 12">
                                </form>

			</TD>
                         <TD>
         		 	<form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 1 0 1 ">
                                <input type="submit" value="Channel 13">
                                </form>
                                <P><form action="radiocontrol.php" method="get">
                                <INPUT TYPE=HIDDEN NAME="action" value="1 1 1 0">
                                <input type="submit" value="Channel 14">
                                </form>
                                <P><form action="radiocontrol.php" method="get"> 
                                <INPUT TYPE=HIDDEN NAME="action" value="1 1 1 1">
                                <input type="submit" value="Channel 15">
                                </form>

                       </TD>                      
</TABLE>
                         <P><center><form action="radiocontrol.php" method="get"> 
                                <INPUT TYPE=HIDDEN NAME="action" value="0 0 0 0">
                                <input type="submit" value="Radio Off">
                                </form> 
<center><h3>The radio is currently<?=" $status" ?></CENTER></h3>
</BODY>
</html>
