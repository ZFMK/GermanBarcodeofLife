<?php
	ini_set('display_errors',1);
	error_reporting(E_ALL);
	
	$test = 0;
	// 0: no test
	// 1: use testdate from file
	// 2: generate testdata, no read from file

	$path = '../dateien/intern/download/';

	if ($test>0){
		$filename = "Fundstellen_Gastropoda_TaxonName.txt";
	} else {
		//$pwd = preg_replace( '~(\w)$~' , '$1' . DIRECTORY_SEPARATOR , realpath( getcwd() ) );
		//$path = preg_replace( '~[/\\\\]scripts[/\\\\]$~' , DIRECTORY_SEPARATOR , $pwd).$_GET['path'];
		$filename = $_GET['path'];
	}
$file_path = $path.$filename;
if (file_exists($file_path))
{
	if ($test==1) {
		$handler = true;
	} else {
		$handler = fopen($file_path, 'r');
	}
	if(false !== $handler)
	{
		header('Content-Description: File Transfer');
		header('Content-Type: text/csv');
		header('Content-Disposition: attachment; filename='.$filename);
		header('Expires: 0');
		header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
		header('Pragma: no-cache');
		header('Content-Length: ' . filesize($file_path));

		if ($test==1){
			$data = array(
				array("name 1", "age 1", "city 1"),
				array("name 2", "age 2", "city 2"),
				array("name 3", "age 3", "city 3")
			);
			foreach($data as $vals) {
				echo implode("\t",$vals);
				echo "\n";
			}
		} else { //Send the file content in chunks*/
			while (!feof($handler)) {
				echo fread($handler,4096);
			}
		}
	}
	if ($test!=1) {
		fclose($handler);
	}
	exit;
}
$error = "Content error: The file ".$file_path." does not exist!";
/*header('Content-Description: Content Error');
header('Content-Type: text/plain');
header('Content-Disposition: attachment; filename='.$filename);
header('Expires: 0');
header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
header('Pragma: no-cache');
header('Content-Length: ' . strlen($error));*/
echo $error;
?>
