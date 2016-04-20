<?php
header('Content-Type: application/json');
try {
	$db = new PDO('mysql:host=localhost;dbname=gbol-1.5;charset=utf8', 'GzBfOmLk', 'v8KtFdHSPMA2z.Mv');
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);
	$id = $_POST['nodeid'];
	//$id = "0";
	$stmt = $db->prepare("SELECT taxon, id, parent_id, known, collected, barcode, collected_individuals, barcode_individuals, rgt - lft as rank FROM GBOL_Taxa where lft is not null AND parent_id = ? order by lft");
	$stmt->bindValue(1, $id, PDO::PARAM_STR);
	$stmt->execute();
	$rows = $stmt->fetchAll(PDO::FETCH_NUM);
	$arr = array();
	for( $i = 0; $i < count($rows); $i++) {
		$arr[] = '["'.$rows[$i][0].'",'.implode(",", array_slice($rows[$i],1)).']';
	}
	echo '{"success": true, "node": '.$id.', "entries": ['.implode(",", $arr).']}';
} catch(Exception $e) {
	echo '{"success": false, "text": "'.$e->getMessage().'", "node": '.$id.', "entries": []}';
}
$db = null;
?>
