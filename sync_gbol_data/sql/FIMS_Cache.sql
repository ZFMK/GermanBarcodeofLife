drop database if exists fims;
create database fims;

CREATE TABLE `GBOL_FIMS` (
	`CollectionSpecimenID` int(10) unsigned NOT NULL,
	`ProjectID` int(10) unsigned DEFAULT NULL,
	`Project` varchar(50) NOT NULL,
	`GBOL_Nr` varchar(50) NOT NULL,
	`Einsender` varchar(255) DEFAULT NULL,
	`EinsenderNummer` varchar(255) DEFAULT NULL,
	`Feldnummer` varchar(50) DEFAULT NULL,
	`Ordnung` varchar(255) DEFAULT NULL,
	`Familie` varchar(255) DEFAULT NULL,
	`Taxon_Name` varchar(255) DEFAULT NULL,
	`Taxon_Qualifier` varchar(50) DEFAULT NULL,
	`Bestimmer_Name` varchar(255) DEFAULT NULL,
	`Taxon_URI` varchar(255) DEFAULT NULL,
	`Bestimmungs_Datum` varchar(255) DEFAULT NULL,
	`Bem_Taxonomie` text,
	`Entwicklungsstadium` varchar(255) DEFAULT NULL,
	`Sex` varchar(50) DEFAULT NULL,
	`Number_of_Units` varchar(50) DEFAULT NULL,
	`Bem_Probe` text,
	`Tissue_Description` text,
	`Number_Part` varchar(50) DEFAULT NULL,
	`Fixierungsmethode` text,
	`CollectionEventGUID` varchar(50) DEFAULT NULL,
	`Land` varchar(50) DEFAULT NULL,
	`Bundesland` varchar(255) DEFAULT NULL,
	`Bundesland_URI` varchar(255) DEFAULT NULL,
	`Fundort` text,
	`Fundortbeschreibung` text,
	`Longitude` varchar(255) DEFAULT NULL,
	`Latitude` varchar(255) DEFAULT NULL,
	`GKS_R` varchar(255) DEFAULT NULL,
	`GKS_H` varchar(255) DEFAULT NULL,
	`Geo_Accuracy` varchar(50) DEFAULT NULL,
	`Geo_Method` varchar(500) DEFAULT NULL,
	`Geo_Notes` text,
	`Altitude_from` varchar(255) DEFAULT NULL,
	`Altitude_to` varchar(255) DEFAULT NULL,
	`Altitude_accuracy` varchar(50) DEFAULT NULL,
	`Altitude_notes` text,
	`Sammler` varchar(255) DEFAULT NULL,
	`Sammel_Datum` varchar(25) DEFAULT NULL,
	`Sammelmethode` text,
	`Bem_Sammeln` text,
	`Habitat` text,
	`Barcode` text,
	`Analysis_Person` varchar(255) DEFAULT NULL,
	`Analysis_Date` varchar(50) DEFAULT NULL,
	`Analysis_Number` varchar(50) DEFAULT NULL,
	`Problems` text,
	`Original_Notes` text,
	`Additional_Notes` text,
	`Sammeltabelle` text,
	`Collection` varchar(255) DEFAULT NULL,
	`Material_Category` varchar(50) DEFAULT NULL,
	`Storage_Location` varchar(255) DEFAULT NULL,
	`Preparation_Date` datetime DEFAULT NULL,
	`Notes_for_part` text,
	`RowGUID` varchar(36) DEFAULT NULL,
	`Blocked_Until` varchar(255) DEFAULT NULL,
	`Specimen_Created_by` varchar(50) DEFAULT NULL,
	`Specimen_Changed_by` varchar(50) DEFAULT NULL,
	`Specimen_Created` datetime DEFAULT NULL,
	`Specimen_Changed` datetime DEFAULT NULL,
	`Created` datetime DEFAULT NULL,
	`Changed` datetime DEFAULT NULL,
	PRIMARY KEY (`CollectionSpecimenID`),
	KEY `idx_gbol_nr` (`GBOL_Nr`) USING HASH,
	KEY `idx_taxon-Name` (`Taxon_Name`),
	KEY `idx_CollectionEventGUID` (`CollectionEventGUID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `GBOL_FIMS_tmp` (
	`CollectionSpecimenID` int(10) unsigned NOT NULL,
	`ProjectID` int(10) unsigned DEFAULT NULL,
	`Project` varchar(50) NOT NULL,
	`GBOL_Nr` varchar(50) NOT NULL,
	`Einsender` varchar(255) DEFAULT NULL,
	`EinsenderNummer` varchar(255) DEFAULT NULL,
	`Feldnummer` varchar(50) DEFAULT NULL,
	`Ordnung` varchar(255) DEFAULT NULL,
	`Familie` varchar(255) DEFAULT NULL,
	`Taxon_Name` varchar(255) DEFAULT NULL,
	`Taxon_Qualifier` varchar(50) DEFAULT NULL,
	`Bestimmer_Name` varchar(255) DEFAULT NULL,
	`Taxon_URI` varchar(255) DEFAULT NULL,
	`Bestimmungs_Datum` varchar(255) DEFAULT NULL,
	`Bem_Taxonomie` text,
	`Entwicklungsstadium` varchar(255) DEFAULT NULL,
	`Sex` varchar(50) DEFAULT NULL,
	`Number_of_Units` varchar(50) DEFAULT NULL,
	`Bem_Probe` text,
	`Tissue_Description` text,
	`Number_Part` varchar(50) DEFAULT NULL,
	`Fixierungsmethode` text,
	`CollectionEventGUID` varchar(50) DEFAULT NULL,
	`Land` varchar(50) DEFAULT NULL,
	`Bundesland` varchar(255) DEFAULT NULL,
	`Bundesland_URI` varchar(255) DEFAULT NULL,
	`Fundort` text,
	`Fundortbeschreibung` text,
	`Longitude` varchar(255) DEFAULT NULL,
	`Latitude` varchar(255) DEFAULT NULL,
	`GKS_R` varchar(255) DEFAULT NULL,
	`GKS_H` varchar(255) DEFAULT NULL,
	`Geo_Accuracy` varchar(50) DEFAULT NULL,
	`Geo_Method` varchar(500) DEFAULT NULL,
	`Geo_Notes` text,
	`Altitude_from` varchar(255) DEFAULT NULL,
	`Altitude_to` varchar(255) DEFAULT NULL,
	`Altitude_accuracy` varchar(50) DEFAULT NULL,
	`Altitude_notes` text,
	`Sammler` varchar(255) DEFAULT NULL,
	`Sammel_Datum` varchar(25) DEFAULT NULL,
	`Sammelmethode` text,
	`Bem_Sammeln` text,
	`Habitat` text,
	`Barcode` text,
	`Analysis_Person` varchar(255) DEFAULT NULL,
	`Analysis_Date` varchar(50) DEFAULT NULL,
	`Analysis_Number` varchar(50) DEFAULT NULL,
	`Problems` text,
	`Original_Notes` text,
	`Additional_Notes` text,
	`Sammeltabelle` text,
	`Collection` varchar(255) DEFAULT NULL,
	`Material_Category` varchar(50) DEFAULT NULL,
	`Storage_Location` varchar(255) DEFAULT NULL,
	`Preparation_Date` datetime DEFAULT NULL,
	`Notes_for_part` text,
	`RowGUID` varchar(36) DEFAULT NULL,
	`Blocked_Until` varchar(255) DEFAULT NULL,
	`Specimen_Created_by` varchar(50) DEFAULT NULL,
	`Specimen_Changed_by` varchar(50) DEFAULT NULL,
	`Specimen_Created` datetime DEFAULT NULL,
	`Specimen_Changed` datetime DEFAULT NULL,
	`Created` datetime DEFAULT NULL,
	`Changed` datetime DEFAULT NULL,
	PRIMARY KEY (`CollectionSpecimenID`),
	KEY `idx_gbol_nr` (`GBOL_Nr`) USING HASH
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE VIEW `gbol_fims`.`fims` AS
	select
		`f`.`CollectionSpecimenID` AS `CollectionSpecimenID`,
		`f`.`GBOL_Nr` AS `GBOL_Nr`,
		`f`.`Einsender` AS `Einsender`,
		`f`.`EinsenderNummer` AS `EinsenderNummer`,
		`f`.`Feldnummer` AS `Feldnummer`,
		`f`.`Ordnung` AS `Ordnung`,
		`f`.`Familie` AS `Familie`,
		trim(trailing ',' from substring_index(`f`.`Taxon_Name`, ' ', 2)) AS `Taxon_Name`,
		`f`.`Bem_Taxonomie` AS `Bem_Taxonomie`,
		`f`.`Entwicklungsstadium` AS `Entwicklungsstadium`,
		`f`.`Sex` AS `Sex`,
		`f`.`Bem_Probe` AS `Bem_Probe`,
		`f`.`Number_Part` AS `Number_Part`,
		`f`.`Fixierungsmethode` AS `Fixierungsmethode`,
		`f`.`Land` AS `Land`,
		`f`.`Bundesland` AS `Bundesland`,
		`f`.`Fundort` AS `Fundort`,
		`f`.`Fundortbeschreibung` AS `Fundortbeschreibung`,
		`f`.`Sammler` AS `Sammler`,
		`f`.`Sammel_Datum` AS `Sammel_Datum`,
		`f`.`Sammelmethode` AS `Sammelmethode`,
		`f`.`Bem_Sammeln` AS `Bem_Sammeln`,
		if(isnull(`f`.`Barcode`), 0, 1) AS `Barcode`,
		`f`.`Problems` AS `Problems`,
		`f`.`Specimen_Changed` AS `Specimen_Changed`
	from
		`gbol_fims`.`GBOL_FIMS` `f`