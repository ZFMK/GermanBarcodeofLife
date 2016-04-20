<?php
try {
	//$db = new PDO('mysql:host=localhost;dbname=gbol-1.5;charset=utf8', 'GzBfOmLk', 'v8KtFdHSPMA2z.Mv');
	$db = new PDO('mysql:host=localhost;dbname=gbol_python;charset=utf8', 'root', 'vmware');
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$db->setAttribute(PDO::ATTR_EMULATE_PREPARES, false);

	$uid = $_POST['user_id'];
	$sql = "select language from users where uid = ?";
	$stmt = $db->prepare($sql);
	$stmt->bindValue(1, $uid , PDO::PARAM_INT);
	$stmt->execute();
	$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
	$language = $rows[0]['language'];

	if($language == "" || $language == null) {
		$language = "DE";
	}
	$sql = "select field_name from GBOL_Data_Fields where id like ? ";
	if($uid==0) {
		$sql = $sql . " and restricted != 1 ;";
	}
	$stmt = $db->prepare($sql);

	$stmt->bindValue(1, "%".$language. "%", PDO::PARAM_STR);
	$stmt->execute();

	$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

	for( $i = 0; $i < count($rows); $i++) {
		echo $rows[$i]['field_name']. ";";
	}
} catch(PDOException $ex) {
	echo "An Error occured! ".$ex;
}
?>

