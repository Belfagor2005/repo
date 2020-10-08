<?

$file = $_GET['q'];
file_put_contents("counter.txt", date('l jS \of F Y h:i:s A') . "," . $_GET['q'] . "\n", FILE_APPEND);

header("Content-Type: application/zip");
header("Content-Disposition: attachment; filename=$file");
readfile($file);

?>
