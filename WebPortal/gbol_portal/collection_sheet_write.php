#!/usr/bin/php
<?php
set_include_path(get_include_path() . PATH_SEPARATOR . '../php_inc/');

#include 'PHPExcel.php';
#include 'PHPExcel/IOFactory.php';
require_once dirname(__FILE__) . '/../php_inc/PHPExcel.php';
require_once dirname(__FILE__) . '/../php_inc/PHPExcel/IOFactory.php';

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

define('VERBOSE', FALSE);

$TIMER = array();

function createExcelFile($TIMER, array $params = array()) {
	$templateFilepath = $params[0];
	$targetFilepath = $params[1];
	$firstTubeNo = $params[2];
	$lastTubeNo = $params[3];
	$transactionId = $params[4];
	if (!isset($params[5])) { $lang = "de"; }
	else { $lang = $params[5]; }


	$templateFileType = PHPExcel_IOFactory::identify($templateFilepath);
	$objReader = PHPExcel_IOFactory::createReader($templateFileType);
	if(VERBOSE){$TIMER['Create reader']=microtime(TRUE);}
	$excel = $objReader->load($templateFilepath);

	if(VERBOSE){$TIMER['Loading file']=microtime(TRUE);}

	$excel->getProperties()->setSubject($transactionId);
	$sheet = $excel->getSheet(2); // getSheetByName("Daten");

	$size = $lastTubeNo-$firstTubeNo;
	for($i = 0; $i <= $size; ++$i) {
		$sheet->getCellByColumnAndRow(0, $i+5)->setValue($firstTubeNo+$i);
	}
	if(VERBOSE){$TIMER['Inserting']=microtime(TRUE);}

	$excelWriter = PHPExcel_IOFactory::createWriter( $excel, $templateFileType );
	//$excelWriter->setPreCalculateFormulas(false);
	$excelWriter->save($targetFilepath);

	if(VERBOSE){$TIMER['Writing file']=microtime(TRUE);}

	$excel->disconnectWorksheets();
	unset($excel);
	unset($excelWriter);

	return $TIMER;
}

if(VERBOSE){$TIMER['Start']=microtime(TRUE);}

$script = basename(array_shift($_SERVER['argv']));

if (in_array('--help', $_SERVER['argv']) || empty($_SERVER['argv'])) {
	echo <<<EOF

Write GBOL Collection Sheet.

Usage:        {$script} templateFilepath targetFilepath firstTubeNo lastTubeNo transactionId lang
	templateFilepath:	Path and filename of template collection sheet, e.g. documents/download/Sammeltabelle_GBOL_2014-10-14.xls
	targetFilepath:		Path and filename of desired collection sheet, e.g. documents/download/700_2015-02-18_000000.xls
	firstTubeNo:		Number of the first tube, e.g. 3500760
	lastTubeNo:			Number of the last tube, e.g. 3500854
	transactionId:		Transaction id as generated during material order, e.g. 700_2015-02-18_000000
	lang:				Current language (not used)

Example:
	collection_sheet_write.php documents/download/Sammeltabelle_GBOL_2014-10-14.xls documents/download/700_2015-02-18_000000.xls 3500760 3500854 700_2015-02-18_000000
\n
EOF;
	exit;
}

define('DRUPAL_ROOT', getcwd());
$TIMER = createExcelFile($TIMER, $_SERVER['argv']);

if(VERBOSE){
	$TIMER['End']=microtime(TRUE);

	$format = "\n%-10s\t%01.3f\t%01.3f\t%01.3f";
	printf("\n%-10s\t%s\t%s\t%s", "name", "so far", "delta", "per cent");
	reset($TIMER);
	$start=$prev=current($TIMER);
	$total=end($TIMER)-$start;
	foreach($TIMER as $name => $value) {
		$sofar=round($value-$start,3);
		$delta=round($value-$prev,3);
		$percent=round($delta/$total*100);
		printf($format, $name, $sofar, $delta, $percent);
		$prev=$value;
	}
	print "\n";
}

exit(0);
