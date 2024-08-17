if ($_REQUEST['match']) {
  $match= $_REQUEST['match'];
}
cmd = 'grep -R "$match" ./uploads/*.csv.csv';
$result = exec(cmd);
print_r(result);
