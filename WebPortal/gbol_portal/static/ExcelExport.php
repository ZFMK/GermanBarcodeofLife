<?php
require('../New/Includes/PHPExcel.php');

//$db = new PDO('mysql:host=localhost;dbname=gbol-1.5;charset=utf8', 'GzBfOmLk', 'v8KtFdHSPMA2z.Mv');
$db = new PDO('mysql:host=localhost;dbname=gbol_python;charset=utf8', 'root', 'vmware');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

$TEST = false;

if ($TEST) {
	$id = "Soricomorpha";
	$category = "Taxon Name";
	$uid = 214;
} else {
	$id = $_POST['caption'];
	$category = $_POST['category'];
	$uid = $_POST['user_id'];
}

$lang = 'DE';

$no_results['DE'] = "Die Excel-Datei konnte nicht erstellt werden: ";
$no_results['EN'] = "Could not create Excel file: ";
$file_trunk['DE'] = "Fundstellen";
$file_trunk['EN'] = "Locations";

$sql = "Select s.id, ";
if($uid>0) {
	$sql = $sql . "g.lat as center_x, g.lon as center_y, ";
} else {
	$sql = $sql . "g.center_x, g.center_y, ";
}

$sql = $sql . " if(s.id is null, t.taxon, s.taxon) as taxon, replace(c.breadcrumb,';',', ') as parenttaxon, d.term, d.field
		from GBOL_Taxa t
			left join GBOL_Taxa_Cache c on c.taxon_id = t.id
			left join GBOL_Specimen s on t.id = s.taxon_id
			left join GBOL_Geo g on g.specimen_id = s.id
			left join GBOL_Data2Specimen ds on ds.specimen_id = s.id
			inner join GBOL_Data d on d.id = ds.data_id
			inner join GBOL_Data_Fields f on f.id = d.field
		where";
if($uid<0) {  // nicht eingeloggt
	$sql = $sql . " restricted<1 and";
}

// Keine Kategorie Ausgewählt
if($category == '0' or $category == "") {
	// Und keinen Suchbegriff
	if($id == "") {
		$sql = $sql . " 1=1";
		$stmt = $db->prepare($sql);
	}
	// Und einen Suchbegriff
	else {
		$sql = $sql . " s.id IN (
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
			$sql = $sql . " t.id in (select taxon_id from GBOL_Taxa_Cache)" ;
			$stmt = $db->prepare($sql);
		}
		else {
			$sql = $sql . " s.id IN (
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
			$sql = $sql . " c.breadcrumb like :id " ;
			$stmt = $db->prepare($sql);
			$stmt->bindValue(':id', "%".$id."%");
		}
		else {
			$sql = $sql . " s.id IN (
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

if ($TEST) {
	echo $sql."\n";
}

$datum = "";
$land = "";
$sex = "";
$alter = "";
$anzahl = "";
$sammeldatum = "";
$katalognummer = "";
$sammelmethode = "";
$habitatbeschreibung = "";
$fundortbeschreibung = "";
$fundort = "";
$praepmethode = "";
$habitat = "";
$rownumber = 2;

$stmt->execute();
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
$rows[count($rows)]['id'] = -1;

if ($TEST) {
	echo "\nFound ".count($rows)." entries\n";
}

try {
	if($uid == 0) {
		$excel = PHPExcel_IOFactory::load("../dateien/intern/download/FundstellenDownloadGast.xls");
	}
	else {
		$excel = PHPExcel_IOFactory::load("../dateien/intern/download/FundstellenDownloadUser.xls");
	}
	$sheet = $excel->getSheetByName( "Tabelle1");
	for( $i = 0; $i < count($rows)-1; $i++) {
		if($rows[$i]['field'] == "7".$lang) {
			$land = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "2".$lang) {
			$datum = new DateTime($rows[$i]['term']);
		}
		else if($rows[$i]['field'] == "17".$lang) {
			$sex = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "15".$lang) {
			$anzahl = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "1".$lang) {
			$katalognummer = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "3".$lang) {
			$sammelmethode = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "4".$lang) {
			$sammeldatum = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "11".$lang) {
			$habitat = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "12".$lang) {
			$alter = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "13".$lang) {
			$fundortbeschreibung = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "14".$lang) {
			$fundort = $rows[$i]['term'];
		}
		else if($rows[$i]['field'] == "16".$lang) {
			$praepmethode = $rows[$i]['term'];
		}
		if ($TEST) {
			echo "\n".$land;
			echo "\n".$rows[$i]['taxon'];
		}
		if($i == count($rows) || $rows[$i]['id'] != $rows[$i+1]['id']) {
			if($uid == 0) {
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
			$habitatbeschreibung = "";
			$fundortbeschreibung = "";
			$fundort = "";
			$praepmethode = "";
			$habitat = "";
			$rownumber ++;
		}
	}

	if($id == "") {
		$id = "";
	} else {
		$id = "_".$id;
	}
	if($category == '0' or $category == "") {
		$category = "";
	} else {
		$category = "_".str_replace(' ','',$category);
	}
	$filename = $file_trunk[$lang] . $id . $category . ".xls";

	$excelWriter = PHPExcel_IOFactory::createWriter($excel, 'Excel5');
	$excelWriter->save("../dateien/intern/download/".$filename);

	echo '{"success": true, "filename": "'.$filename.'"}';
}
catch(Exception $ex) {
	echo '{"success": false, "text": "' . $no_results[$lang] . $ex . '"}';
}
//todo filedownload vielleicht schon hier einbauen
//sonst nach dem ajax call in javascript
?>
