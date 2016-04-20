-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: gbol-python
-- ------------------------------------------------------
-- Server version	5.5.47-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `gbol-python`
--

/*!40000 DROP DATABASE IF EXISTS `gbol-python`*/;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `gbol-python` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `gbol-python`;

--
-- Table structure for table `Expertise`
--

DROP TABLE IF EXISTS `Expertise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Expertise` (
  `tid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ExpertiseId',
  `name` varchar(255) NOT NULL DEFAULT '' COMMENT 'Expertise Name',
  PRIMARY KEY (`tid`),
  KEY `name` (`name`),
  KEY `taxonomy_tree` (`name`),
  KEY `vid_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=29993 DEFAULT CHARSET=utf8 COMMENT='Stores term information.';
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `Expertise` WRITE;
/*!40000 ALTER TABLE `Expertise` DISABLE KEYS */;
INSERT INTO `Expertise` VALUES (26778,'Acoelomorpha'),
(26779,'Amphibia (Amphibien)'),
(26780,'Annelida s.l. (Ringelwürmer)'),
(26781,'Arachnida (Spinnentiere)'),
(26782,'Archaeognatha (Felsenspringer)'),
(26783,'Auchenorrhyncha (Zikaden)'),
(26784,'Aves (Vögel)'),
(26785,'Bodenfauna (diverse Taxa)'),
(26787,'Bryozoa (Moostierchen)'),
(26788,'Cnidaria (Nesseltiere)'),
(26789,'Coleoptera (Käfer)'),
(26790,'Crustacea (Krebstiere)'),
(26791,'Dermaptera (Ohrwürmer)'),
(26792,'Dictyoptera'),
(26793,'Diptera (Zweiflügler)'),
(26794,'Entognatha (Sackkiefler)'),
(26795,'Ephemeroptera (Eintagsfliegen)'),
(29992,'Fauna-Ost SGN'),
(26796,'Fungi: Pucciniales (Rostpilze)'),
(26797,'Gnathifera'),
(26798,'Heteroptera (Wanzen)'),
(26799,'Hymenoptera general (Hautflügler)'),
(26800,'Hymenoptera: Formicidae (Ameisen)'),
(26801,'Hymenoptera: Parasitoide'),
(26802,'Lichenes (Flechten)'),
(26803,'Macrolepidoptera (Großschmetterlinge)'),
(26804,'Mammalia (Säugetiere)'),
(26786,'Marchantiophytina / Bryophytina / Anthocerotophytina / Lycophytina / Monilophytina'),
(26805,'Marine Organismen'),
(26806,'Mecoptera (Schnabelfliegen)'),
(26807,'Megaloptera (Großflügler)'),
(26808,'Microlepidoptera (Kleinschmetterlinge)'),
(26809,'Mollusca (Weichtiere)'),
(26810,'Myriapoda (Tausendfüßer)'),
(26811,'Nemathelminthes (Schlauchwürmer)'),
(26812,'Nemertini (Schnurwürmer)'),
(26813,'Neuroptera (Netzflügler)'),
(26814,'Odonata (Libellen)'),
(26815,'Orthoptera (Heuschrecken)'),
(26816,'Phthiraptera (Tierläuse)'),
(26817,'Pisces (Fische)'),
(26818,'Plathelminthes (Plattwürmer)'),
(26819,'Plecoptera (Steinfliegen)'),
(26820,'Porifera (Schwämme)'),
(26821,'Psocoptera (Staubläuse)'),
(26823,'Raphidioptera (Kamelhalsfliegen)'),
(26822,'Reptilia (Reptilien)'),
(26824,'Siphonaptera (Flöhe)'),
(26825,'Spermatophytina (Samenpflanzen)'),
(26830,'Sternorrhyncha (Pflanzenläuse)'),
(26826,'Strepsiptera (Fächerflügler)'),
(26848,'Subterrane Fauna'),
(26827,'Tardigrada (Bärtierchen)'),
(26828,'Thysanoptera (Fransenflügler)'),
(26829,'Trichoptera (Köcherfliegen)'),
(26831,'Zygentoma (Fischchen)');
/*!40000 ALTER TABLE `Expertise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ForcePwChange`
--

DROP TABLE IF EXISTS `ForcePwChange`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ForcePwChange` (
  `Uid` int(10) unsigned NOT NULL,
  `ForceChange` int(1) NOT NULL,
  PRIMARY KEY (`Uid`),
  KEY `fk_ForcePwChange_1` (`Uid`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `ForgotPw`
--

DROP TABLE IF EXISTS `ForgotPw`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ForgotPw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(11) NOT NULL,
  `requestDate` datetime NOT NULL,
  `requestLink` varchar(100) NOT NULL,
  `notUsed` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_CollectionProjects`
--

DROP TABLE IF EXISTS `GBOL_CollectionProjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_CollectionProjects` (
  `specimen_id` int(10) unsigned NOT NULL,
  `project_id` int(10) unsigned NOT NULL,
  KEY `specimen_id` (`specimen_id`),
  KEY `project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='All projects a specimen entry is assigned to (from CollectionProjects)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Data`
--

DROP TABLE IF EXISTS `GBOL_Data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Data` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `term` varchar(3000) DEFAULT NULL,
  `field_id` tinyint(3) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_term` (`term`(255)) USING BTREE,
  KEY `idx_field_id` (`field_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2139895 DEFAULT CHARSET=utf8 COMMENT='Enthält die Daten aus DiversityCollection_ZFMK';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Data2Specimen`
--

DROP TABLE IF EXISTS `GBOL_Data2Specimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Data2Specimen` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `data_id` int(10) unsigned DEFAULT NULL,
  `specimen_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `data_id` (`data_id`),
  KEY `taxa_specimen_id` (`specimen_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2139895 DEFAULT CHARSET=utf8 COMMENT='n:m mapping der Einträge in GBOL_Data auf die Specimen in GB';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Data_Category`
--

DROP TABLE IF EXISTS `GBOL_Data_Category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Data_Category` (
  `id` varchar(4) NOT NULL,
  `category` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Data categories';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Data_Fields`
--

DROP TABLE IF EXISTS `GBOL_Data_Fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Data_Fields` (
  `id` int(10) unsigned NOT NULL,
  `lang` enum('prg','de','en') NOT NULL DEFAULT 'en' COMMENT 'Language. prg for internal use only!',
  `field_name` varchar(255) DEFAULT NULL COMMENT 'The field name from the table in DiversityCollection, i.e. `AccessionNumber`',
  `category` varchar(4) DEFAULT NULL COMMENT 'id zu GBOL_Data_Category',
  `restricted` bit(1) DEFAULT b'0' COMMENT 'wenn 1: Daten können nur von eingeloggten Benutzern eingesehen werden',
  `order` tinyint(3) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`,`lang`),
  KEY `categorie` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Fieldnames (columns names) for the data';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Geo`
--

DROP TABLE IF EXISTS `GBOL_Geo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Geo` (
  `specimen_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'CollectionSpecimenID aus CollectionSpecimen_ZFMK',
  `lat` varchar(25) DEFAULT NULL,
  `lon` varchar(25) DEFAULT NULL,
  `center_x` varchar(45) DEFAULT NULL,
  `center_y` varchar(45) DEFAULT NULL,
  `radius` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`specimen_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Geokoordinaten aus CollectionSpecimen_ZFMK';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Institutes`
--

DROP TABLE IF EXISTS `GBOL_Institutes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Institutes` (
  `institute_id` int(10) unsigned NOT NULL,
  `project_institute` varchar(50) NOT NULL,
  `project_name` varchar(6) DEFAULT NULL,
  `institute_short` varchar(100) DEFAULT NULL,
  `institute_name` varchar(100) NOT NULL,
  PRIMARY KEY (`institute_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Institutes from CollectionExternalDatasource';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Specimen`
--

DROP TABLE IF EXISTS `GBOL_Specimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Specimen` (
  `id` int(10) unsigned NOT NULL COMMENT 'CollectionSpecimenID',
  `taxon_id` int(10) unsigned DEFAULT NULL COMMENT 'TNT TaxonID',
  `taxon` varchar(100) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `barcode` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'Specimen has barcode',
  `institute_id` int(10) unsigned DEFAULT NULL,
  `withhold` varchar(50) DEFAULT NULL,
  `color` enum('black','red') DEFAULT 'black',
  PRIMARY KEY (`id`),
  KEY `taxon_id` (`taxon_id`),
  KEY `taxon` (`taxon`),
  KEY `idx_color` (`color`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='All Specimen from CollectionSpecimen';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Stats_States`
--

DROP TABLE IF EXISTS `GBOL_Stats_States`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Stats_States` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `taxon_id` int(10) unsigned NOT NULL,
  `taxon` varchar(100) NOT NULL,
  `total` int(10) unsigned DEFAULT NULL,
  `collected` int(10) unsigned DEFAULT NULL,
  `barcode` int(10) unsigned DEFAULT NULL,
  `state` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `taxon` (`taxon`),
  KEY `state` (`state`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Taxa`
--

DROP TABLE IF EXISTS `GBOL_Taxa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Taxa` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `taxon` varchar(100) NOT NULL,
  `author` varchar(100) DEFAULT NULL,
  `rank` varchar(25) NOT NULL,
  `parent_id` bigint(20) unsigned DEFAULT NULL,
  `lft` int(10) unsigned DEFAULT NULL,
  `rgt` int(10) unsigned DEFAULT NULL,
  `known` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'number of species',
  `collected` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'number of collected species',
  `barcode` int(10) unsigned NOT NULL DEFAULT '0' COMMENT 'number of species with barcodes',
  `collected_individuals` int(10) NOT NULL DEFAULT '0',
  `barcode_individuals` int(10) NOT NULL DEFAULT '0',
  `color` enum('red','black') DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `left` (`lft`),
  KEY `right` (`rgt`),
  KEY `parent_id` (`parent_id`),
  KEY `taxon` (`taxon`),
  KEY `idx_color` (`color`)
) ENGINE=InnoDB AUTO_INCREMENT=5442940 DEFAULT CHARSET=utf8 COMMENT='All Taxa from tnt.diversityworkbench.de';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Taxa4Statistics`
--

DROP TABLE IF EXISTS `GBOL_Taxa4Statistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Taxa4Statistics` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `taxon_id` int(10) unsigned DEFAULT NULL,
  `user` int(10) unsigned DEFAULT NULL,
  `modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1 COMMENT='Taxa selected for display in statistics';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_TaxaCommonNames`
--

DROP TABLE IF EXISTS `GBOL_TaxaCommonNames`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_TaxaCommonNames` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `taxon_id` int(10) unsigned NOT NULL,
  `name` varchar(255) NOT NULL,
  `code` varchar(2) NOT NULL DEFAULT 'de',
  `db_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `taxon_id` (`taxon_id`),
  KEY `idx_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=4586 DEFAULT CHARSET=utf8 COMMENT='Common taxon names from tnt.diversityworkbench.de';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `GBOL_Taxa_Cache`
--

DROP TABLE IF EXISTS `GBOL_Taxa_Cache`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `GBOL_Taxa_Cache` (
  `taxon_id` int(10) unsigned NOT NULL,
  `breadcrumb` text,
  PRIMARY KEY (`taxon_id`),
  FULLTEXT KEY `text` (`breadcrumb`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Institution`
--

DROP TABLE IF EXISTS `Institution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Institution` (
  `Id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'GBOL Institutionen für Taxon-Koordinatoren',
  `Name` varchar(100) NOT NULL COMMENT 'Long name of the institution',
  `ShortName` varchar(10) NOT NULL COMMENT 'A short name for the institution',
  `Email` varchar(45) DEFAULT NULL COMMENT 'a central email address for the institution',
  `Email_org` varchar(45) DEFAULT NULL,
  `PostalAddress` longtext COMMENT 'the postal address for the institution',
  PRIMARY KEY (`Id`),
  UNIQUE KEY `Name_UNIQUE` (`Name`),
  UNIQUE KEY `ShortName_UNIQUE` (`ShortName`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1 COMMENT='The institution involved into GBOL';
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `Institution` WRITE;
/*!40000 ALTER TABLE `Institution` DISABLE KEYS */;
INSERT INTO `Institution` VALUES (3,'Zoologisches Forschungsmuseum Alexander Koenig','ZFMK','b.rulik@zfmk.de',NULL,'Zoologisches Forschungsmuseum Alexander Koenig\nGBOL: DNA-Barcoding\nAdenauerallee 160\n53113 Bonn');
/*!40000 ALTER TABLE `Institution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `News`
--

DROP TABLE IF EXISTS `News`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `News` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `text` longtext,
  `date` date DEFAULT NULL,
  `lang` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `Publikationen`
--

DROP TABLE IF EXISTS `Publikationen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Publikationen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(10) DEFAULT NULL,
  `text` longtext,
  `date` date DEFAULT NULL,
  `lang` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `RelUserInstitution`
--

DROP TABLE IF EXISTS `RelUserInstitution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `RelUserInstitution` (
  `Uid` int(10) unsigned NOT NULL,
  `InstitutionId` int(11) NOT NULL,
  PRIMARY KEY (`Uid`,`InstitutionId`),
  KEY `fk_RelUserInstituion_1` (`Uid`),
  KEY `fk_RelUserInstituion_2` (`InstitutionId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Relation between (some) Users and their institution. This is';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RelUserInstitution`
--

LOCK TABLES `RelUserInstitution` WRITE;
/*!40000 ALTER TABLE `RelUserInstitution` DISABLE KEYS */;
INSERT INTO `RelUserInstitution` VALUES (42,3);
/*!40000 ALTER TABLE `RelUserInstitution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Role`
--

DROP TABLE IF EXISTS `Role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Role` (
  `id` int(10) unsigned NOT NULL,
  `role` varchar(45) CHARACTER SET latin1 DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

LOCK TABLES `Role` WRITE;
/*!40000 ALTER TABLE `Role` DISABLE KEYS */;
INSERT INTO `Role` VALUES (1,'Administrator',NULL),(2,'Taxon-Koordinator',NULL),(3,'Experte',NULL),(4,'Redaktion',NULL),(5,'Tester',NULL);
/*!40000 ALTER TABLE `Role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ShippingRequests`
--

DROP TABLE IF EXISTS `ShippingRequests`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ShippingRequests` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `TransactionKey` varchar(40) NOT NULL,
  `Uid` int(10) unsigned NOT NULL COMMENT 'references the user id of the user who has done the shipping request',
  `KindOf` varchar(45) NOT NULL COMMENT 'kind of pipes\n',
  `Count` int(11) NOT NULL COMMENT 'number of pipes',
  `ExpertiseId` int(10) unsigned NOT NULL COMMENT 'the taxonomy group of this shipping request',
  `ContactId` int(10) unsigned NOT NULL COMMENT 'references the user id which is the contact person',
  `RequestDate` datetime NOT NULL COMMENT 'the datetime of this request',
  `XlsFile` varchar(200) NOT NULL COMMENT 'Contains the path and name to the xls file relativ to the drupal private files directory',
  `FirstTubeId` int(10) NOT NULL,
  `LastTubeId` int(10) NOT NULL,
  PRIMARY KEY (`Id`),
  UNIQUE KEY `TransactionKey_UNIQUE` (`TransactionKey`),
  KEY `fk_ShippingRequests_1` (`ContactId`),
  KEY `fk_ShippingRequests_2` (`ExpertiseId`),
  KEY `fk_ShippingRequests_3` (`Uid`)
) ENGINE=InnoDB AUTO_INCREMENT=634 DEFAULT CHARSET=latin1 COMMENT='Contains the shipping request done by the DRUPAL System';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Shippings`
--

DROP TABLE IF EXISTS `Shippings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Shippings` (
  `Id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `ShippingRequestId` int(10) unsigned NOT NULL,
  `Uploaded` datetime DEFAULT NULL,
  `XlsFile` varchar(200) DEFAULT NULL,
  `Count` int(10) unsigned DEFAULT NULL,
  `Status` enum('raw','cooking','done') NOT NULL DEFAULT 'raw',
  PRIMARY KEY (`Id`),
  KEY `fk_Shippings_1` (`ShippingRequestId`)
) ENGINE=InnoDB AUTO_INCREMENT=166 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Sync_Transfer_Log`
--

DROP TABLE IF EXISTS `Sync_Transfer_Log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Sync_Transfer_Log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `temp_table` varchar(100) DEFAULT NULL,
  `action` enum('Start','DTN taxa','ZFMK data','BOLD data','External DC data') DEFAULT NULL,
  `dtn_taxa` int(10) unsigned DEFAULT NULL,
  `zfmk_specimens` int(10) unsigned DEFAULT NULL,
  `bold_specimens` int(10) unsigned DEFAULT NULL,
  `external_specimens` int(10) unsigned DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `TransferLog`
--

DROP TABLE IF EXISTS `TransferLog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TransferLog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `direction` varchar(10) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `UserExpertise`
--

DROP TABLE IF EXISTS `UserExpertise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserExpertise` (
  `Uid` int(10) unsigned NOT NULL,
  `id_Expertise` int(11) unsigned NOT NULL,
  KEY `fk_RelUserExpertise_3` (`Uid`),
  KEY `fk_RelUserExpertise_4` (`id_Expertise`),
  KEY `idx_uid` (`Uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserExpertise`
--

LOCK TABLES `UserExpertise` WRITE;
/*!40000 ALTER TABLE `UserExpertise` DISABLE KEYS */;
INSERT INTO `UserExpertise` VALUES (42,26779),
(42,26781),
(42,26783),
(42,26784),
(42,26789),
(42,26790),
(42,26793),
(42,26798),
(42,26804),
(42,26806),
(42,26807),
(42,26810),
(42,26811),
(42,26813),
(42,26816),
(42,26817),
(42,26821),
(42,26822),
(42,26823),
(42,26824),
(42,26826),
(42,26827),
(42,26828),
(42,26848);
/*!40000 ALTER TABLE `UserExpertise` ENABLE KEYS */;
UNLOCK TABLES;
--
-- Table structure for table `UserExpertiseRequest`
--

DROP TABLE IF EXISTS `UserExpertiseRequest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserExpertiseRequest` (
  `Uid` int(10) unsigned NOT NULL,
  `id_Expertise` int(11) unsigned NOT NULL,
  `RequestDate` datetime NOT NULL,
  PRIMARY KEY (`Uid`,`id_Expertise`),
  KEY `fk_ExpertiseRequests_3` (`Uid`),
  KEY `fk_ExpertiseRequests_4` (`id_Expertise`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `UserRole`
--

DROP TABLE IF EXISTS `UserRole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `UserRole` (
  `uid` int(10) unsigned NOT NULL,
  `rid` int(10) unsigned NOT NULL,
  KEY `idx_uid` (`uid`),
  KEY `idx_rid` (`rid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UserRole`
--

LOCK TABLES `UserRole` WRITE;
/*!40000 ALTER TABLE `UserRole` DISABLE KEYS */;
INSERT INTO `UserRole` VALUES (42,2),(42,4),(42,5);
/*!40000 ALTER TABLE `UserRole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kontakt`
--

DROP TABLE IF EXISTS `kontakt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kontakt` (
  `kontaktid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `taxa` varchar(100) DEFAULT NULL,
  `institut` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `user_id` int(10) unsigned DEFAULT NULL,
  `lang` enum('de','en') DEFAULT 'de',
  PRIMARY KEY (`kontaktid`)
) ENGINE=InnoDB AUTO_INCREMENT=125 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kontakt`
--

LOCK TABLES `kontakt` WRITE;
/*!40000 ALTER TABLE `kontakt` DISABLE KEYS */;
INSERT INTO `kontakt` VALUES (7,'Arachnida Expert','Arachnida','Institute','email@somwhere.ct',42,'de'),
( 9,'Auchenorrhyncha Expert','Auchenorrhyncha','Institute','email@somwhere.ct',42,'de'),
(17,'Crustacea Expert','Crustacea','Institute','email@somwhere.ct',42,'de'),
(20,'Diptera Expert','Diptera','Institute','email@somwhere.ct',42,'de'),
(25,'Heteroptera Expert','Heteroptera','Institute','email@somwhere.ct',42,'de'),
(34,'Mecoptera Expert','Mecoptera','Institute','email@somwhere.ct',42,'de'),
(35,'Megaloptera Expert','Megaloptera','Institute','email@somwhere.ct',42,'de'),
(42,'Neuroptera Expert','Neuroptera','Institute','email@somwhere.ct',42,'de'),
(45,'Phthiraptera Expert','Phthiraptera','Institute','email@somwhere.ct',42,'de'),
(50,'Pscocoptera Expert','Pscocoptera','Institute','email@somwhere.ct',42,'de'),
(52,'Rhaphidioptera Expert','Rhaphidioptera','Institute','email@somwhere.ct',42,'de'),
(53,'Siphonaptera Expert','Siphonaptera','Institute','email@somwhere.ct',42,'de'),
(56,'Strepsiptera Expert','Strepsiptera','Institute','email@somwhere.ct',42,'de'),
(58,'Tardigrada Expert','Tardigrada','Institute','email@somwhere.ct',42,'de'),
(59,'Thysanoptera Expert','Thysanoptera','Institute','email@somwhere.ct',42,'de'),
(61,'Zoraptera Expert','Zoraptera','Institute','email@somwhere.ct',42,'de');
/*!40000 ALTER TABLE `kontakt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `newsletter`
--

DROP TABLE IF EXISTS `newsletter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `newsletter` (
  `type` int(11) NOT NULL,
  `email` varchar(45) NOT NULL,
  `uid` int(11) DEFAULT NULL,
  PRIMARY KEY (`type`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `uid` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `pass` varchar(255) DEFAULT NULL,
  `mail` varchar(45) NOT NULL,
  `phone` varchar(45) DEFAULT NULL,
  `salutation` varchar(45) DEFAULT NULL,
  `title` varchar(45) DEFAULT NULL,
  `vorname` varchar(45) NOT NULL,
  `nachname` varchar(45) NOT NULL,
  `role` int(10) unsigned DEFAULT NULL,
  `organisation` tinytext,
  `street` varchar(45) DEFAULT NULL,
  `zip` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `country` varchar(45) DEFAULT NULL,
  `passwd_drupal` varchar(128) DEFAULT NULL,
  `language` varchar(45) DEFAULT NULL,
  `referenzen` longtext,
  `expertiseAngaben` longtext,
  `termsofuse` enum('0','1') DEFAULT '1',
  `status` varchar(2) NOT NULL DEFAULT '0',
  `public` varchar(2) NOT NULL DEFAULT '0',
  `created` datetime DEFAULT NULL COMMENT 'Registration date',
  `access` datetime DEFAULT NULL COMMENT 'Last access',
  `login` datetime DEFAULT NULL COMMENT 'First login',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=782 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (42,'example_taxon_coordinator','sha-encrypted_passwd-here','email',NULL,'Herr',NULL,'Lastname','Surname',2,'Affiliation','Street','ZIP','Bonn','Country',NULL,'de','References',NULL,'1','1','1','2016-01-01 12:00:01','2016-01-01 12:00:01','2016-01-01 12:00:01');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
