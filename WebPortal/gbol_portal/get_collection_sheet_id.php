#!/usr/bin/php
<?php
set_include_path(get_include_path() . PATH_SEPARATOR . '../php_inc/');

include 'PHPExcel.php';
include 'PHPExcel/IOFactory.php';

if (version_compare(PHP_VERSION, "5.2.0", "<")) {
	$version  = PHP_VERSION;
	echo <<<EOF

ERROR: This script requires at least PHP version 5.2.0. You invoked it with
       PHP version {$version}.
\n
EOF;
	exit;
}
error_reporting(E_ALL);
ini_set('display_errors', TRUE);
ini_set('display_startup_errors', TRUE);
date_default_timezone_set('Europe/Berlin');

function parse_excel_file($inputFileName) {
	$inputFileType = PHPExcel_IOFactory::identify($inputFileName);
	$objReader = PHPExcel_IOFactory::createReader($inputFileType);
	$objPHPExcel = $objReader->load($inputFileName);
	$transaction_id = $objPHPExcel->getProperties()->getSubject();
	if ($transaction_id=='') {
		$transaction_id = $objPHPExcel->getSheet(0)->getCell('A1')->getValue();
	}
	return $transaction_id;
}


$script = basename(array_shift($_SERVER['argv']));

if (in_array('--help', $_SERVER['argv']) || empty($_SERVER['argv'])) {
  echo <<<EOF

Get GBOL transaction id from Metadata in Collection Excel Sheet .

Usage:        {$script} "<filename>.xls"

\n
EOF;
  exit;
}

$file = '';

while ($param = array_shift($_SERVER['argv'])) {
	$file = $param;
}

define('DRUPAL_ROOT', getcwd());
$transaction_id=parse_excel_file($file);
exit($transaction_id);
