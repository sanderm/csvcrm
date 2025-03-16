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
<!link rel="stylesheet" type="text/css" href="style.css">
</head>
<title>rockefellerthrust.com</title>
<body>
<img src='tagframe-logo.jpg'> Partner:<img width=100 src='stortinget.png'> We are also proud to follow GDPR and DMCA becouse we use firebase storage<br>
<h2><a href="http://rockefellerthrust.com">http://rockefellerthrust.com</a> - scroll down for lists of companies & famous names revealed with video</h2> 
<iframe width="560" height="315" src="https://www.youtube.com/embed/9saLsvWcppw?si=dzmjq3-6LYH6JDAB" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<iframe width="560" height="315" src="https://www.youtube.com/embed/CSJTXST1jII?si=_k5D8et-ejq73DP_" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
<?php
print "<h2>Sander; the trustee of this fund have synonym names like Bradley Cooper, Emanuel Kant, Ronan Keating, Edvard Munch and Bruce Springsteen</h2>";
$tags_num = file_get_contents('./tags.txt', true);
$letters_num = file_get_contents('./letters.txt', true);
$uniq_num = file_get_contents('./uniq.txt', true);
$pages_num = file_get_contents('./pages.txt', true);
print "<h2>Total tags: $tags_num Total letters: $letters_num uniq visitors: $uniq_num visitor pages: $pages_num</h2>Send me a tweet on for inquiries: ";
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
if ($handle = opendir('img/')) {
   while (false !== ($entry = readdir($handle))) {
        if ($entry != "." && $entry != "..") {
            if (stringEndsWith($entry, '.jpg')) {
?>
<div class="slideshow">
<?php
print "<img float='left' height='700' src='img/" . $entry . "'>";
?>
</div>
<?php
           }
       }
   }
}
$choosefile="";
// upload a file to filestore by choosing
if ($handle = opendir('uploads/')) {
    print "<form action='http://rockefellerthrust.com:8080/choosefile' method='post' enctype='multipart/form-data'>";
    print "<label for='changefiles'>Choose a file:</label><br>";
    //print "<select name='changefile' id='changefile'>";
    //$changefile= $_REQUEST['changefiles'] 
   while (false !== ($entry = readdir($handle))) {
        
        if ($entry != "." && $entry != "..") {

            $onecsvfile="";
            if (stringEndsWith($entry, '.csv')) {
                 $onecsvfile .= $entry;
                 $csvfiles .="$onecsvfile";

            $sum= "$sum" . "$entry\n";
            if ("$entry" == "$choosefile") {
                $exec_entry = "$entry";
            }
                //$exec_entry .= "$changefile";
            //print "<option value='" . $entry . "'";
            //if ("$entry" == "$changefile") {
            //    print " selected ";
            //}            
            //print ">$entry</option>";
            //print "<a href='?file=$entry'>$entry</a>";
            //$changefile= $_REQUEST['changefile'];
            print "<input type='radio' name='choosefile'";
            if ("$entry" == "$choosefile") {
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
<form action="http://rockefellerthrust.com:8080/upload" method="post" enctype="multipart/form-data">
  <input id="fileupload" type="file" name="fileupload">
  <input type="submit" value="Upload">
</form>
<span style="vertical-align:top">Embed:</span><form><textarea style="height: 200px; width: 700px;" class="test-input">
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
  <input id="fileupload" type="file" name="fileupload">
  <input type="submit" value="Upload">
  </form>
  </body>
  </html>
</textarea>
</form>
</body>

</html>
