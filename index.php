<html>
<head>

  <meta name="viewport" content="width=device-width">
<!-- Start of  Zendesk Widget script -->
<script id="ze-snippet" src="https://static.zdassets.com/ekr/snippet.js?key=a0595545-82d1-4095-9f0c-bd28246d8227"> </script>
<!-- End of  Zendesk Widget script -->

<script src="https://cdn.firebase.com/js/client/2.4.2/firebase.js"></script>
<script src="jquery.js"></script>
<script src="jquery-csv.js"></script>
<script type="text/javascript" src=tagup.js></script>
<script> 
window.onload = function ()
{
	Tagup.initialize("https://tagupexits2-710aa.firebaseio.com/", "http://tagfame.com/startupmap.rev25-normal.png", document.getElementsByTagName("body")[0]);
}
</script>


<link rel="stylesheet" type="text/css" href='tagup.css'/>
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
</head>
<title>tagfame.com</title>
<body>
<img src='tagframe-logo.jpg'><br>
<h2><a href="http://tagfame.com">http://tagfame.com</a></h2>
<?php

$tags = file_get_contents('./tags.txt', true);
$letters = file_get_contents('./letters.txt', true);
print "<h2>Total tags: $tags Total letters: $letters</h2>";
function stringEndsWith($haystack,$needle,$case=true) {
    $expectedPosition = strlen($haystack) - strlen($needle);
    if ($case){
        return strrpos($haystack, $needle, 0) === $expectedPosition;
    }
    return strripos($haystack, $needle, 0) === $expectedPosition;
}
$sum= "";
$csvfiles="";
$exec_entry="";
if ($handle = opendir('uploads/')) {
    print "<form action='http://tagfame.com:8080/change' method='post' enctype='multipart/form-data'>";
    print "<label for='changefiles'>Choose a file:</label><select name='changefile' id='changefile'>";
    while (false !== ($entry = readdir($handle))) {

        if ($entry != "." && $entry != "..") {

            $onecsvfile="";
            if (stringEndsWith($entry, '.csv')) {
                 $onecsvfile .= $entry;
                 $csvfiles .="$onecsvfile";

            $sum= "$sum" . "$entry\n";
            if ("$entry" == "$changefile") {
                $exec_entry = "$entry";
            }
                //$exec_entry .= "$changefile";
            print "<option value='" . $entry . "'";
            if ("$entry" == "$changefile") {
                print " selected ";
            }            
            print ">$entry</option>";
            }
        }
    }

    closedir($handle);
    print "</select>";
    print "<input type='image' name='submit' src='send-bt.jpg' border='0' alt='Submit' style='width: 50px;' />";
    print "<input type='image' name='submit' src='skip-bt.jpg' border='0' alt='Submit' style='width: 50px;' />";
    print "</form>";
}
?>
<div class="tagup" tagupimagehref="http://tagfame.com/startupmap.rev25-normal.png"></div>
<form action="http://tagfame.com:8080/upload" method="post" enctype="multipart/form-data">
  <input id="fileupload" type="file" name="file">
  <input type="submit" value="Upload">
</form>
<span style="vertical-align:top">Embed:</span><textarea style="height: 200px; width: 700px;" class="test-input">
  <!--
one beer excel refactoring: 1. embed code on yourwebsite.com 2.send us mail with an excel document or csv document exported to post@sanderm.no 3. The excel document will be visible on the yourwebsite.com url after we have altered the column names to fit our system so you can have a one week focus on a spesific document in your organisatio, becouse you can upload documents yourself here after we've polished the document right.
-->
  <html>
  <head>
  <script src="https://cdn.firebase.com/js/client/2.4.2/firebase.js"></script>
  <script src="https://tagstartups.com/jquery.js"></script>
  <script src="https://tagstartups.com/jquery-csv.js"></script>
  <script type="text/javascript" src=https://tagstartups.com/tagup.js></script>
  <script>
  window.onload = function ()
  {
	  Tagup.initialize("https://tagupexits2-710aa.firebaseio.com/", "https://tagfame.com/startupmap.rev25-normal.png", document.getElementsByTagName("body")[0]);
  }
  </script>
  <link rel="stylesheet" type="text/css" href='https://tagfame.com/tagup.css'/>
  <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
  </head>
  <title>Tagup demo</title>
  <body>
  <form action="http://tagfame.com:8080/upload" method="post" enctype="multipart/form-data">
  <input id="fileupload" type="file" name="file">
  <input type="submit" value="Upload">
  </form>
  </body>
  </html>
</textarea>
</body>

</html>
