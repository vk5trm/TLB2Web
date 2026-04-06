#!/usr/bin/perl

#################################################################### 
#
#	Log Viewer
#	©2000, PerlScriptsJavaScripts.com
#
#	Requires: Perl5+
#	Created:  December, 2001
#	Updated:  June, 2003
#	Author:   John Krinelos
#	Contact:  john@perlscriptsjavascripts.com
#	Version:  1.1
#
#	http://www.perlscriptsjavascripts.com/copyright_fees.html
#
#################################################################### 

# Log File Path:
# Set this variable to the absolute path to your server's
# WINDOWS Servers should use two backslashes to seperate 
# folders. Eg. $LOG = "logs\\access";
$LOG = "/home/tlb/tlb.log";

# default starting line number, leave as 0 to view last 50 lines by default
$start = 0;
# default ending line number, leave as 0 to view last 50 lines by default
$end   = 0;
# default wrap 1 = no wrap  2 = wrap
$wrap  = 2;
 
#################################################################### 
#
#    THERE IS NO NEED TO EDIT ANYTHING ELSE
#
#################################################################### 

$ScriptURL = "http://$ENV{'SERVER_NAME'}$ENV{'SCRIPT_NAME'}";
$FONT  = qq~<font face="arial,verdana,helvetica" size="2">~;

&Parse;

$FORM{file}  ||= $LOG;

@contents = getfile($FORM{file});

$numlines = @contents;

if($FORM{start} eq '0'){$FORM{start} = 1; $minus = 1;}

$FORM{start} ||= $start;
$FORM{end}   ||= $end;

$FORM{wrap}  ||= $wrap;

$FORM{start}   =~ s/\D//ig;
$FORM{start} ||= $numlines - 50;
$FORM{start}   = $FORM{start} < 0 ? 0 : $FORM{start};
$FORM{start}   = $FORM{start} > $numlines ? $numlines - 50 : $FORM{start};
if($minus){$FORM{start} -= 1;}

$FORM{end}     =~ s/\D//ig;
$FORM{end}   ||= $numlines;
$FORM{end}     = $FORM{end} > $numlines ? $numlines : $FORM{end};
if($minus){$FORM{end} -= 1;}

# is end greater than start?
if($FORM{start} > $FORM{end}){
	$FORM{end} = $FORM{start} + 50;
}

print "Content-type: text/html\n\n";
print qq~
<head>
<title>Log Viewer</title>
<style>
<!--
a{color:#000060;font-weight:bold;font-family:arial;text-decoration:underline;font-size:13px;}
a:hover{color:#0000c0;font-weight:bold;font-family:arial;text-decoration:none;font-size:13px;}
// -->
</style>
</head><BODY BACKGROUND="fuzzy-lightgrey.jpg" text="navy" link="navy" alink="navy" vlink="navy">
<P ALIGN=CENTER STYLE="margin-top: 0.42cm; page-break-after: avoid"><FONT FACE="Albany, sans-serif"><FONT SIZE=7 STYLE="font-size: 44pt">Log Viewer</FONT></FONT></P><BR>
<table border=0 width=100% cellpadding=3 cellspacing="0" style="border:white outset 2px;">
<tr bgcolor="#ffd000"><form action="$Scripturl" method="post">
<td>$FONT<b>$numlines lines in log.</b></font></td>
<td>$FONT<b>View lines</b></font>
<input type="text" name="start" value="$FORM{start}" size="5"> 
$FONT<b>to </b></font>
<input type="text" name="end" value="$FORM{end}" size="5">
$FONT<b> with
<select name="wrap">~;

if($FORM{wrap} == 2) {
	print qq~
	<option value="2" selected>Wrap On
	<option value="1">Wrap Off
	~;
} else {
	print qq~
	<option value="2">Wrap
	<option value="1" selected>No Wrap
	~;
}


if($FORM{wrap} == 1) {
	$WRAP = qq~nowrap~;
} else {
	$WRAP = qq~~;
}

print qq~</select> in <input type="Text" name="file" value="$FORM{file}">
<font style="font-size:13px;font-weight:bold;font-family:arial;"><input type="submit" value="View" style="font-size:13px;font-weight:bold;font-family:arial;cursor:hand;"></font></th>
</tr></form>
</table>
<br>
$FONT
~;

if($contents[0]){

	print qq~
	<table border=0 width=100% cellpadding=3 cellspacing="0">
	<tr><form action="$Scripturl" method="post">
	<td $WRAP>
	$FONT~;

	for($a = $FORM{start}; $a < $FORM{end}; $a++) {
		$contents[$a] =~ s/\+/ /ig;
		$contents[$a] =~ s/\%3A/\:/ig;
		$contents[$a] =~ s/\%26/\&/ig;
		$contents[$a] =~ s/\%3D/\=/ig;
		$contents[$a] =~ s/\%2C/\,/ig;
		$contents[$a] =~ s/\%3B/\;/ig;
		$contents[$a] =~ s/\%2B/\+/ig;
		$contents[$a] =~ s/\%25/\%/ig;
		$contents[$a] =~ s/\%3F/\?/ig;
		
		print qq~$contents[$a]<br>
		~;

		print qq~<hr>~;
	}
	
	$file_size  = (-s $LOG);
	$file_size  = $file_size / 1024;
	$file_size  = sprintf("%5.2f", $file_size);
	$file_size =~ s/\s+//ig;
	$file_size .= qq~kb~;
	1 while $file_size =~ s/(.*\d)(\d\d\d)/$1,$2/g;
	
	print qq~
	<br><br>
	<b>File size : $file_size</b> : <a href="javascript:scrollTo(0,0);"><b>Top</b></a>
	</td>
	</tr>
	</table>~;
	
} else {
	$OS = $^O;
	if($OS =~ /win/i) { $isWIN = 1; }
	else {$isUNIX = 1;}

    print qq~
	<font color="#FF0000"><b>
	<BR><BR>
	<B>Unable to open Log file!</B>
	<BR><BR>
	Is the path "$LOG" correct?
	<br><br> 
	</b></font>
	~;
	unless($isWIN){
		print qq~
		<font color="#FF0000"><b>
		Your Document Root is : $ENV{DOCUMENT_ROOT}
		<BR><BR>
		</b></font>
		~;
	}
}

print qq~
</font><br>

<table border=0 width=100% cellpadding=3 cellspacing="0" style="border:white outset 2px;">
<tr bgcolor="#ffd000">
<th></th>
</tr>
</table>
</body>
</html>
~;

#################################################################### 

#################################################################### 

sub Parse {
	my($name, $value, $buffer, $pair, $hold, @pairs);
	
	if($ENV{'REQUEST_METHOD'} eq 'GET') {
		@pairs = split(/&/, $ENV{'QUERY_STRING'});
	} else {
		read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
		@pairs = split(/&/, $buffer);
	}
	
	foreach $pair (@pairs) {
		($name, $value) = split(/=/, $pair);
		$name =~ tr/+/ /;
		$name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$name =~ s/\n//g;
		$name =~ s/\r//g;
		unless($name eq 'content' || $name eq 'headerdata' || $name eq 'footerdata') {
			$value =~ s/\n//g;
			$value =~ s/\</&lt;/g;
			$value =~ s/\|//g;
		}
		$value =~ s/\r//g;

		$value =~ s/system\(/system\&#40;/g;
		$value =~ s/grep//g;
		
		$name =~ s/^\s-\w.+//g;
		$name =~ s/system\(.+//g;
		$name =~ s/grep//g;
		$name =~ s/\.\.\///g;
		$FORM{$name} = $value;
	}
	undef @parse_excludes;
	undef %parse_exclude;
}

#################################################################### 

#################################################################### 

sub Date {
	($second, $minute, $hour, $DAYOFMONTH, $MONTH, $year, $weekday, $dayofyear, $isDST) = 
	localtime($offset);
	
	$THISYEAR = $year + 1900;
}

#################################################################### 

#################################################################### 

sub getfile {
	my ($gf_path, $exists, @gf_contents);
	my $z;
	$gf_path = $_[0];
	
	if(open(GET, "<$gf_path")) {
		flock(GET, '2');
		@gf_contents = <GET>;
		close(GET);
		for($z = 0; $z < $#gf_contents; $z++){
			if(length($gf_contents[$z]) > 1){
				chop($gf_contents[$z]);
			}	
		}
		
		foreach (@gf_contents){
			if($_ ne ""){
				$exists = 1; last;
			}
		}
			
		if($exists){
	    	chomp(@gf_contents);
			return(@gf_contents);
		} 
	}
	undef $gf_path;
	undef $exists; 
	undef @gf_contents;
}
