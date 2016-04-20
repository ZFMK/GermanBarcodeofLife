<?php

require('../New/Includes/PHPExcel.php');

//$db = new PDO('mysql:host=localhost;dbname=gbol-1.5;charset=utf8', 'GzBfOmLk', 'v8KtFdHSPMA2z.Mv');
$db = new PDO('mysql:host=localhost;dbname=gbol_python;charset=utf8', 'root', 'vmware');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

$test_category = array(false, 'logged_in', 'anonymous');
$test = $test_category[1];

if ($test == $test_category[1] or ($test == $test_category[2])) {
	if ($test == $test_category[1]) {
		$uid = intval("214");
	} else {
		$uid = intval("not logged in");
	}
	/* NO category & NO search string */
	$id = '';
	$category = '';
	/* NO category & search string */
	$id = 'Riedenberg';
	$category = '';
	/* Category & NO search string */
	$id = "";
	$category = "Taxon Name";
	/* Category & search string */
	$id = 'Erpobdella';
	$category = "Taxon Name";
} else {
	$id = $_POST['caption'];
	$category = $_POST['category'];
	$uid = $_POST['user_id'];
}

$lang = 'DE';
$short_field_query =  " f.id in ('2".$lang."', '7".$lang."', '12".$lang."', '17".$lang."')";
$no_results = array();
$no_results['DE'] = "Keine Ergebnisse gefunden";
$no_results['EN'] = "Nothing found";

// hole alle Feld-Kategorien in der ausgewählten Sprache

if($uid>0) {  // nicht eingeloggt
	$sql = " SELECT id, field_name, category FROM `GBOL_Data_Fields` where id like '%".$lang."' order by `order`";
} else {
	$sql = " SELECT id, field_name, category FROM `GBOL_Data_Fields` where id like '%".$lang."' and restricted<1 order by `order`";
}

if ($test != false) {
	print "\nField Query:\n\t";
	print $sql;
	print "\n";
}

$stmt = $db->prepare($sql);
$stmt->execute();
$rows = $stmt->fetchAll(PDO::FETCH_NUM);
$fields = array();
for( $i = 0; $i < count($rows) -1; $i++ ) {
	$fields[] = $rows[$i][0];
}
$long_field_query = " f.id in ('".implode("','", $fields)."')";

if ($test != false) {
	print "\nAll Fields:\n\t";
	print $long_field_query;
}


$sql = "Select s.id, ";

if($uid>0) {
	$sql = $sql . "g.lat as latitude, g.lon as longitude, ";
} else {
	$sql = $sql . "g.center_x as latitude, g.center_y as longitude, ";
}
$sql = $sql . " if(s.id is null, t.taxon, s.taxon) as taxon, replace(c.breadcrumb,';',' &#187; ') as parenttaxon,
			(select group_concat(concat('\"',d.field, '\":[\"', f.field_name, '\",\"', if(left(d.field,2)=2,DATE_FORMAT(d.term, '%d.%m.%Y'),d.term),'\"]') separator ',')
				from GBOL_Data2Specimen ds
					inner join GBOL_Data d on d.id = ds.data_id
					inner join GBOL_Data_Fields f on f.id = d.field        
				where ".$long_field_query." and ds.specimen_id = s.id
			) as data
		from GBOL_Taxa t
			left join GBOL_Taxa_Cache c on c.taxon_id = t.id
			left join GBOL_Specimen s on t.id = s.taxon_id
			left join GBOL_Geo g on g.specimen_id = s.id";


// Keine Kategorie Ausgewählt
if($category == '0' or $category == "") {
	// Und keinen Suchbegriff
	if($id == "") {
		//$sql = $sql . " )";
		$stmt = $db->prepare($sql);
	}
	// Und einen Suchbegriff
	else {
		$sql = $sql . " where s.id IN (
			select s.id
			from GBOL_Data2Specimen ds
				inner join GBOL_Specimen s on ds.specimen_id = s.id
				inner join GBOL_Data d ON d.id = ds.data_id
				inner join GBOL_Data_Fields f On f.id = d.field 
				inner join GBOL_Taxa t ON t.id = s.taxon_id 
				inner join GBOL_Taxa_Cache c on c.taxon_id=s.taxon_id
			where (d.term like :id or c.breadcrumb like :id2)";
		if($uid==0) {
			$sql = $sql . " and f.restricted<1)";
		} else {
			$sql = $sql . ")";
		}
		$stmt = $db->prepare($sql);
		$stmt->bindValue(':id', "%".$id."%");
		$stmt->bindValue(':id2', "%".$id."%");
	}
}
//Kategorie ausgewählt
else {
	// und keinen Suchbegriff
	if($id == "") {
		if($category == "Taxon Name") {
			$sql = $sql . " where t.id in (select taxon_id from GBOL_Taxa_Cache)" ;
			$stmt = $db->prepare($sql);
		}
		else {
			$sql = $sql . " where s.id IN (
				select s.id
				from GBOL_Data2Specimen ds
					inner join GBOL_Specimen s on ds.specimen_id = s.id
					inner join GBOL_Data d ON d.id = ds.data_id
					inner join GBOL_Data_Fields f On f.id = d.field 
				where f.field_name = :category";
			if($uid==0) {
				$sql = $sql . " and f.restricted<1)";
			} else {
				$sql = $sql . ")";
			}
			$stmt = $db->prepare($sql);
			$stmt->bindValue(':category', $category);
		}
	}
	// und einen Suchbegriff
	else {
		if($category == "Taxon Name") {
			$sql = $sql . " where c.breadcrumb like :id " ;
			$stmt = $db->prepare($sql);
			$stmt->bindValue(':id', "%".$id."%");
		}
		else {
			$sql = $sql . " where s.id IN (
				select s.id
				from GBOL_Data2Specimen ds
					inner join GBOL_Specimen s on ds.specimen_id = s.id
					inner join GBOL_Data d ON d.id = ds.data_id
					inner join GBOL_Data_Fields f On f.id = d.field 
				where f.field_name = :category and d.term like :id";
			if($uid==0) {
				$sql = $sql . " and f.restricted<1)";
			} else {
				$sql = $sql . ")";
			}
			$stmt = $db->prepare($sql);
			$stmt->bindValue(':category', $category);
			$stmt->bindValue(':id', "%".$id."%");
		}
	}
}

if ($test != false) {
	print "\nSearch Query:\n\t";
	print $sql;
	print "\n";
}

$TIMER['before q']=microtime(TRUE);

$stmt->execute();
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

if ($test != false) {
	print "\nNumber of results: ";
	print count($rows);
	print "\n";
}

$TIMER['after q']=microtime(TRUE);

if($id == "") {
	$id = "";
}
if ($category == '0' or $category == "") {
	$category = "";
}

echo "Fundstellen_".$id."_".$category.".txt";

$myFile = "../dateien/intern/download/Fundstellen_".$id."_".$category.".txt";
$fh = fopen($myFile, 'w') or die("can't open file");


/* --- Header --- */
$long_field_query = " f.id in ('".implode("','", $fields)."')";

fwrite($fh, $stringData);

$resA = array();
for($i = 0; $i < count($rows); $i++) {
	$resA[] = '{"coord":["'.str_replace(',','.',$rows[$i]['center_y']).'", "'.str_replace(',','.',$rows[$i]['center_x']).'"], "species": "'.$rows[$i]['taxon'].'", "data":{'.$rows[$i]['data'].'}, "taxa":"'.$rows[$i]['parenttaxon'].'"}';
}
$TIMER['array filled']=microtime(TRUE);  

if ($test == false) {
	header('Content-Type: application/json');

	if(count($rows) == 0) {
		echo '{"success": false, "text": "'.$no_results[$lang].'", "lang":"'.$lang.'", "entries": []}';
	} else {
		echo '{"success": true, "lang":"'.$lang.'", "entries": ['.implode(",", $resA).']}';
	}
}

if ($test != false) {
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


$stmt->execute();
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
$datum = "";
$land = "";
$geschlecht = "";
$alter = "";
$anzahl = "";
$sammeldatum = "";
$katalognummer = "";
$sammelmethode = "";
$habitatbeschreibung = "";
$fundortbeschreibung = "";
$fundort = "";
$praepmethode = "";
$rownumber = 2;
$rows[count($rows)]['id'] = -1;
try {
	if($uid == "noch nicht zugeordnet") {
		$excel = PHPExcel_IOFactory::load("/var/www/bolgermany.de/dateien/intern/download/FundstellenDownloadGast.xls");
	}
	else {
		$excel = PHPExcel_IOFactory::load("/var/www/bolgermany.de/dateien/intern/download/FundstellenDownloadUser.xls");
	}
	$sheet = $excel->getSheetByName( "Tabelle1");
	for( $i = 0; $i < count($rows) -1; $i++) {
		if($rows[$i]['field'] == "7DE" || $rows[$i]['field'] == "7EN") {
			$land = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "2DE" || $rows[$i]['field'] == "2EN") {
			$datum = new DateTime($rows[$i]['term']);
		}
		else if($rows[$i]['field'] == "17DE" || $rows[$i]['field'] == "17EN") {
			$sex = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "15DE" || $rows[$i]['field'] == "15EN") {
			$anzahl = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "12DE" || $rows[$i]['field'] == "12EN") {
			$alter = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "1DE" || $rows[$i]['field'] == "1EN") {
			$katalognummer = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "3DE" || $rows[$i]['field'] == "3EN") {
			$sammelmethode = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "4DE" || $rows[$i]['field'] == "4EN") {
			$sammeldatum = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "11DE" || $rows[$i]['field'] == "11EN") {
			$habitat = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "12DE" || $rows[$i]['field'] == "12EN") {
			$alter = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "13DE" || $rows[$i]['field'] == "13EN") {
			$fundortbeschreibung = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "14DE" || $rows[$i]['field'] == "14EN") {
			$fundort = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "16DE" || $rows[$i]['field'] == "16EN") {
			$praepmethode = $rows[$i]['term'];
		}
		if($i == count($rows) || $rows[$i]['id'] != $rows[$i+1]['id']) {
			if($uid == "noch nicht zugeordnet") {
				$sheet->getCellByColumnAndRow(0, $rownumber)->setValue( $katalognummer);
				$sheet->getCellByColumnAndRow(1, $rownumber)->setValue( $rows[$i]['taxon']);
				$sheet->getCellByColumnAndRow(2, $rownumber)->setValue( $rows[$i]['parenttaxon']);
				$sheet->getCellByColumnAndRow(3, $rownumber)->setValue( $alter);
				$sheet->getCellByColumnAndRow(4, $rownumber)->setValue( $sex);
				$sheet->getCellByColumnAndRow(5, $rownumber)->setValue( $land);
				$sheet->getCellByColumnAndRow(6, $rownumber)->setValue( $fundort);
				$sheet->getCellByColumnAndRow(7, $rownumber)->setValue( $sammelmethode);
				$sheet->getCellByColumnAndRow(8, $rownumber)->setValue( $sammeldatum);
				$sheet->getCellByColumnAndRow(9, $rownumber)->setValue( $habitat);
				$sheet->getCellByColumnAndRow(10, $rownumber)->setValue( $praepmethode);
				$sheet->getCellByColumnAndRow(11, $rownumber)->setValue( $datum->format('d.m.Y'));
			} else {
				$sheet->getCellByColumnAndRow(0, $rownumber)->setValue( $katalognummer);
				$sheet->getCellByColumnAndRow(1, $rownumber)->setValue( $rows[$i]['taxon']);
				$sheet->getCellByColumnAndRow(2, $rownumber)->setValue( $rows[$i]['parenttaxon']);
				$sheet->getCellByColumnAndRow(3, $rownumber)->setValue( $alter);
				$sheet->getCellByColumnAndRow(4, $rownumber)->setValue( $sex);
				$sheet->getCellByColumnAndRow(5, $rownumber)->setValue( $land);
				$sheet->getCellByColumnAndRow(6, $rownumber)->setValue( $fundort);
				$sheet->getCellByColumnAndRow(7, $rownumber)->setValue( $fundortbeschreibung);
				$sheet->getCellByColumnAndRow(8, $rownumber)->setValue( $rows[$i]['center_x']);
				$sheet->getCellByColumnAndRow(9, $rownumber)->setValue( $rows[$i]['center_y']);
				$sheet->getCellByColumnAndRow(10, $rownumber)->setValue( $sammelmethode);
				$sheet->getCellByColumnAndRow(11, $rownumber)->setValue( $sammeldatum);
				$sheet->getCellByColumnAndRow(12, $rownumber)->setValue( $habitat);
				$sheet->getCellByColumnAndRow(13, $rownumber)->setValue( $praepmethode);
				$sheet->getCellByColumnAndRow(14, $rownumber)->setValue( $datum->format('d.m.Y'));
			}
			$datum = "";
			$land = "";
			$sex = "";
			$alter = "";
			$anzahl = "";
			$sammeldatum = "";
			$katalognummer = "";
			$sammelmethode = "";
			$habitat = "";
			$fundortbeschreibung = "";
			$fundort = "";
			$praepmethode = "";
			$rownumber ++;
	}

fclose($fh);

}
//todo filedownload vielleicht schon hier einbauen
//sonst nach dem ajax call in javascript
?>
