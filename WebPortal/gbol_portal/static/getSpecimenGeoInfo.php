<?php
error_reporting(E_ALL);
ini_set('display_errors', TRUE);
ini_set('display_startup_errors', TRUE);

$TIMER['start']=microtime(TRUE);

//$db = new PDO('mysql:host=localhost;dbname=gbol-1.5;charset=utf8', 'GzBfOmLk', 'v8KtFdHSPMA2z.Mv');
$db = new PDO('mysql:host=localhost;dbname=gbol_python;charset=utf8', 'root', 'vmware');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

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
	$id = 'Erpobdella';
	$category = "Taxon Name";
	/* treeview and taxon */
	$id = 4403265;
	$category = "treeview";
} else {
	$id = $_POST['id'];
	$category = $_POST['category'];
	$uid = intval($_POST['user_id']);
}

$lang = 'DE';
$short_field_query =  " f.id in ('2".$lang."', '7".$lang."', '12".$lang."', '17".$lang."')";
$no_results = array();
$no_results['DE'] = "Keine Ergebnisse gefunden";
$no_results['EN'] = "Nothing found";

if ($test != false) {
	print $no_results[$lang];
	if ($uid>0) {
		print "\nLogged in\n";
	} else {
		print "\nNot logged in\n";
	}
}

$sql = "Select s.id, ";
if($uid>0) {
	$sql = $sql . "g.lat as center_x, g.lon as center_y, ";
} else {
	$sql = $sql . "g.center_x, g.center_y, ";
}
$sql = $sql . " if(s.id is null, t.taxon, s.taxon) as taxon, replace(c.breadcrumb,';',' &#187; ') as parenttaxon,
			(select group_concat(concat('\"',d.field, '\":[\"', f.field_name, '\",\"', if(left(d.field,2)=2,DATE_FORMAT(d.term, '%d.%m.%Y'),d.term),'\"]') separator ',')
				from GBOL_Data2Specimen ds
					inner join GBOL_Data d on d.id = ds.data_id
					inner join GBOL_Data_Fields f on f.id = d.field        
				where ".$short_field_query." and ds.specimen_id = s.id
			) as data
		from GBOL_Specimen s
			left join GBOL_Taxa t on t.id = s.taxon_id
			left join GBOL_Taxa_Cache c on c.taxon_id = t.id
			left join GBOL_Geo g on g.specimen_id = s.id";

if($category == "treeview") {
	$sql = $sql . " where t.id in (select p.id FROM GBOL_Taxa n, GBOL_Taxa p  where n.id = :id AND p.`lft` BETWEEN n.`lft` AND n.`rgt`)";
	$stmt = $db->prepare($sql);
	$stmt->bindValue(':id', $id);
}else{
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
} else {
	var_dump($resA);
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
