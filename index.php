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
	Tagup.initialize("https://tagupexits2-710aa.firebaseio.com/", "http://rockefellerthrust.com/startupmap.rev25-normal.png", document.getElementsByTagName("body")[0]);
}
</script>


<link rel="stylesheet" type="text/css" href='tagup.css'/>
<link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
</head>
<title>rockefellerthrust.com</title>
<body>
<img src='tagframe-logo.jpg'> Partner:<img width=100 src='stortinget.png'> We are also proud to follow GDPR and DMCA becouse we use firebase storage<br>
<h2><a href="http://rockefellerthrust.com">http://rockefellerthrust.com</a></h2>
<iframe width="560" height="315" src="https://www.youtube.com/embed/9saLsvWcppw?si=dzmjq3-6LYH6JDAB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<iframe width="560" height="315" src="https://www.youtube.com/embed/CSJTXST1jII?si=_k5D8et-ejq73DP_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<?php

$tags = file_get_contents('./tags.txt', true);
$letters = file_get_contents('./letters.txt', true);
print "<h2>Total tags: $tags Total letters: $letters</h2>Send me a tweet on for inquiries: ";
print "<a href='http://twitter.com/sanderm'><img width=100 src='twitterx.png'></a>";

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
    print "<form action='http://rockefellerthrust.com:8080/change' method='post' enctype='multipart/form-data'>";
    print "<label for='changefiles'>Choose a file:</label><br>";
    //print "<select name='changefile' id='changefile'>";
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
            //print "<option value='" . $entry . "'";
            //if ("$entry" == "$changefile") {
            //    print " selected ";
            //}            
            //print ">$entry</option>";
            //print "<a href='?file=$entry'>$entry</a>";
            print "<input type='radio' name='changefile'";
            if ("$entry" == "$changefile") {
                print " checked ";
            }
            print "value='$entry'>$entry<br>";
            }
        }
    }

    closedir($handle);
    print "</select>";
    print "<input type='image' name='submit' src='send-bt.jpg' border='0' alt='Submit' style='width: 50px;' />";
    print "<input type='image' name='submit' src='skip-bt.jpg' border='0' alt='Submit' style='width: 50px;' />";
    print "</form>";
}
            //$file="";
            //if (isset($_REQUEST['file'])) {
            //  $file= $_REQUEST['file'];
            //}
            //if ($entry = $file) {
            //}

?>
<div class="tagup" tagupimagehref="http://rockefellerthrust.com/startupmap.rev25-normal.png"></div>
<form action="http://rockefellerthrust.com:8080/change" method="post" enctype="multipart/form-data">
  <input id="fileupload" type="file" name="file">
  <input type="submit" value="Upload">
</form>
<span style="vertical-align:top">Embed:</span><textarea style="height: 200px; width: 700px;" class="test-input">
  <!--
embed code on yourwebsite
-->
  <html>
  <head>
  <script src="https://cdn.firebase.com/js/client/2.4.2/firebase.js"></script>
  <script src="https://rockefellerthrust.com/jquery.js"></script>
  <script src="https://rockefellerthrust.com/jquery-csv.js"></script>
  <script type="text/javascript" src=https://rockefellerthrust.com/tagup.js></script>
  <script>
  window.onload = function ()
  {
	  Tagup.initialize("https://tagupexits2-710aa.firebaseio.com/", "https://rockefellerthrust.com/startupmap.rev25-normal.png", document.getElementsByTagName("body")[0]);
  }
  </script>
  <link rel="stylesheet" type="text/css" href='https://rockefellerthrust.com/tagup.css'/>
  <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
  </head>
  <title>Tagup demo</title>
  <body>
  <form action="http://rockefellerthrust.com:8080/upload" method="post" enctype="multipart/form-data">
  <input id="fileupload" type="file" name="file">
  <input type="submit" value="Upload">
  </form>
  </body>
  </html>
</textarea>
<form action="http://rockefellerthrust.com:8080/upload" method="post" enctype="multipart/form-data">
  <input id="fileupload" type="file" name="file">
  <input type="submit" value="Upload">
</form>
</body>

</html>
