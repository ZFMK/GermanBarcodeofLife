<?php

//$db = new PDO('mysql:host=localhost;dbname=gbol-1.5;charset=utf8', 'GzBfOmLk', 'v8KtFdHSPMA2z.Mv');
$db = new PDO('mysql:host=localhost;dbname=gbol_python;charset=utf8', 'root', 'vmware');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

$TIMER['start']=microtime(TRUE);

$test_category = array(false, 'logged_in', 'anonymous');
$test = $test_category[0];

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
	$id = 'Lemke';
	$category = "Sammlername";
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
$file_trunk['DE'] = "Fundstellen";
$file_trunk['EN'] = "Locations";
$coord['lat']['DE'] = "Geogr. Breite";
$coord['lon']['DE'] = "Geogr. Länge";
$coord['lat']['EN'] = "Geo. lat";
$coord['lon']['EN'] = "Geo. lon";
$taxon['parent_taxa']['DE'] = "Taxa";
$taxon['parent_taxa']['EN'] = "Higher Taxa";

// hole alle Feld-Kategorien in der ausgewählten Sprache
$Afields = array();
$Afields_query = array();

if($uid>0) {  // nicht eingeloggt
	$sql = " SELECT id, field_name, category, `order` FROM `GBOL_Data_Fields` where id like '%".$lang."' order by `order`";
} else {
	$sql = " SELECT id, field_name, category, `order` FROM `GBOL_Data_Fields` where id like '%".$lang."' and restricted<1 order by `order`";
}

if ($test != false) {
	print "\nField Query:\n\t";
	print $sql;
	print "\n";
}

$stmt = $db->prepare($sql);
$stmt->execute();
$Arows = $stmt->fetchAll(PDO::FETCH_NUM);
for( $i = 0; $i < count($Arows); $i++ ) {
	$Afields[] = array(intval($Arows[$i][3]), $Arows[$i][1], $Arows[$i][0]);
	$Afields_order[] = intval($Arows[$i][3]);
}
$TIMER['fieldnames']=microtime(TRUE);

if ($test != false) {
	print "\nAll Fields:\n\t";
	print $Afields;
}
$Sfields_query = ' f.`order` in ('.implode(',',$Afields_order).') and f.id like "%'.$lang.'"';


$sql = "Select s.id, ";

if($uid>0) {
	$sql = $sql . "replace(g.lat, ',', '.') as `lat`, replace(g.lon, ',', '.') as `lon`, ";
} else {
	$sql = $sql . "replace(g.center_x, ',', '.') as `lat`, replace(g.center_y, ',', '.') as `lon`, ";
}
$sql = $sql . " if(s.id is null, t.taxon, s.taxon) as taxon, replace(c.breadcrumb,';',', ') as `parent_taxa`,
			(select group_concat(concat(f.`order`, '|', if(left(f.id,2)=2,DATE_FORMAT(d.term, '%d.%m.%Y'),d.term)) order by f.`order` separator '§')
				from GBOL_Data2Specimen ds
					inner join GBOL_Data d on d.id = ds.data_id
					inner join GBOL_Data_Fields f on f.id = d.field        
				where ".$Sfields_query." and ds.specimen_id = s.id
			) as data
		from GBOL_Specimen s
			left join GBOL_Taxa t on t.id = s.taxon_id
			left join GBOL_Taxa_Cache c on c.taxon_id = t.id
			left join GBOL_Geo g on g.specimen_id = s.id
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

if ($test != false) {
	print "\nSearch Query:\n\t".$sql."\n";
}

$stmt->execute();
$Arows = $stmt->fetchAll(PDO::FETCH_ASSOC);

if ($test != false) {
	print "\nNumber of results: ".count($Arows)."\n";
	var_dump($Arows);
	print "\n";
}
$TIMER['after query']=microtime(TRUE);


if (count($Arows)>0) {
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
	$filename = $file_trunk[$lang] . $id . $category . ".txt";

	if ($test != false) {
		$myFile = "./".$filename;
	} else {
		$myFile = "../dateien/intern/download/".$filename;
	}

	$fh = fopen($myFile, 'w') or die("can't open file");

	/* --- Header --- */
	$Ares = array();
	for ( $c = 0; $c < count($Afields); $c++ ) {
		if ($Afields[$c][0]==11) {  // insert Coordinates before no. indivuals
			$Ares[] = $coord['lat'][$lang];
			$Ares[] = $coord['lon'][$lang];
		} else if ($Afields[$c][0]==4) {  // insert parent taxa before coll. method
			$Ares[] = $taxon['parent_taxa'][$lang];
		}
		$Ares[] = $Afields[$c][1];
	}
	$header = implode("\t", $Ares);
	//fwrite($fh,  "\xEF\xBB\xBF");
	fwrite($fh, $header."\n");
	$TIMER['header']=microtime(TRUE);

	/* --- Body --- */
	for ( $i = 0; $i < count($Arows); $i++ ) {
		$Ares = array();
		$Ar = $Arows[$i];
		$Adata = explode('§',$Ar['data']);
		$j = 0;
		foreach($Afields_order as $Scolumn) {
			$Aentry = explode('|', $Adata[$j]);
			if ($Scolumn == 11) {
				$Ares[] = $Ar['lat'];
				$Ares[] = $Ar['lon'];
			} else if ($Scolumn == 2) {
				$Ares[] = $Ar['taxon'];
				$Ares[] = $Ar['parent_taxa'];
			}
			if ($Scolumn == intval($Aentry[0])) {  // is cell in column filled?
				//echo $Scolumn."?=".$Aentry[0]."=> ".$Aentry[1]."\n";
				$Ares[] = $Aentry[1];
				$j++;
			} else if ($Scolumn > 2) {  // insert empty cell, only after taxonname because both Cataloue no. and taxon name are always present
				//echo $Scolumn."?=".$Aentry[0]."=> .\n";
				$Ares[] = "";
			}
		}
		$file_row = implode("\t", $Ares);
		fwrite($fh, $file_row."\n");
	}
	$TIMER['body']=microtime(TRUE);
	
	fclose($fh);
	echo '{"success": true, "filename": "'.$filename.'"}';
} else {
	echo '{"success": false, "text": "' . $no_results[$lang] . '"}';
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
?>
