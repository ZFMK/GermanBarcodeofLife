BOL = {};

BOL.results = {};

BOL.set_lang = function(lang) {
	this.lang = lang;
};

BOL.get_lang = function() {
	return this.lang;
};

BOL.loadingOverlay = function($target, mode, text) {
	if(mode == 'display') {
		if(document.getElementById("overlay") === null) {
			var div = '<div id="overlay" /><div id="overlay_msg">'+text+'</div>';
			$target.prepend(div);
		}
	} else {
		$target.remove( "#overlay" );;
		$target.remove( "#overlay_msg" );;
	}
};

function setMenu(elementId){
	$('#'+elementId).addClass('active');
}
function setCurrentMenu(){
	//contains window.location.pathname machen und entsprechenden obermenüpunkt mit getelementbyid ansprechen und klasse hinzufügen, die ausgewählten teil markiet
	if(window.location.pathname.indexOf("/ergebnisse") != -1) {
		setMenu("menu-ergebnisse");
	}
	else if(window.location.pathname.indexOf("/sammeln/regist") != -1) {
		setMenu("menu-regist");
	}
	else if(window.location.pathname.indexOf("/sammeln/dashboard") != -1) {
		setMenu("menu-login");
	}
	else if(window.location.pathname.indexOf("/sammeln/login") != -1) {
		setMenu("menu-login");
	}
	else if(window.location.pathname.indexOf("/kontakt") != -1) {
		setMenu("menu-kontakt");
	}
	else if(window.location.pathname.indexOf("/links") != -1) {
		setMenu("menu-links");
	}
	else if(window.location.pathname.indexOf("/news/news") != -1) {
		setMenu("menu-publikationen");
	}
	else if(window.location.pathname.indexOf("/news/publikationen") != -1) {
		setMenu("menu-publikationen");
	}
	else if(window.location.pathname.indexOf("/mitmachen") != -1) {
		setMenu("menu-mitmachen");
	}
	else if(window.location.pathname.indexOf("/team") != -1) {
		setMenu("menu-team");
	}
	else if(window.location.pathname.indexOf("/dna-barcoding") != -1) {
		setMenu("menu-barcoding");
	}
	else if(window.location.pathname.indexOf("/gbol") != -1) {
		setMenu("menu-gbol");
	}
	else if(window.location.pathname.indexOf("/admin") != -1) {
		setMenu("menu-admin");
	}
}

BOL.checkStrength = function() {
	var pw = document.getElementById("edit-pass-pass1");
	var bar = document.getElementById("password-bar");
	var strength = 0;
	if (pw.value.length >= 6) {
		document.getElementById("sixLetter").style.display = "none";
		strength = strength + 1;
	}
	else {
		document.getElementById("sixLetter").style.display = "";
	}
	var bigLetterFlag = false,
		smallLetterFlag = false,
		numberLetterFlag = false,
		specialLetterFlag = false;
	for(var i = 0; i < pw.value.length; i ++) {
				var key = pw.value.charCodeAt(i);
		if (key >= 65 && key <= 90) {
			bigLetterFlag = true;
		}
		else if (key >= 97 && key <= 122) {
				smallLetterFlag = true;
		}
		else if (key >= 48 && key <= 57) {
				numberLetterFlag = true;
		}
		else if (key >= 33 && key <= 126) {
				specialLetterFlag = true;
		}
	}
	if (bigLetterFlag == true) {
		document.getElementById("bigLetter").style.display = "none";
		strength = strength + 1;
	}
	else {
		document.getElementById("bigLetter").style.display = "";
	}
	if (smallLetterFlag == true) {
		document.getElementById("smallLetter").style.display = "none";
		strength = strength + 1;
	}
	else {
		document.getElementById("smallLetter").style.display = "";
	}
	if (numberLetterFlag == true) {
		document.getElementById("numberLetter").style.display = "none";
		strength = strength + 1;
	}
	else {
		document.getElementById("numberLetter").style.display = "";
	}
	if (specialLetterFlag == true) {
		document.getElementById("specialLetter").style.display = "none";
		strength = strength + 1;
	}
	else {
		document.getElementById("specialLetter").style.display = "";
	}
	if (strength == 5) {
			document.getElementById("password-suggestion").style.display = "none";
		document.getElementById("password-text").innerHTML = "strong";
	}
	else {
		document.getElementById("password-suggestion").style.display = "block";
		if (strength == 3) {
			document.getElementById("password-text").innerHTML = "okay";
		}
		else if (strength == 4) {
			document.getElementById("password-text").innerHTML = "good";
		}
		else {
			document.getElementById("password-text").innerHTML = "weak";
		}
	}
	bar.style.width = (0 + strength * 20).toString() + "%"
}
