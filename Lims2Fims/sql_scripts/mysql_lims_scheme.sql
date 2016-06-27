-- MySQL dump 10.13  Distrib 5.5.47, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: lims
-- ------------------------------------------------------
-- Server version	5.5.47-0ubuntu0.14.04.1

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
-- Current Database: `lims`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `lims` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `lims`;

--
-- Table structure for table `L2FcheckConsensus`
--

DROP TABLE IF EXISTS `L2FcheckConsensus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L2FcheckConsensus` (
  `id` int(10) unsigned NOT NULL,
  `status` varchar(999) DEFAULT NULL,
  `note` varchar(999) DEFAULT NULL,
  `workflow_id` int(10) DEFAULT NULL,
  `extraction_id` varchar(999) DEFAULT NULL,
  `ass_notes` longtext,
  `plate_suffix` varchar(999) DEFAULT NULL,
  `consensus` longtext,
  `consensus_length` int(10) DEFAULT NULL,
  `gen_parentfolder_id` int(11) DEFAULT NULL,
  `gen_nameparentfolder` varchar(255) DEFAULT NULL,
  `gen_consensusfolder_id` int(11) DEFAULT NULL,
  `gen_ann_doc_id` int(11) DEFAULT NULL,
  `gen_extraction_id` varchar(999) DEFAULT NULL,
  `gen_workflow` varchar(999) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `L2FchkDC`
--

DROP TABLE IF EXISTS `L2FchkDC`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L2FchkDC` (
  `id` int(10) unsigned NOT NULL,
  `status` varchar(999) DEFAULT NULL,
  `note` varchar(999) DEFAULT NULL,
  `ass_consensus_length` int(10) DEFAULT NULL,
  `DC_consensus_length` int(10) DEFAULT NULL,
  `ass_consensus` varchar(10000) DEFAULT NULL,
  `DC_consensus` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `L2FscTable`
--

DROP TABLE IF EXISTS `L2FscTable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `L2FscTable` (
  `id` int(10) unsigned NOT NULL,
  `status` varchar(999) DEFAULT NULL,
  `note` varchar(999) DEFAULT NULL,
  `workflow_id` int(10) DEFAULT NULL,
  `extraction_id` varchar(999) DEFAULT NULL,
  `ass_notes` varchar(10000) DEFAULT NULL,
  `plate_suffix` varchar(999) DEFAULT NULL,
  `gen_parentfolder_id` int(11) DEFAULT NULL,
  `gen_nameparentfolder` varchar(255) DEFAULT NULL,
  `gen_consensusfolder_id` int(11) DEFAULT NULL,
  `gen_ann_doc_id` int(11) DEFAULT NULL,
  `gen_extraction_id` varchar(999) DEFAULT NULL,
  `gen_workflow` varchar(999) DEFAULT NULL,
  `gen_name` varchar(999) DEFAULT NULL,
  `consensus_length` int(10) DEFAULT NULL,
  `consensus` varchar(10000) DEFAULT NULL,
  `gen_consensus` varchar(10000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Transfer_Extr_Plate_Name`
--

DROP TABLE IF EXISTS `Transfer_Extr_Plate_Name`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Transfer_Extr_Plate_Name` (
  `id` int(10) unsigned NOT NULL,
  `transferDate` datetime DEFAULT NULL,
  `status` varchar(999) DEFAULT NULL,
  `note` varchar(999) DEFAULT NULL,
  `sampleId` varchar(45) DEFAULT NULL,
  `collSpecId` int(10) unsigned NOT NULL,
  `plateId` int(10) unsigned NOT NULL,
  `plateLocation` int(10) unsigned NOT NULL,
  `plateSize` int(11) unsigned NOT NULL,
  `plateName` varchar(64) DEFAULT NULL,
  `concatPlateNames` varchar(999) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `assembly_export_COI`
--

DROP TABLE IF EXISTS `assembly_export_COI`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `assembly_export_COI` (
  `id` int(10) unsigned NOT NULL,
  `exportDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `workflowId` int(10) unsigned NOT NULL,
  `workflowDate` date DEFAULT NULL,
  `extractionTblId` int(10) unsigned NOT NULL,
  `extractionId` varchar(45) DEFAULT NULL,
  `extractionDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwb_CollectionSpecimenId` int(10) unsigned NOT NULL,
  `sampleId` varchar(45) DEFAULT NULL,
  `status` varchar(999) DEFAULT NULL,
  `note` varchar(999) DEFAULT NULL,
  `assemDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `assemProgress` varchar(45) DEFAULT NULL,
  `assemTechnician` varchar(255) DEFAULT NULL,
  `assemNotes` longtext,
  `assemConsensus` longtext,
  `assemPlateSuffix` varchar(999) DEFAULT NULL,
  `assemContam` varchar(999) DEFAULT NULL,
  `assem_failure_reason_id` int(11) DEFAULT NULL,
  `assem_failure_reason` varchar(80) DEFAULT NULL,
  `assem_failure_detail` longtext,
  `locus` varchar(45) DEFAULT NULL,
  `pcrAnzahl` int(11) DEFAULT NULL,
  `pcrId` int(11) DEFAULT NULL,
  `pcrDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pcrPrName` varchar(64) DEFAULT NULL,
  `pcrPrSequence` varchar(999) DEFAULT NULL,
  `pcrRevPrName` varchar(64) DEFAULT NULL,
  `pcrRevPrSequence` varchar(999) DEFAULT NULL,
  `cycleSeqForwAnzahl` int(11) DEFAULT NULL,
  `cycleSeqForwId` int(11) DEFAULT NULL,
  `cycleSeqForwPrimerName` varchar(64) DEFAULT NULL,
  `cycleSeqForwPrimerSequence` varchar(999) DEFAULT NULL,
  `cycleSeqForwTraceAnzahl` int(11) DEFAULT NULL,
  `cycleSeqForwTraceId` int(10) DEFAULT NULL,
  `cycleSeqForwTraceName` varchar(999) DEFAULT NULL,
  `cycleSeqForwTechnician` varchar(90) DEFAULT NULL,
  `cycleSeqForwDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `cycleSeqForwTraceFormat` varchar(45) DEFAULT NULL,
  `cycleSeqRevAnzahl` int(11) DEFAULT NULL,
  `cycleSeqRevId` int(11) DEFAULT NULL,
  `cycleSeqRevPrimerName` varchar(64) DEFAULT NULL,
  `cycleSeqRevPrimerSequence` varchar(999) DEFAULT NULL,
  `cycleSeqRevTraceAnzahl` int(11) DEFAULT NULL,
  `cycleSeqRevTraceId` int(10) DEFAULT NULL,
  `cycleSeqRevTraceName` varchar(999) DEFAULT NULL,
  `cycleSeqRevTechnician` varchar(90) DEFAULT NULL,
  `cycleSeqRevDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `cycleSeqRevTraceFormat` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ixdwb_CollectionSpecimenId` (`dwb_CollectionSpecimenId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;



--
-- Table structure for table `extraction_export`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `extraction_export` (
  `id` int(10) unsigned NOT NULL,
  `workflowId` int(10) unsigned NOT NULL,
  `dwb_CollectionSpecimenId` int(10) unsigned NOT NULL,
  `sampleId` varchar(45) DEFAULT NULL,
  `extractionId` varchar(45) DEFAULT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(999) DEFAULT NULL,
  `note` varchar(999) DEFAULT NULL,
  `locus` varchar(45) DEFAULT NULL,
  `pcrPrName` varchar(64) DEFAULT NULL,
  `pcrPrSequence` varchar(999) DEFAULT NULL,
  `pcrRevPrName` varchar(64) DEFAULT NULL,
  `pcrRevPrSequence` varchar(999) DEFAULT NULL,
  `cycleSeqForwPrimerName` varchar(64) DEFAULT NULL,
  `cycleSeqForwPrimerSequence` varchar(999) DEFAULT NULL,
  `cycleSeqForwTraceId` int(10) DEFAULT NULL,
  `cycleSeqForwTraceName` varchar(999) DEFAULT NULL,
  `cycleSeqRevPrimerName` varchar(64) DEFAULT NULL,
  `cycleSeqRevPrimerSequence` varchar(999) DEFAULT NULL,
  `cycleSeqRevTraceId` int(10) DEFAULT NULL,
  `cycleSeqRevTraceName` varchar(999) DEFAULT NULL,
  `assemDate` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `assemProgress` varchar(45) DEFAULT NULL,
  `assemTechnician` varchar(255) DEFAULT NULL,
  `assemConsensus` longtext,
  PRIMARY KEY (`id`,`workflowId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `sampleId_numeric`
--

DROP TABLE IF EXISTS `sampleId_numeric`;
/*!50001 DROP VIEW IF EXISTS `sampleId_numeric`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `sampleId_numeric` (
  `sampleId` tinyint NOT NULL,
  `sampleId_numeric` tinyint NOT NULL,
  `extractionId` tinyint NOT NULL,
  `plate` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Dumping routines for database 'lims'
--
/*!50003 DROP PROCEDURE IF EXISTS `checkAlreadyPassed` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `checkAlreadyPassed`
DELIMITER ;;
CREATE PROCEDURE `checkAlreadyPassed`()
main_block: Begin
/**************** Aenderungen *********************************************************/
/* V2  04.11.2015 Aendere longtext Typ in varchar(20000)                              */
/* V3  04.11.2015 Speichere gefundene Id in note Feld ab                              */
/**************************************************************************************/
  Declare param_max_anzahl int(10);  -- maximale Durchlaeufe der Verarbeitungsloop
  /* Declares fuer Tabelle assembly_export_COI */
  Declare e_id int(10);
  Declare e_dwb_CollectionSpecimenId int(10);
  Declare e_assemConsensus varchar(20000);

  Declare v_zaehler int;  -- verarbeitete Eintraege
  Declare v_count int;  -- Hilfsvariable fuer gefundene Eintraege
  Declare v_done int;   -- Ende der Ergebnismenge
  Declare v_id int(10);   -- gefundene Id

  Declare c_extr Cursor For Select id, dwb_CollectionSpecimenId, assemConsensus
    From assembly_export_COI
    Where status='prepCheck'
    Order By id;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set v_zaehler = 0;
  Set v_count  = 0;
  Set v_done   = 0;
  Set param_max_anzahl = 10000;  -- maximale Durchlaeufe der Verarbeitungsloop
  Set v_id = 0;

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into e_id, e_dwb_CollectionSpecimenId, e_assemConsensus;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_zaehler = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
   Set v_zaehler = v_zaehler + 1;

    Select Count(id), id into v_count, v_id From assembly_export_COI
      Where dwb_CollectionSpecimenId=e_dwb_CollectionSpecimenId
        and (status='ok' or status='prepared' or status='prepCheck')
        and assemConsensus=e_assemConsensus and id < e_id;
    If v_count>0 Then
--      Update assembly_export_COI Set status='ignore_already_passed_less' Where id=e_id;
      Update assembly_export_COI Set status='ignore_already_passed_less', note=CONCAT('less id=',(CAST(v_id AS CHAR)))
        Where id=e_id;
      Iterate l_fetch_data;
    End If;

    Select Count(id), id into v_count, v_id From assembly_export_COI
      Where dwb_CollectionSpecimenId=e_dwb_CollectionSpecimenId
        and (status='ok' or status='prepared')
        and assemConsensus=e_assemConsensus and id > e_id;
    If v_count>0 Then
--      Update assembly_export_COI Set status='ignore_already_passed_greater' Where id=e_id;
      Update assembly_export_COI Set status='ignore_already_passed_greater', note=CONCAT('greater, id=',(CAST(v_id AS CHAR)))
        Where id=e_id;
      Iterate l_fetch_data;
    End If;

    Update assembly_export_COI Set status='prepared' Where id=e_id;

  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_zaehler AS CHAR)) );

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `checkConsensus` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `checkConsensus`;

DELIMITER ;;
CREATE PROCEDURE `checkConsensus`(IN p_start_id int(10) )
Begin
/**************** Aenderungen *********************************************************/
/*                                                            */
/**************************************************************************************/
  Declare param_max_anzahl int(10);  -- maximale Durchlaeufe der Verarbeitungsloop
  Declare v_id int(10);  -- id der assembly Tabelle
  Declare v_count int;   -- Zeilen Zaehler
  Declare v_done int;    -- Ende der Ergebnismenge

  Declare c_extr Cursor For Select id
    From assembly
    Where id>=p_start_id
    Order By id Limit 1000;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set param_max_anzahl = 500;  -- maximale Durchlaeufe der Verarbeitungsloop
  Set v_count  = 0;
  Set v_done   = 0;

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into v_id;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_count = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
    Set v_count = v_count+1;

    Call checkConsensusData(v_id);

  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_count AS CHAR)) );

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `checkConsensusData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `checkConsensusData`;

DELIMITER ;;
CREATE PROCEDURE `checkConsensusData`(IN p_ass_id int(10) )
main_block: Begin
/*******************************************************************************************************/
/* Programmlogik                                                                                       */
/*   Suche Eintrag in der Tabelle assembly. Mache nichts, falls nicht vorhanden.                       */
/*   Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly, notes Feld darf nicht leer sein. */
/*   Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly.                                  */
/*   Schneide _NW von Platten-Suffix ab.                                                               */
/*   Ermittle die ParentFolderId mit Hilfe des Platten-Suffix.                                         */
/*   Ermittle die ConsensusFolderId.                                                                   */
/*   Ueberpruefe die extraction_id                                                                     */
/*   Ueberpruefe die workflow_id                                                                       */
/*   Ueberpruefe die consensus Sequenz                                                                 */
/*   Schreibe Ergebnis in Tabelle L2FcheckConsensus                                               */
/*                                                                                                     */
/*******************************************************************************************************/
  /* Variable */
  Declare v_count int(10);           -- Anzahl Eintraege
  Declare v_error_indicator int(10); -- Fehler aufgetreten
  Declare v_ann_doc_id int(11);      -- Annotated Document Id
  Declare v_consensus LONGTEXT;      -- consensus aus Tabelle assembly
  Declare v_chars varchar(999);      -- Hilfsvariable
  Declare v_int1 int(10);             -- Hilfsvariable
  Declare v_int2 int(10);             -- Hilfsvariable
  Declare v_mapped int;               -- Hilfsvariable Suffixmapping


  /* Variable zum Aufruf der Prozedur ExtractInfo */
  Declare h_procRc int;
  Declare h_reason varchar(99);
  Declare h_assemContam varchar(999);
  Declare h_assemNotes varchar(999);


  /* Variable fuer Tabelle L2FcheckConsensus  */
  Declare t_id int(10);
  Declare t_status varchar(999);
  Declare t_note varchar(999);
  Declare t_workflow_id int(10);         -- workflow aus Tabelle assembly
  Declare t_extraction_id varchar(999);  -- extraction_id aus Tabelle assembly
  Declare t_ass_notes LONGTEXT;          -- notes aus Tabelle assembly
  Declare t_plate_suffix varchar(999);   -- Plattensuffix zur Bestimmung der parentfolder_id
  Declare t_consensus LONGTEXT;          -- consensus aus Tabelle assembly
  Declare t_consensus_length int(10);
  Declare t_gen_parentfolder_id int(11);    -- parentfolder_id aus Tabelle gbol_geneious.folder
  Declare t_gen_nameparentfolder varchar(255);
  Declare t_gen_consensusfolder_id int(11); -- consensusfolder_id aus Tabelle gbol_geneious.folder
  Declare t_gen_ann_doc_id int(11);         -- id aus Tabelle gbol_geneious.annotated_document
  Declare t_gen_extraction_id varchar(999); -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document
  Declare t_gen_workflow varchar(999);      -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document

  Set t_id = p_ass_id;
  Set t_status = 'Fehler';
  Set t_note = 'Interner Fehler';
  Set t_workflow_id = 0;
  Set t_extraction_id = 'leer';
  Set t_ass_notes = 'leer';
  Set t_plate_suffix = 'leer';
  Set t_consensus = 'leer';
  Set t_consensus_length = 0;
  Set t_gen_parentfolder_id = 0;
  Set t_gen_nameparentfolder = 'leer';
  Set t_gen_consensusfolder_id = 0;
  Set t_gen_ann_doc_id = 0;
  Set t_gen_extraction_id = 'leer';
  Set t_gen_workflow = 'leer';      -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document

  Set v_error_indicator = 0; -- Noch ist kein Fehler aufgetreten

  /* Suche Eintrag in der Tabelle assembly */
  Select count(*), workflow, extraction_id, notes, consensus, Length(consensus)
    into v_count, t_workflow_id, t_extraction_id, t_ass_notes, t_consensus, t_consensus_length
    from assembly Where id=t_id;
  If v_count=0 Then
    Leave main_block;
  End If;

  /* Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly, notes Feld darf nicht leer sein */
  If ((t_ass_notes IS NULL) OR (Length(t_ass_notes) = 0)) Then
    Set t_status = 'Fehler';
    Set t_note = 'Notes Feld der Tabelle Assembly ist leer';
    Set v_error_indicator = 1; -- Fehler aufgetreten
  End If;

  /* Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly */
  If v_error_indicator=0 Then
    Set v_mapped = 0; -- Assembly notes Feld nicht auf Plattensuffix abgebildet
    Call mapSuffix(t_ass_notes, t_plate_suffix, v_mapped);
    If v_mapped = 0 Then
      Call ExtractInfo(t_ass_notes, 'P:', 'C:', h_procRc, h_reason, t_plate_suffix, h_assemContam, h_assemNotes);
      If (h_procRc > 0) Then
        Set t_status = 'Fehler';
        Set t_note = CONCAT('ExtractInfo_Reason=', h_reason, ';Notes=', t_ass_notes);
        Set v_error_indicator = 1; -- Fehler aufgetreten
      End If;
    End If;
  End If;

  /* Schneide _NW von Platten-Suffix ab */
  If v_error_indicator=0 Then
    Set v_int1=Locate('_NW', t_plate_suffix);
    If v_int1>1 then
      Set t_plate_suffix=Substring(t_plate_suffix,1,v_int1-1);
    End if;
  End If;

  /* Ermittle die ParentFolderId mit Hilfe von Platten-Suffix */
  If v_error_indicator=0 Then
    Select count(*), id, name
      Into v_count, t_gen_parentfolder_id, t_gen_nameparentfolder
      From gbol_geneious.folder
      Where name like CONCAT('GBOL\\', t_plate_suffix, '%') and name not like CONCAT('GBOL\\', t_plate_suffix, '\\_%')
        and name not like CONCAT('GBOL\\', t_plate_suffix, '-%');
    -- Where name like 'GBOL\_0505%' and name not like 'GBOL\_0505\_%' and name not like 'GBOL\_0505-%';  -- id=14215 name=GBOL_0505 (Col - Het)
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ermittle_Parentfolderid, Id ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_parentfolder_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Parentfolderid is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ermittle die ConsensusFolderId */
  If v_error_indicator=0 Then
    Select count(*), id
      Into v_count, t_gen_consensusfolder_id
      From gbol_geneious.folder
      Where parent_folder_id=t_gen_parentfolder_id and name='Consensus';  -- id=14219
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ermittle_Consensusfolder_id, Id ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_consensusfolder_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Consensusfolder_id is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ueberpruefe die extraction_id */
  If v_error_indicator=0 Then
    Set t_gen_extraction_id=CONCAT('<XML%<extraction.extractionId>', t_extraction_id, '</extraction.extractionId>%');
    Select count(*), id
      Into v_count, t_gen_ann_doc_id
      From gbol_geneious.annotated_document
      Where folder_id=t_gen_consensusfolder_id
        And plugin_document_xml like t_gen_extraction_id; -- 1 row id=564758
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ueberpruefe extraction_id, DocumentId ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_ann_doc_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Extraction, Annotated_document_id is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ueberpruefe die workflow_id */
  If v_error_indicator=0 Then
    Set t_gen_workflow=CONCAT('<XML%<workflowName>COI_workflow', CAST(t_workflow_id AS CHAR), '</workflowName>%' );
    Select count(*), id
      Into v_count, v_ann_doc_id
      From gbol_geneious.annotated_document
      Where folder_id=t_gen_consensusfolder_id
        And plugin_document_xml like t_gen_workflow; -- 1 row id=564758
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ueberpruefe workflow, DocumentId ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (v_ann_doc_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Workflow, Annotated_document_id is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_ann_doc_id <> v_ann_doc_id) Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Workflow, Annotated_document_id=', CAST(v_ann_doc_id AS CHAR),
       'is ungleich extraction_doc_id=', CAST(t_gen_ann_doc_id AS CHAR));
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ueberpruefe die consensus Sequenz */
  If v_error_indicator=0 Then
    Set v_consensus=CONCAT('<XML%<charSequence>', t_consensus, '</charSequence>%');
    Select count(*), id
      Into v_count, v_ann_doc_id
      From gbol_geneious.annotated_document
      Where folder_id=t_gen_consensusfolder_id and id=t_gen_ann_doc_id
        And plugin_document_xml like v_consensus; -- 1 row id=564758
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ueberpruefe Consensus, Daten stimmen nicht ueberein, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  If v_error_indicator=0 Then
    Set t_status = 'ok';
    Set t_note = 'consensusCheck ok';
  End if;  -- v_error_indicator=0

  /* Schreibe Ergebnis in Tabelle L2FcheckConsensus */
  Select Count(id) into v_count From L2FcheckConsensus Where id = t_id;
  If v_count=0 Then
    /* insert, da Eintrag nicht vorhanden */
    -- Insert Into L2FcheckConsensus (id, note, ...) Values (1002, 'noteABC123', ...);
    -- Set t_note = 'Insert alles ok';
    Insert Into L2FcheckConsensus
     (id, status, note, workflow_id, extraction_id, ass_notes, plate_suffix, consensus, consensus_length,
      gen_parentfolder_id, gen_nameparentfolder, gen_consensusfolder_id, gen_ann_doc_id, gen_extraction_id, gen_workflow)
     Values (t_id, t_status, t_note, t_workflow_id, t_extraction_id, t_ass_notes, t_plate_suffix, t_consensus, t_consensus_length,
      t_gen_parentfolder_id, t_gen_nameparentfolder, t_gen_consensusfolder_id, t_gen_ann_doc_id, t_gen_extraction_id, t_gen_workflow);
  Else
    /* update, da Eintrag vorhanden */
    -- Update L2FcheckConsensus Set status=..., note=... Where id=t_id;
    -- Set t_note = 'Update alles ok';
    Update L2FcheckConsensus
     Set status=t_status, note=t_note, workflow_id=t_workflow_id, extraction_id=t_extraction_id, ass_notes=t_ass_notes,
      plate_suffix=t_plate_suffix, consensus=t_consensus, consensus_length=t_consensus_length, gen_parentfolder_id=t_gen_parentfolder_id,
      gen_nameparentfolder=t_gen_nameparentfolder, gen_consensusfolder_id=t_gen_consensusfolder_id,
      gen_ann_doc_id=t_gen_ann_doc_id, gen_extraction_id=t_gen_extraction_id, gen_workflow=t_gen_workflow
     Where id=t_id;
  End If;

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `checkConsPlate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `checkConsPlate`;

DELIMITER ;;
CREATE PROCEDURE `checkConsPlate`(IN p_assembly_notes Longtext )
Begin
/**************** Aenderungen *********************************************************/
/*                                                            */
/**************************************************************************************/
  Declare param_max_anzahl int(10);  -- maximale Durchlaeufe der Verarbeitungsloop
  Declare v_id int(10);  -- id der assembly Tabelle
  Declare v_count int;   -- Zeilen Zaehler
  Declare v_done int;    -- Ende der Ergebnismenge

  Declare c_extr Cursor For Select id
    From assembly
    Where notes=p_assembly_notes
    Order By id Limit 1000;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set param_max_anzahl = 500;  -- maximale Durchlaeufe der Verarbeitungsloop
  Set v_count  = 0;
  Set v_done   = 0;

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into v_id;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_count = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
    Set v_count = v_count+1;

    Call checkConsensusData(v_id);

  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_count AS CHAR)) );

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `deleteEntries_COI` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `deleteEntries_COI`;

DELIMITER ;;
CREATE PROCEDURE `deleteEntries_COI`()
Begin
  Declare v_id int(10);
  Declare v_status varchar(999);
  Declare v_count int;
  Declare v_done int;

  Declare c_select Cursor For Select ae.id From assembly_export_COI as ae
    Where (ae.id Not In (SELECT id From assembly)) And ae.status<>'deleted' AND ae.status<>'delete' Order By ae.id;


  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set v_status = 'new';
  Set v_count  = 0;
  Set v_done   = 0;

  Open c_select;

  Repeat
    Fetch c_select Into v_id;
    If Not v_done Then

          Update assembly_export_COI Set status='delete' Where Id=v_id;
          Set v_count = v_count+1;

    End If;
  Until v_done End Repeat;
  Close c_select;

  Select CONCAT('Zeilengeloescht=',(CAST(v_count AS CHAR)));
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ExtractInfo` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `ExtractInfo`;
DELIMITER ;;
CREATE PROCEDURE `ExtractInfo`(IN p_strIn varchar(20000), IN p_key1 varchar(99), IN p_key2 varchar(99),
  OUT p_procRc int, OUT p_reason varchar(99), OUT p_value1 varchar(999), OUT p_value2 varchar(999), OUT p_prefix varchar(999) )
main_block: Begin
/********************************************************/
/* V2 04.11.2015 Aendere longtext Typ in varchar(20000) */
/********************************************************/
  Declare v_length_strIn int;
  Declare v_locate_key1  int;
  Declare v_length_key1  int;
  Declare v_locate_key2  int;
  Declare v_length_key2  int;
  Declare v_mehrfach int;  -- gesuchter Key kommt mehrfach vor

  Set p_procRc = 8;
  Set p_reason = 'Fehler';
  Set p_value1 = 'leer';
  Set p_value2 = 'leer';
  Set p_prefix = 'leer';

  Set v_length_strIn = Length(p_strIn);
  If (v_length_strIn = 0) Then
	Set p_procRc = 0;
	Set p_reason = 'Leerer EingangsString';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;
  If (v_length_strIn > 999) Then
	Set p_procRc = 8;
	Set p_reason = 'EingabeString ist laenger als 999';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;

  Set v_length_key1 = Length(p_key1);
  If (v_length_key1 = 0) Then
	Set p_procRc = 8;
	Set p_reason = 'Leerer Key1String';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;

  Set v_length_key2 = Length(p_key2);
  If (v_length_key2 = 0) Then
	Set p_procRc = 8;
	Set p_reason = 'Leerer Key2String';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;

  Set v_locate_key1 = LOCATE(p_key1, p_strIn);
  Set v_locate_key2 = LOCATE(p_key2, p_strIn);
  -- Select CONCAT('v_locate_key1=',(CAST(v_locate_key1 AS CHAR)),';v_locate_key2=',(CAST(v_locate_key2 AS CHAR)) );

  If ((v_locate_key1=0) And (v_locate_key2=0)) Then
    /* Eingabestring enthaelt keinen Key */
    Set p_procRc = 0;
    Set p_reason = 'EingabeString enthaelt keinen Key';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = TRIM(p_strIn);
    If (Length(p_prefix)=0) Then
      Set p_prefix = 'leer';
    End if;
    Leave main_block;
  End if;  -- Eingabestring enthaelt keinen Key

  If ((v_locate_key1>0) And (v_locate_key2=0)) Then
    /* Eingabestring enthaelt nur Key1 */
    Set v_mehrfach = LOCATE(p_Key1, p_strIn, v_locate_key1 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key1 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    Set p_value2 = 'leer';

    If (v_locate_key1 = 1) then
      Set p_prefix = 'leer';
    Else
      Set p_prefix = TRIM(Substring(p_strIn, 1, v_locate_key1-1));
      If (Length(p_prefix)=0) Then
        Set p_prefix = 'leer';
      End if;
    End if;

    If (v_length_strIn < (v_locate_key1 + v_length_key1)) then
      Set p_value1 = 'leer';
    Else
      Set p_value1 = Trim(Substring(p_strIn, v_locate_key1+v_length_key1));
      If (Length(p_value1)=0) Then
        Set p_value1 = 'leer';
      End if;
    End if;
    Set p_procRc = 0;
    Set p_reason = 'Key1information extrahiert';
    Leave main_block;

  End if;  -- Eingabestring enthaelt nur Key1

  If ((v_locate_key1=0) And (v_locate_key2>0)) Then
    /* Eingabestring enthaelt nur Key2 */
    Set v_mehrfach = LOCATE(p_Key2, p_strIn, v_locate_key2 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key2 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    Set p_value1 = 'leer';

    If (v_locate_key2 = 1) then
      Set p_prefix = 'leer';
    Else
      Set p_prefix = Trim(Substring(p_strIn, 1, v_locate_key2-1));
      If (Length(p_prefix)=0) Then
        Set p_prefix = 'leer';
      End if;
    End if;

    If (v_length_strIn < (v_locate_key2 + v_length_key2)) then
      Set p_value2 = 'leer';
    Else
      Set p_value2 = Trim(Substring(p_strIn, v_locate_key2+v_length_key2));
      If (Length(p_value2)=0) Then
        Set p_value2 = 'leer';
      End if;
    End if;
    Set p_procRc = 0;
    Set p_reason = 'Key2information extrahiert';
    Leave main_block;
  End if;  -- Eingabestring enthaelt nur Key2


  If ((v_locate_key1>0) And (v_locate_key2>0)) Then
    /* Eingabestring enthaelt Key1 und Key2 */
    Set v_mehrfach = LOCATE(p_Key1, p_strIn, v_locate_key1 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key1 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    Set v_mehrfach = LOCATE(p_Key2, p_strIn, v_locate_key2 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key2 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    If (v_locate_key1 < v_locate_key2) Then
      If (v_locate_key1 = 1) then
        Set p_prefix = 'leer';
      Else
        Set p_prefix = Trim(Substring(p_strIn, 1, v_locate_key1-1));
        If (Length(p_prefix)=0) Then
          Set p_prefix = 'leer';
        End if;
      End if;

      If ((v_locate_key1 + v_length_key1) = v_locate_key2) then
        Set p_value1 = 'leer';
      Else
        Set p_value1 = Trim(Substring(p_strIn, v_locate_key1+v_length_key1, v_locate_key2-v_locate_key1-v_length_key1));
        If (Length(p_value1)=0) Then
          Set p_value1 = 'leer';
        End if;
      End if;

      If (v_length_strIn < (v_locate_key2 + v_length_key2)) then
        Set p_value2 = 'leer';
      Else
        Set p_value2 = Trim(Substring(p_strIn, v_locate_key2+v_length_key2));
        If (Length(p_value2)=0) Then
          Set p_value2 = 'leer';
        End if;
      End if;
    Else  -- v_locate_key1 > v_locate_key2
      If (v_locate_key2 = 1) then
        Set p_prefix = 'leer';
      Else
        Set p_prefix = Trim(Substring(p_strIn, 1, v_locate_key2-1));
        If (Length(p_prefix)=0) Then
          Set p_prefix = 'leer';
        End if;
      End if;

      If ((v_locate_key2 + v_length_key2) = v_locate_key1) then
        Set p_value2 = 'leer';
      Else
        Set p_value2 = Trim(Substring(p_strIn, v_locate_key2+v_length_key2, v_locate_key1-v_locate_key2-v_length_key2));
        If (Length(p_value2)=0) Then
          Set p_value2 = 'leer';
        End if;
      End if;

      If (v_length_strIn < (v_locate_key1 + v_length_key1)) then
        Set p_value1 = 'leer';
      Else
        Set p_value1 = Trim(Substring(p_strIn, v_locate_key1+v_length_key1));
        If (Length(p_value1)=0) Then
          Set p_value1 = 'leer';
        End if;
      End if;
    End if; -- v_locate_key1 > v_locate_key2
    Set p_procRc = 0;
    Set p_reason = 'Key1Information und Key2information extrahiert';
    Leave main_block;

  End if;  -- Eingabestring enthaelt Key1 und Key2

-- Select CONCAT('Platte=',(CAST(v_count AS CHAR)),' neue Fehler=',(CAST(v_error AS CHAR)) );
-- Select CONCAT('Notes=', p_notes, ';Platte=', p_platte, ';Contamination=', p_contamination, ';Note=', p_note);
--  Select CONCAT('Notes=', p_notes, ';Platte=', p_platte, ';v_locate_platte=', CAST(v_locate_platte AS CHAR),
--    ';v_length_notes=', CAST(v_length_notes AS CHAR) );
  Set p_procRc = 0;
  Set p_reason = 'Internal Error';
  Set p_value1 = 'leer';
  Set p_value2 = 'leer';
  Set p_prefix = 'leer';
  Leave main_block;

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `ExtractInfoTest` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `ExtractInfoTest`;
DELIMITER ;;
CREATE PROCEDURE `ExtractInfoTest`(IN p_strIn longtext, IN p_key1 varchar(99), IN p_key2 varchar(99),
  OUT p_procRc int, OUT p_reason varchar(99), OUT p_value1 varchar(999), OUT p_value2 varchar(999), OUT p_prefix varchar(999) )
main_block: Begin
/**************** procedure TestParseNotes ****************/
  Declare v_length_strIn int;
  Declare v_locate_key1  int;
  Declare v_length_key1  int;
  Declare v_locate_key2  int;
  Declare v_length_key2  int;
  Declare v_mehrfach int;  -- gesuchter Key kommt mehrfach vor

  Set p_procRc = 8;
  Set p_reason = 'Fehler';
  Set p_value1 = 'leer';
  Set p_value2 = 'leer';
  Set p_prefix = 'leer';

  Set v_length_strIn = Length(p_strIn);
  If (v_length_strIn = 0) Then
	Set p_procRc = 0;
	Set p_reason = 'Leerer EingangsString';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;
  If (v_length_strIn > 999) Then
	Set p_procRc = 8;
	Set p_reason = 'EingabeString ist laenger als 999';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;

  Set v_length_key1 = Length(p_key1);
  If (v_length_key1 = 0) Then
	Set p_procRc = 8;
	Set p_reason = 'Leerer Key1String';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;

  Set v_length_key2 = Length(p_key2);
  If (v_length_key2 = 0) Then
	Set p_procRc = 8;
	Set p_reason = 'Leerer Key2String';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = 'leer';
    Leave main_block;
  End if;

  Set v_locate_key1 = LOCATE(p_key1, p_strIn);
  Set v_locate_key2 = LOCATE(p_key2, p_strIn);
  -- Select CONCAT('v_locate_key1=',(CAST(v_locate_key1 AS CHAR)),';v_locate_key2=',(CAST(v_locate_key2 AS CHAR)) );

  If ((v_locate_key1=0) And (v_locate_key2=0)) Then
    /* Eingabestring enthaelt keinen Key */
    Set p_procRc = 0;
    Set p_reason = 'EingabeString enthaelt keinen Key';
    Set p_value1 = 'leer';
    Set p_value2 = 'leer';
    Set p_prefix = TRIM(p_strIn);
    If (Length(p_prefix)=0) Then
      Set p_prefix = 'leer';
    End if;
    Leave main_block;
  End if;  -- Eingabestring enthaelt keinen Key

  If ((v_locate_key1>0) And (v_locate_key2=0)) Then
    /* Eingabestring enthaelt nur Key1 */
    Set v_mehrfach = LOCATE(p_Key1, p_strIn, v_locate_key1 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key1 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    Set p_value2 = 'leer';

    If (v_locate_key1 = 1) then
      Set p_prefix = 'leer';
    Else
      Set p_prefix = TRIM(Substring(p_strIn, 1, v_locate_key1-1));
      If (Length(p_prefix)=0) Then
        Set p_prefix = 'leer';
      End if;
    End if;

    If (v_length_strIn < (v_locate_key1 + v_length_key1)) then
      Set p_value1 = 'leer';
    Else
      Set p_value1 = Trim(Substring(p_strIn, v_locate_key1+v_length_key1));
      If (Length(p_value1)=0) Then
        Set p_value1 = 'leer';
      End if;
    End if;
    Set p_procRc = 0;
    Set p_reason = 'Key1information extrahiert';
    Leave main_block;

  End if;  -- Eingabestring enthaelt nur Key1

  If ((v_locate_key1=0) And (v_locate_key2>0)) Then
    /* Eingabestring enthaelt nur Key2 */
    Set v_mehrfach = LOCATE(p_Key2, p_strIn, v_locate_key2 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key2 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    Set p_value1 = 'leer';

    If (v_locate_key2 = 1) then
      Set p_prefix = 'leer';
    Else
      Set p_prefix = Trim(Substring(p_strIn, 1, v_locate_key2-1));
      If (Length(p_prefix)=0) Then
        Set p_prefix = 'leer';
      End if;
    End if;

    If (v_length_strIn < (v_locate_key2 + v_length_key2)) then
      Set p_value2 = 'leer';
    Else
      Set p_value2 = Trim(Substring(p_strIn, v_locate_key2+v_length_key2));
      If (Length(p_value2)=0) Then
        Set p_value2 = 'leer';
      End if;
    End if;
    Set p_procRc = 0;
    Set p_reason = 'Key2information extrahiert';
    Leave main_block;
  End if;  -- Eingabestring enthaelt nur Key2


  If ((v_locate_key1>0) And (v_locate_key2>0)) Then
    /* Eingabestring enthaelt Key1 und Key2 */
    Set v_mehrfach = LOCATE(p_Key1, p_strIn, v_locate_key1 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key1 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    Set v_mehrfach = LOCATE(p_Key2, p_strIn, v_locate_key2 + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Key2 kommt mehrfach vor';
      Set p_value1 = 'leer';
      Set p_value2 = 'leer';
      Set p_prefix = 'leer';
      Leave main_block;
    End if;

    If (v_locate_key1 < v_locate_key2) Then
      If (v_locate_key1 = 1) then
        Set p_prefix = 'leer';
      Else
        Set p_prefix = Trim(Substring(p_strIn, 1, v_locate_key1-1));
        If (Length(p_prefix)=0) Then
          Set p_prefix = 'leer';
        End if;
      End if;

      If ((v_locate_key1 + v_length_key1) = v_locate_key2) then
        Set p_value1 = 'leer';
      Else
        Set p_value1 = Trim(Substring(p_strIn, v_locate_key1+v_length_key1, v_locate_key2-v_locate_key1-v_length_key1));
        If (Length(p_value1)=0) Then
          Set p_value1 = 'leer';
        End if;
      End if;

      If (v_length_strIn < (v_locate_key2 + v_length_key2)) then
        Set p_value2 = 'leer';
      Else
        Set p_value2 = Trim(Substring(p_strIn, v_locate_key2+v_length_key2));
        If (Length(p_value2)=0) Then
          Set p_value2 = 'leer';
        End if;
      End if;
    Else  -- v_locate_key1 > v_locate_key2
      If (v_locate_key2 = 1) then
        Set p_prefix = 'leer';
      Else
        Set p_prefix = Trim(Substring(p_strIn, 1, v_locate_key2-1));
        If (Length(p_prefix)=0) Then
          Set p_prefix = 'leer';
        End if;
      End if;

      If ((v_locate_key2 + v_length_key2) = v_locate_key1) then
        Set p_value2 = 'leer';
      Else
        Set p_value2 = Trim(Substring(p_strIn, v_locate_key2+v_length_key2, v_locate_key1-v_locate_key2-v_length_key2));
        If (Length(p_value2)=0) Then
          Set p_value2 = 'leer';
        End if;
      End if;

      If (v_length_strIn < (v_locate_key1 + v_length_key1)) then
        Set p_value1 = 'leer';
      Else
        Set p_value1 = Trim(Substring(p_strIn, v_locate_key1+v_length_key1));
        If (Length(p_value1)=0) Then
          Set p_value1 = 'leer';
        End if;
      End if;
    End if; -- v_locate_key1 > v_locate_key2
    Set p_procRc = 0;
    Set p_reason = 'Key1Information und Key2information extrahiert';
    Leave main_block;

  End if;  -- Eingabestring enthaelt Key1 und Key2

-- Select CONCAT('Platte=',(CAST(v_count AS CHAR)),' neue Fehler=',(CAST(v_error AS CHAR)) );
-- Select CONCAT('Notes=', p_notes, ';Platte=', p_platte, ';Contamination=', p_contamination, ';Note=', p_note);
--  Select CONCAT('Notes=', p_notes, ';Platte=', p_platte, ';v_locate_platte=', CAST(v_locate_platte AS CHAR),
--    ';v_length_notes=', CAST(v_length_notes AS CHAR) );
  Set p_procRc = 0;
  Set p_reason = 'Internal Error';
  Set p_value1 = 'leer';
  Set p_value2 = 'leer';
  Set p_prefix = 'leer';
  Leave main_block;

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `FillTransferTable` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `FillTransferTable`;
DELIMITER ;;
CREATE PROCEDURE `FillTransferTable`()
Begin
/**************** Aenderungen ***********************************************************/
/* V2 Erzeuge Status=error Eintraege                                                    */
/****************************************************************************************/
  /* Declares fuer Tabelle Transfer_Extr_Plate_Name */
  Declare e_id            int(10);
  Declare e_transferDate  datetime;
  Declare e_status        varchar(999);
  Declare e_note          varchar(999);
  Declare e_sampleId      varchar(45);
  Declare e_collSpecId    int(10);
  Declare e_plateId       int(10);
  Declare e_plateLocation int(10);
  Declare e_plateSize     int(11);
  Declare e_plateName     varchar(64);

  /* Declares fuer Variable */
  Declare v_version int;  -- Version dieser Prozedur
  Declare v_anzahl int;  -- Gefundene Zeilen der Select Befehle
  Declare v_count int;   -- Zeilen Zaehler
  Declare v_error int;   -- Fehler Zaehler
  Declare v_done int;    -- Indikator Ende der Ergebnismenge
  Declare param_max_anzahl int;  -- maximale Durchlaeufe der Verarbeitungsloop
  Declare v_collSpecId     varchar(45); -- Hilfsvariable fuer Konvertierung in e_collSpecId
  Declare v_is_integer int; -- Indikator fuer ganze positive Zahl

  Declare c_extr Cursor For Select id
    From Transfer_Extr_Plate_Name
    Where status='new'
    Order By id;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set v_version = 2;
  Set v_anzahl = 0;
  Set v_count  = 0;
  Set v_error  = 0;
  Set v_done   = 0;
  Set param_max_anzahl = 1000;  -- maximale Durchlaeufe der Verarbeitungsloop

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into e_id ;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_count = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
    Set v_count = v_count+1;

    /* ############# Extrahiere Informationen aus Tabelle extraction ######################*/
    Select count(id), sampleId, plate, location into v_anzahl, e_sampleId, e_plateId, e_plateLocation From extraction Where id = e_id;
    If v_anzahl=0 Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_ExtractionEintragNichtGefunden fuer Id=',(CAST(e_id AS CHAR)) );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW()
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End If;

    /* e_sampleId */
    If (e_sampleId IS NULL) OR (Length(e_sampleId) = 0) Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_SampleId ist leer fuer Id=',(CAST(e_id AS CHAR)) );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW()
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End if;
    /* Extrahiere den numerischen Teil der sampleId zB ZFMK-TIS-12345 -> 12345 */
    If (Length(e_sampleId) > 9) And (Upper(Left(e_sampleId,9))='ZFMK-TIS-') then
	  Set v_CollSpecId=Right(e_sampleId,Length(e_sampleId)-9);
    ElseIf (Length(e_sampleId) > 9) And (Upper(Left(e_sampleId,9))='ZFMK-DNA-') then
	  Set v_CollSpecId=Right(e_sampleId,Length(e_sampleId)-9);
    ElseIf (Length(e_sampleId) > 5) And (Upper(Left(e_sampleId,5))='GBOL-') then
	  Set v_CollSpecId=Right(e_sampleId,Length(e_sampleId)-5);
    ElseIf (Length(e_sampleId) > 5) And (Upper(Left(e_sampleId,5))='GBOL ') then
	  Set v_CollSpecId=Right(e_sampleId,Length(e_sampleId)-5);
    Else
      Set v_CollSpecId = e_sampleId;
    End If;
    /* Numerischer Teil muss positive ganze Zahl sein */
    Set v_is_integer = (v_CollSpecId REGEXP '^[0-9]+$'); -- auch negative Zahlen '^-?[0-9]+$'
    If v_is_integer<>1 Then
      If v_CollSpecId = 'N' Then
        Set e_status = 'ignore';
        Set e_note = CONCAT('Ignore_fill_SampleId nicht in ganze Zahl umgewandelt, sampleId=', e_sampleId, ' ->', v_CollSpecId );
        Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW()
          Where id=e_id;
      Else
        Set e_status = 'error';
        Set e_note = CONCAT('Ignore_fill_SampleId nicht in ganze Zahl umgewandelt, sampleId=', e_sampleId, ' ->', v_CollSpecId );
        Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW()
          Where id=e_id;
      End If;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End If;
    Set e_CollSpecId = CAST(v_CollSpecId AS UNSIGNED INTEGER);

    /* e_plateLocation */
    If (e_plateLocation IS NULL) OR (e_plateLocation < 0) Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_PlateLocation ist ungueltig <0, location=', e_plateLocation );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
        collSpecId=e_collSpecId
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End If;

    /* e_plateId */
    If (e_plateId IS NULL) OR (e_plateId < 1) Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_PlateId ist ungueltig <1, plate=', e_plateId );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
        collSpecId=e_collSpecId, plateLocation=e_plateLocation
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End If;


    /* ############# Extrahiere Informationen aus Tabelle plate ###################*/
    Select count(id), name, size into v_anzahl, e_plateName, e_plateSize From plate Where id = e_plateId;
    If v_anzahl=0 Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_PlateEintragNichtGefunden fuer Id=',(CAST(e_plateId AS CHAR)) );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
        collSpecId=e_collSpecId, plateId=e_plateId, plateLocation=e_plateLocation
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End If;

    /* e_plateName */
    If (e_plateName IS NULL) OR (Length(e_plateName) = 0) Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_PlateName ist leer fuer PlateId=',(CAST(e_plateId AS CHAR)) );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
        collSpecId=e_collSpecId, plateId=e_plateId, plateLocation=e_plateLocation
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End if;
    If (Length(Trim(e_plateName)) = 0) Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_PlateName enthaelt nur Leerzeichen fuer PlateId=',(CAST(e_plateId AS CHAR)) );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
        collSpecId=e_collSpecId, plateId=e_plateId, plateLocation=e_plateLocation
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End if;

    /* e_plateSize */
    If (e_plateSize IS NULL) OR (e_plateSize < 1) Then
      Set e_status = 'error';
      Set e_note = CONCAT('Ignore_fill_PlateSize ist ungueltig <1 fuer PlateId=',(CAST(e_plateId AS CHAR)) );
      Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
        collSpecId=e_collSpecId, plateId=e_plateId, plateLocation=e_plateLocation, plateName=e_plateName
        Where id=e_id;
      Set v_error = v_error+1;
      Iterate l_fetch_data;
    End if;

    Set e_status = 'prepared';
    Set e_note = 'fill ok';
    Update Transfer_Extr_Plate_Name Set status=e_status, note=e_note, transferDate=NOW(), sampleId=e_sampleId,
      collSpecId=e_collSpecId, plateId=e_plateId, plateSize=e_plateSize, plateLocation=e_plateLocation, plateName=e_plateName
      Where id=e_id;


  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_count AS CHAR)),' neue Fehler=',(CAST(v_error AS CHAR)) );

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `InsertIntoTransferTable` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `InsertIntoTransferTable`;
DELIMITER ;;
CREATE PROCEDURE `InsertIntoTransferTable`()
Begin



  Declare v_id varchar(255);
  Declare v_status varchar(999);
  Declare v_note varchar(999);

  Declare v_count int;
  Declare v_error int;
  Declare v_count_max int;
  Declare v_done int;

  Declare c_sync Cursor For
    Select id From extraction
      Where (id Not In (SELECT id From Transfer_Extr_Plate_Name)) Order By id;


  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set v_count  = 0;
  Set v_error  = 0;
  Set v_count_max  = 1000;
  Set v_done   = 0;

  Set v_status = 'new';
  Set v_note   = 'insert new';

  Open c_sync;

  l_fetch_data: Loop
    Fetch c_sync Into v_id;
    If v_done Then
      Leave l_fetch_data;
    End If;

    Insert Into Transfer_Extr_Plate_Name (id, `status`, note) Values (v_id, v_status, v_note);

    Set v_count = v_count+1;

   If v_count = v_count_max Then
      Leave l_fetch_data;
    End If;
  End Loop l_fetch_data;
  Close c_sync;

  Select CONCAT('Zeileneingefuegt=',(CAST(v_count AS CHAR)),' Fehler=',(CAST(v_error AS CHAR)) );
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `loadAssemblyData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `loadAssemblyData`;
DELIMITER ;;
CREATE PROCEDURE `loadAssemblyData`(IN p_id int(10),
   OUT p_procRc int, OUT p_note varchar(999), OUT p_extractionId varchar(45), OUT p_workflowId varchar(45),
   OUT p_progress varchar(45), OUT p_date timestamp, OUT p_technician varchar(255),
   OUT p_assemNotes varchar(20000), OUT p_consensus varchar(20000), OUT p_assemPlateSuffix varchar(999), OUT p_assemContam varchar(999),
   OUT p_assem_failure_reason_id int, OUT p_assem_failure_reason varchar(80), OUT p_assem_failure_detail varchar(20000) )
main_block: Begin
/**************** Aenderungen *********************************************************/
/* V1 neues Feld assemNotes                                                           */
/* V2 neue Felder assemPlateSuffix, assemContam                                       */
/* V3 neue Felder assem_failure_reason_id, assem_failure_reason, assem_failure_detail */
/* V4 vereinfache das Fuellen des assemContam Feldes                                  */
/* V5 neues Feld workflowDate                                                         */
/* V6 initialisiere workflowDate in Prozedur loadExtractionData                       */
/* V7 04.11.2015 Aendere longtext Typ in varchar(20000)                               */
/**************************************************************************************/

  Declare v_count int; -- Anzahl Eintraege
  -- Declare v_id int;    -- AssemblyId
  -- Declare v_extractionId varchar(45);    -- AssemblyExtractionId
  Declare v_assemNotes varchar(20000);
  Declare v_reason varchar(99);

  Set v_assemNotes = NULL;
  Set v_reason = NULL;

  Set p_procRc = 8; -- Nimm Fehlerfall an
  Set p_note = 'Fehler';
  Set p_extractionId = NULL;
  Set p_workflowId = 0;
  Set p_progress = NULL;
  Set p_date = NULL;
  Set p_technician = NULL;
  Set p_assemNotes = NULL;
  Set p_consensus = NULL;
  Set p_assemPlateSuffix = NULL;
  Set p_assemContam = NULL;
  Set p_assem_failure_reason_id = 0;
  Set p_assem_failure_reason = Null;
  Set p_assem_failure_detail = Null;

  Select Count(id) into v_count From assembly Where id=p_id;
  /* Kein AssemblyEintrag gefunden */
  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_KeinEintragGefundenFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End If;

  Select extraction_id, workflow, progress, consensus, date, technician, notes, failure_reason, failure_notes
    Into p_extractionId, p_workflowId, p_progress, p_consensus, p_date, p_technician, p_assemNotes,
      p_assem_failure_reason_id, p_assem_failure_detail
    From assembly Where id=p_id;

  /* ExtractionId darf nicht leer sein */
  If (p_extractionId IS NULL) OR (Length(p_extractionId) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_ExtractionIdIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* WorkflowId darf nicht leer sein */
  If (p_workflowId IS NULL) OR (p_workflowId < 1) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_WorkflowIstUngueltigFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Progress darf nicht leer sein */
  If (p_progress IS NULL) OR (Length(p_progress) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_ProgressIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Consensus darf nicht leer sein */
  If (p_consensus IS NULL) OR (Length(p_consensus) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_ConsensusIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Technician darf nicht leer sein */
  If (p_technician IS NULL) OR (Length(p_technician) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_TechnicianIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Date darf nicht leer sein */
  If (p_date IS NULL) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_DateIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Initialisiere die Parameter p_assemNotes, p_assemPlateSuffix und p_assemContam */
  If ((p_assemNotes IS NULL) OR (Length(p_assemNotes) = 0)) Then
    Set p_assemContam = 'leer';
    Set p_assemPlateSuffix = 'leer';
    Set p_assemNotes = 'leer';
  Else
    Call ExtractInfo(p_assemNotes, 'P:', 'C:', p_procRc, v_reason, p_assemPlateSuffix, p_assemContam, v_assemNotes);
    If (p_procRc > 0) Then
      Set p_procRc = 8;
      Set p_note = CONCAT('Fehler_Assem_ExtractInfoReason=', v_reason, ';Notes=', p_assemNotes);
      Leave main_block;
    End if;
    Set p_assemNotes = v_assemNotes;
  End if;

  /* Initialisiere den Parameter p_assem_failure_reason_id und p_assem_failure_reason */
  If ((p_assem_failure_reason_id IS NULL) OR (p_assem_failure_reason_id < 1)) Then
    Set p_assem_failure_reason_id = 0;
    Set p_assem_failure_reason = 'leer';
  Else
    Select Count(id) into v_count From failure_reason Where id=p_assem_failure_reason_id;
    /* Kein Failure_reasonEintrag gefunden */
    If v_count=0 Then
      Set p_procRc = 8;
      Set p_note = CONCAT('Fehler_Assem_KeinFailure_reasonEintragGefundenFuerId=', (CAST(p_assem_failure_reason_id AS CHAR)) );
      Leave main_block;
    End If;
    Select name into p_assem_failure_reason From failure_reason Where id=p_assem_failure_reason_id;
  End if;

  /* Initialisiere den Parameter p_assem_failure_detail */
  If ((p_assem_failure_detail IS NULL) OR (Length(p_assem_failure_detail)=0) ) Then
    Set p_assem_failure_detail = 'leer';
  End if;

  Set p_procRc = 0;
  Set p_note = 'Assembly alles ok';

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `loadAssemblyDataTest` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `loadAssemblyDataTest`;
DELIMITER ;;
CREATE PROCEDURE `loadAssemblyDataTest`(IN p_id int(10),
   OUT p_procRc int, OUT p_note varchar(999), OUT p_extractionId varchar(45), OUT p_workflowId varchar(45),
   OUT p_progress varchar(45), OUT p_date timestamp, OUT p_technician varchar(255),
   OUT p_assemNotes varchar(65535), OUT p_consensus varchar(65535), OUT p_assemPlateSuffix varchar(999), OUT p_assemContam varchar(999),
   OUT p_assem_failure_reason_id int, OUT p_assem_failure_reason varchar(80), OUT p_assem_failure_detail varchar(65535) )
main_block: Begin
/**************** Aenderungen *********************************************************/
/* V1 neues Feld assemNotes                                                           */
/* V2 neue Felder assemPlateSuffix, assemContam                                       */
/* V3 neue Felder assem_failure_reason_id, assem_failure_reason, assem_failure_detail */
/* V4 vereinfache das Fuellen des assemContam Feldes                                  */
/* V5 neues Feld workflowDate                                                         */
/* V6 initialisiere workflowDate in Prozedur loadExtractionData                       */
/**************************************************************************************/

  Declare v_count int; -- Anzahl Eintraege
  -- Declare v_id int;    -- AssemblyId
  -- Declare v_extractionId varchar(45);    -- AssemblyExtractionId
  Declare v_assemNotes longtext;
  Declare v_reason varchar(99);
  Declare v_trace1 varchar(99);
  Declare v_trace2 varchar(99);
  Declare v_trace3 varchar(199);
  Declare v_trace4 varchar(99);
  Declare v_callin  varchar(999);
  Declare v_callout varchar(999);

  Set v_assemNotes = 'ni';
  Set v_reason = 'ni';
  Set v_trace1  = 'ni';
  Set v_trace2  = 'ni';
  Set v_trace3  = 'ni';
  Set v_trace4  = 'ni';
  Set v_callin  = 'ni';
  Set v_callout = 'ni';

/*
IN p_strIn varchar(999),v_callin
IN p_key1 varchar(99), 'P:'
IN p_key2 varchar(99),'C:'
OUT p_procRc int, p_procRc
OUT p_reason varchar(99), v_reason
OUT p_value1 varchar(999), p_assemPlateSuffix
OUT p_value2 varchar(999), p_assemContam
OUT p_prefix varchar(999) v_callout*/

  Set p_procRc = 8; -- Nimm Fehlerfall an
  Set p_note = 'Fehler';
  Set p_extractionId = NULL;
  Set p_workflowId = 0;
  Set p_progress = NULL;
  Set p_date = NULL;
  Set p_technician = NULL;
  Set p_assemNotes = NULL;
  Set p_consensus = NULL;
  Set p_assemPlateSuffix = NULL;
  Set p_assemContam = NULL;
  Set p_assem_failure_reason_id = 0;
  Set p_assem_failure_reason = Null;
  Set p_assem_failure_detail = Null;

  Select Count(id) into v_count From assembly Where id=p_id;
  /* Kein AssemblyEintrag gefunden */
  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_KeinEintragGefundenFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End If;

  Select extraction_id, workflow, progress, consensus, `date`, technician, notes, failure_reason, failure_notes
    Into p_extractionId, p_workflowId, p_progress, p_consensus, p_date, p_technician, p_assemNotes,
      p_assem_failure_reason_id, p_assem_failure_detail
    From assembly Where id=p_id;
  Set v_trace1 = CONCAT('T1=', Substring(p_assemNotes,1,40), ' Consensus=', Substring(p_consensus,1,40));

  /* ExtractionId darf nicht leer sein */
  If (p_extractionId IS NULL) OR (Length(p_extractionId) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_ExtractionIdIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;
  /* WorkflowId darf nicht leer sein */
  If (p_workflowId IS NULL) OR (p_workflowId < 1) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_WorkflowIstUngueltigFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Progress darf nicht leer sein */
  If (p_progress IS NULL) OR (Length(p_progress) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_ProgressIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Consensus darf nicht leer sein */
  If (p_consensus IS NULL) OR (Length(p_consensus) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_ConsensusIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Technician darf nicht leer sein */
  If (p_technician IS NULL) OR (Length(p_technician) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_TechnicianIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;

  /* Date darf nicht leer sein */
  If (p_date IS NULL) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Assem_DateIstLeerFuerId=', (CAST(p_id AS CHAR)) );
    Leave main_block;
  End if;
    Set v_trace2 = CONCAT('\nT2=', Substring(p_assemNotes,1,40), ' Consensus=', Substring(p_consensus,1,40));

  /* Initialisiere die Parameter p_assemNotes, p_assemPlateSuffix und p_assemContam */
--    Call ExtractInfo(p_assemNotes, 'P:', 'C:', p_procRc, v_reason, p_assemPlateSuffix, p_assemContam, v_assemNotes);
--    Call ExtractInfoTest(p_assemNotes, 'P:', 'C:', p_procRc, v_reason, p_assemPlateSuffix, p_assemContam, v_assemNotes);

    -- Set v_callin=p_assemNotes;
    Set v_callin='P:_0328_0334_0338_NW';
    Call ExtractInfoTest(v_callin, 'P:', 'C:', p_procRc, v_reason, p_assemPlateSuffix, p_assemContam, v_callout);



    -- If (p_procRc > 0) Then
    --  Set p_procRc = 8;
    --  Set p_note = CONCAT('Fehler_Assem_ExtractInfoReason=', v_reason, ';Notes=', p_assemNotes);
    --  Leave main_block;
    -- End if;
    Set v_trace3 = CONCAT('\nT3=', Substring(p_assemNotes,1,40), ' v_assemNotes=', Substring(v_assemNotes,1,40),
      ' v_reason=', v_reason, ' Consensus=', Substring(p_consensus,1,40), ' p_assemPlateSuffix=', Substring(p_assemPlateSuffix,1,40));
    Set v_trace4 = CONCAT('\nT4=callin', Substring(v_callin,1,40), ' callout=', Substring(v_callout,1,40));
    Set p_note = CONCAT(v_trace1, v_trace2, v_trace3, v_trace4);




  -- Set p_procRc = 0;
  -- Set p_note = 'Assembly alles ok';

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `loadCycleSequencingData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `loadCycleSequencingData`;
DELIMITER ;;
CREATE PROCEDURE `loadCycleSequencingData`(IN p_workflowId int(10), IN p_extractionId varchar(45),
   IN p_direction varchar(32), IN p_assemPlateSuffix varchar(999), IN p_assemNotes varchar(20000),
   OUT p_procRc int, OUT p_note varchar(999), OUT p_cycleSeqAnzahl int, OUT p_cycleSeqId int(11), OUT p_primerName varchar(64),
   OUT p_primerSequence varchar(999), OUT p_traceAnzahl int, OUT p_traceId int(10), OUT p_traceName varchar(96),
   OUT p_technician varchar(90), OUT p_date timestamp, OUT p_traceFormat varchar(45) )
main_block: Begin
/**************** Aenderungen *******************************/
/* V1 neue Selection-Logik mit assemPlateSuffix             */
/* V2 neue Selection-Logik auch fuer Trace-Suche            */
/* V3 neue Selection-Logik fuer assemNotes(1:8)='PlateSeq'  */
/* V4 24.04.2014 Setze v_pname=leer                         */
/* V5 04.11.2015 Aendere longtext Typ in varchar(20000)     */
/************************************************************/
  Declare v_count int; -- Anzahl Eintraege
  Declare v_id int;    -- CyclesequencingId
  Declare v_extractionId varchar(45);    -- CyclesequencingExtractionId
  Declare v_traceFormat varchar(96);     -- Fuer die Ermittlung des TraceFormats
  Declare v_pname varchar(999);

-- p_direction = forward oder reverse
  Set p_procRc = 8; -- Nimm Fehlerfall an
  Set p_note = 'Fehler';
  Set p_cycleSeqAnzahl = 0;
  Set p_cycleSeqId = 0;
  Set p_primerName = NULL;
  Set p_primerSequence = NULL;
  Set p_traceAnzahl = 0;
  Set p_traceId = NULL;
  Set p_traceName = NULL;
  Set p_technician = NULL;
  Set p_date = NULL;
  Set p_traceFormat = NULL;

--  Select Count(id) into v_count From cyclesequencing Where workflow=p_workflowId and direction=p_direction;
  If (Length(p_assemNotes) > 8) AND (Left(p_assemNotes,8)='PlateSeq') then
	Set v_pname=RIGHT(p_assemNotes,LENGTH(p_assemNotes)-8);
    Set v_pname = CONCAT("%", v_pname);
    Select Max(c.id), Count(c.id) into v_id, v_count From cyclesequencing as c, plate as p
      Where c.workflow=p_workflowId and c.direction=p_direction and c.plate=p.id and p.name like v_pname;
  Elseif (p_assemPlateSuffix = 'leer') Then
    Set v_pname = 'leer';
    Select Max(id), Count(id) into v_id, v_count From cyclesequencing Where workflow=p_workflowId and direction=p_direction;
  else
    Set v_pname = CONCAT("%", p_assemPlateSuffix);
    Select Max(c.id), Count(c.id) into v_id, v_count From cyclesequencing as c, plate as p
      Where c.workflow=p_workflowId and c.direction=p_direction and c.plate=p.id and p.name like v_pname;
  end if;
  /* Kein Cyclesequencingeintrag gefunden */
  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_KeinCycleSequencingEintragGefundenFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
                        ' Direction=', p_direction, ' v_pname=', v_pname, ';' );
    Leave main_block;
  End If;
  /* Mindestens ein Cyclesequencing Eintrag gefunden */
  Set p_cycleSeqAnzahl = v_count;
  Select id, primerName, primerSequence, extractionId, date, technician
    Into p_cycleSeqId, p_primerName, p_primerSequence, v_extractionId, p_date, p_technician
    From cyclesequencing Where id = v_id;
  --  From cyclesequencing Where direction=p_direction Group By workflow Having workflow=p_workflowId order by id asc;
  /* PrimerName darf nicht leer sein */
  If (p_primerName IS NULL) OR (Length(p_primerName) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_PrimerNameIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
                        ' Direction=', p_direction, ' CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)) );
    Leave main_block;
  End if;
  /* PrimerSequence darf nicht leer sein */
  If (p_primerSequence IS NULL) OR (Length(p_primerSequence) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_PrimerSequenceIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
                        ' Direction=', p_direction, ' CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)) );
    Leave main_block;
  End if;
  /* ExtractionId darf nicht leer sein */
  If (v_extractionId IS NULL) OR (Length(v_extractionId) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_ExtractionIdIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
                        ' Direction=', p_direction, ' CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)) );
    Leave main_block;
  End if;
  /* ExtractionId muss mit Vorgabe uebereinstimmen */
  If (v_extractionId <> p_extractionId) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_ExtractionId=', v_extractionId,
                        ' ist ungleich erwartetem Wert=', p_extractionId,
                        ' Direction=', p_direction, ' CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)) );
    Leave main_block;
  End if;
  /* Date darf nicht leer sein */
  If (p_date IS NULL) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_DateIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
                        ' Direction=', p_direction, ' CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)) );
    Leave main_block;
  End if;
  /* Technician darf nicht leer sein */
  If (p_technician IS NULL) OR (Length(p_technician) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_TechnicianIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
                        ' Direction=', p_direction, ' CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)) );
    Leave main_block;
  End if;

  /* Suche zugehoerigen Trace Record */
  -- Select Count(id) into v_count From traces Where reaction=p_cycleSeqId;
  Select Max(id), Count(id) into v_id, v_count From traces Where reaction=p_cycleSeqId;
 /* Kein Trace Eintrag gefunden */
  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_KeinTraceEintragGefundenFuerReaction=', (CAST(p_cycleSeqId AS CHAR)),
                        ' Direction=', p_direction );
    Leave main_block;
  End If;
  /* Mindestens ein Trace Eintrag gefunden */
  Set p_traceAnzahl = v_count;

  Select id, name
    Into p_traceId, p_traceName
    From traces Where id=v_id;
--    From traces Group by reaction Having reaction=p_cycleSeqId order by id asc;
  /* TraceName darf nicht leer sein */
  If (p_traceName IS NULL) OR (Length(p_traceName) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_TraceNameIstLeerFuerReaction=', (CAST(p_cycleSeqId AS CHAR)),
                        ' Direction=', p_direction );
    Leave main_block;
  End If;
  /* TraceName muss mindestens 5 Zeichen lang sein */
  If (Length(p_traceName) < 5) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_TraceNameIstZuKurz CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)),
                        ' Direction=', p_direction, ' TraceId=', (CAST(p_traceId AS CHAR)), ' TraceName=', p_traceName );
    Leave main_block;
  End If;
  /* Die Endung des TraceNamens bestimmt das Traceformat */
  Set v_traceFormat = Right(Upper(Trim(p_traceName)), 4);
  If (v_traceFormat='.AB1') Then
    Set p_traceFormat = 'ABI';
  ElseIf (v_traceFormat='.ABI') Then
    Set p_traceFormat = 'ABI';
  ElseIf (v_traceFormat='.SCF') Then
    Set p_traceFormat = 'SCF';
  Else
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_CycleSeq_TraceFormatNichtErkannt CycleSeqId=', (CAST(p_cycleSeqId AS CHAR)),
                        ' Direction=', p_direction, ' TraceId=', (CAST(p_traceId AS CHAR)), ' TraceName=', p_traceName );
    Leave main_block;
  End if;

  Set p_procRc = 0;
  Set p_note = CONCAT('Cyclesequencing alles ok fuer Direction=', p_direction);

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `loadExtractionData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `loadExtractionData`;
DELIMITER ;;
CREATE PROCEDURE `loadExtractionData`(IN p_workflowId int(10), IN p_extractionId varchar(45),
   OUT p_procRc int, OUT p_note varchar(999), OUT p_locus varchar(45), OUT p_extractionTblId int(10),
   OUT p_workflowDate date, OUT p_extractionDate timestamp, OUT p_sampleId varchar(45), OUT p_dwb_CollectionSpecimenId int(10) )
main_block: Begin





  Declare v_count int;
  Declare v_extractionId varchar(45);
  Declare v_is_integer int;
  Declare v_dwb_CollectionSpecimenId varchar(45);

  Set p_procRc = 8;
  Set p_note = 'Fehler';
  Set p_locus = NULL;
  Set p_extractionTblId = 0;
  Set p_workflowDate = NULL;
  Set p_extractionDate = NULL;
  Set p_sampleId = NULL;
  Set p_dwb_CollectionSpecimenId = 0;

  Select Count(id) into v_count From workflow Where id = p_workflowId;

  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_KeinWorkflowEintrag fuer WorkflowId=',(CAST(p_workflowId AS CHAR)) );
    Leave main_block;
  End If;
  Select extractionId, locus, date into p_extractionTblId, p_locus, p_workflowDate From workflow Where id = p_workflowId;

  If (p_locus <> 'COI') Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_LocusIstNichtCOI fuer WorkflowId=',(CAST(p_workflowId AS CHAR)) );
    Leave main_block;
  End if;

  If (p_extractionTblId < 1) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_ExtractionIdIstUngueltig fuer WorkflowId=',(CAST(p_workflowId AS CHAR)) );
    Leave main_block;
  End if;

  If (p_workflowDate IS NULL) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_WorkflowDateIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)) );
    Leave main_block;
  End if;

  Select Count(id) into v_count From extraction Where id = p_extractionTblId;

  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_KeinExtractionEintrag fuer WorkflowId=',(CAST(p_workflowId AS CHAR)),
      ' ExtractionTblId=',(CAST(p_extractionTblId AS CHAR)) );
    Leave main_block;
  End If;
  Select sampleId, extractionId, date into p_sampleId, v_extractionId, p_extractionDate From extraction Where id = p_extractionTblId;

  If (p_sampleId IS NULL) OR (Length(p_sampleId) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_SampleIdIstLeer fuer WorkflowId=',(CAST(p_workflowId AS CHAR)),
      ' ExtractionTblId=',(CAST(p_extractionTblId AS CHAR)) );
    Leave main_block;
  End if;

  If (v_extractionId IS NULL) OR (Length(v_extractionId) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_ExtractionIdIstLeer fuer WorkflowId=',(CAST(p_workflowId AS CHAR)),
      ' ExtractionTblId=',(CAST(p_extractionTblId AS CHAR)) );
    Leave main_block;
  End if;

  If (v_extractionId <> p_extractionId) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_ExtractionId=', v_extractionId,
      ' IstUngleichVorgabe=',p_extractionId );
    Leave main_block;
  End if;

  If (p_extractionDate IS NULL) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_ExtractionDateIstLeer fuer WorkflowId=',(CAST(p_workflowId AS CHAR)),
      ' ExtractionTblId=',(CAST(p_extractionTblId AS CHAR)) );
    Leave main_block;
  End if;


  If (Length(p_sampleId) > 9) AND (left(p_sampleId,9)='ZFMK-TIS-') then
	Set v_dwb_CollectionSpecimenId=RIGHT(p_sampleId,LENGTH(p_sampleId)-9);
  ElseIf (Length(p_sampleId) > 9) AND (left(p_sampleId,9)='ZFMK-DNA-') then
	Set v_dwb_CollectionSpecimenId=RIGHT(p_sampleId,LENGTH(p_sampleId)-9);
  ElseIf (Length(p_sampleId) > 5) AND (left(p_sampleId,5)='GBOL-') then
	Set v_dwb_CollectionSpecimenId=RIGHT(p_sampleId,LENGTH(p_sampleId)-5);
  ElseIf (Length(p_sampleId) > 5) AND (left(p_sampleId,5)='GBOL ') then
	Set v_dwb_CollectionSpecimenId=RIGHT(p_sampleId,LENGTH(p_sampleId)-5);
  ELSE
    Set v_dwb_CollectionSpecimenId = p_sampleId;
  End If;


  Set v_is_integer = (v_dwb_CollectionSpecimenId REGEXP '^[0-9]+$');
  If v_is_integer<>1 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Extraction_SampleIdMussGanzeZahlSein, sampleId=', p_sampleId, ' ->', v_dwb_CollectionSpecimenId);
    Leave main_block;
  End If;
  Set p_dwb_CollectionSpecimenId = CAST(v_dwb_CollectionSpecimenId AS UNSIGNED INTEGER);

  Set p_procRc = 0;
  Set p_note = 'Extraction alles ok';

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `loadPcrData` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `loadPcrData`;
DELIMITER ;;
CREATE PROCEDURE `loadPcrData`(IN p_workflowId int(10), IN p_extractionId varchar(45), IN p_assemPlateSuffix varchar(999),
   OUT p_procRc int, OUT p_note varchar(999), OUT p_Anzahl int, OUT p_Id int(11), OUT p_pcrDate timestamp,
   OUT p_prName varchar(64), OUT p_prSequence varchar(999), OUT p_revPrName varchar(64), OUT p_revPrSequence varchar(999) )
main_block: Begin





  Declare v_count int;
  Declare v_id int;
  Declare v_extractionId varchar(45);
  Declare v_pname varchar(999);

  Set p_procRc = 8;
  Set p_note = 'Fehler';
  Set p_Anzahl = 0;
  Set p_Id = 0;
  Set p_pcrDate = NULL;
  Set p_prName = NULL;
  Set p_prSequence = NULL;
  Set p_revPrName = NULL;
  Set p_revPrSequence = NULL;


  Set v_pname = CONCAT("%", p_assemPlateSuffix);
  If p_assemPlateSuffix = 'leer' Then
    Select Max(id), Count(id) into v_id, v_count From pcr Where workflow=p_workflowId;
  Else
    Select Max(pcr.id), Count(pcr.id) into v_id, v_count From pcr, plate as p
      Where pcr.workflow=p_workflowId and pcr.plate=p.id and p.name like v_pname;
  End if;


  If v_count=0 Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_KeinPcrEintragGefundenFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' v_pname=', v_pname, ';'  );
    Leave main_block;
  End If;

  Set p_Anzahl = v_count;
  Select id, extractionId, prName, prSequence, revPrName, revPrSequence, date
    Into p_Id, v_extractionId, p_prName, p_prSequence, p_revPrName, p_revPrSequence, p_pcrDate
    From pcr Where id = v_id;



  If (v_extractionId IS NULL) OR (Length(v_extractionId) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_ExtractionIdIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' PcrId=', (CAST(p_Id AS CHAR)) );
   Leave main_block;
  End if;

  If (v_extractionId <> p_extractionId) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_ExtractionId=', v_extractionId, ' ist ungleich erwartetem Wert=', p_extractionId,
      ' fuer PcrId=', (CAST(p_Id AS CHAR)) );
    Leave main_block;
  End if;


  If (p_prName IS NULL) OR (Length(p_prName) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_PrNameIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' fuer PcrId=', (CAST(p_Id AS CHAR)) );
    Leave main_block;
  End if;


  If (p_prSequence IS NULL) OR (Length(p_prSequence) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_PrSequenceIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' fuer PcrId=', (CAST(p_Id AS CHAR)) );
    Leave main_block;
  End if;


  If (p_revPrName IS NULL) OR (Length(p_revPrName) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_RevPrNameIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' fuer PcrId=', (CAST(p_Id AS CHAR)) );
    Leave main_block;
  End if;


  If (p_revPrSequence IS NULL) OR (Length(p_revPrSequence) = 0) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_RevPrSequenceIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' fuer PcrId=', (CAST(p_Id AS CHAR)) );
    Leave main_block;
  End if;


  If (p_pcrDate IS NULL) Then
    Set p_procRc = 8;
    Set p_note = CONCAT('Fehler_Pcr_pcrDateIstLeerFuerWorkflowId=', (CAST(p_workflowId AS CHAR)),
      ' fuer PcrId=', (CAST(p_Id AS CHAR)) );
    Leave main_block;
  End if;

  Set p_procRc = 0;
  Set p_note = 'PCR alles ok';

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `mapSuffix` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `mapSuffix`;
DELIMITER ;;
CREATE PROCEDURE `mapSuffix`(IN p_suffixIn longtext, OUT p_suffixOut varchar(999), OUT p_suffixMapped int )
Begin
/**************** Aenderungen *********************************************************/
/* 14.12.2015 Mapping 'P: _0572', 'P:_0573'                                           */
/* 27.01.2016 Mapping 'P: _0572', 'P:_0573' entfernt                                  */
/**************************************************************************************/
  Set p_suffixOut = 'Not Mapped';
  Set p_suffixMapped = 0;

  If p_suffixIn='P:_53_54_55' Then
    Set p_suffixOut = '_0053_0054_0055';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_7_9_10_13_16_20' Then
    Set p_suffixOut = '_0007_0009_0010_0013_0016_0020';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_55_56_57' Then
    Set p_suffixOut = '_0055_0056_0057';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_13_16' Then
    Set p_suffixOut = '_0013_0016';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='PlateSeq_0058_BGI' Then
    Set p_suffixOut = '_0058';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='PlateSeq_0058_M' Then
    Set p_suffixOut = '_0058';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_45_46_49_50' Then
    Set p_suffixOut = '_0045_0046_0049_0050';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_43_45' Then
    Set p_suffixOut = '_0043_0045';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_50_52_53' Then
    Set p_suffixOut = '_0050_0052_0053';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_35_41' Then
    Set p_suffixOut = '_0035_0041';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_44_47' Then
    Set p_suffixOut = '_0044_0047';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_41_44' Then
    Set p_suffixOut = '_0041_0044';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_47_51' Then
    Set p_suffixOut = '_0047_0051';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='PlateSeq_51_47' Then
    Set p_suffixOut = '_0047_0051';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_0105_N' Then
    Set p_suffixOut = '_0105';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_0104_N' Then
    Set p_suffixOut = '_0104';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_0039_0040_0074_0041' Then
    Set p_suffixOut = '_0039_0040_0074_0141';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_JJ_0147_0163_0180_NW' Then
    Set p_suffixOut = '_0147_0163_0180';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_0187_JJ' Then
    Set p_suffixOut = '_0187';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_43_45' Then
    Set p_suffixOut = '_0043_0045';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_51_47' Then
    Set p_suffixOut = '_0047_0051';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='PlateSeq_51_47' Then
    Set p_suffixOut = '_0047_0051';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate_Name:_41_44' Then
    Set p_suffixOut = '_0041_0044';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_0058_M' Then
    Set p_suffixOut = '_0058';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate:_0088_0089_0201' Then
    Set p_suffixOut = '_0088_0089_0201';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate:_0256' Then
    Set p_suffixOut = '_0256';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate:_0264' Then
    Set p_suffixOut = '_0264';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0029_0037_0120' Then
    Set p_suffixOut = '_0029_0037_0120';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0378' Then
    Set p_suffixOut = '_0378';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0414' Then
    Set p_suffixOut = '_0414';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0398' Then
    Set p_suffixOut = '_0398';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0397' Then
    Set p_suffixOut = '_0397';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0414' Then
    Set p_suffixOut = '_0414';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0411' Then
    Set p_suffixOut = '_0411';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0420' Then
    Set p_suffixOut = '_0420';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0418' Then
    Set p_suffixOut = '_0418';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0417' Then
    Set p_suffixOut = '_0417';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate: _0425' Then
    Set p_suffixOut = '_0425';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='Plate:_41_44' Then
    Set p_suffixOut = '_0041_0044';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P: _0464' Then
    Set p_suffixOut = '_0464_neu';
    Set p_suffixMapped = 1;
  ElseIf p_suffixIn='P:_0484' Then
    Set p_suffixOut = '_0484_neu';
    Set p_suffixMapped = 1;
  End if;

/*****************************************************/
/* 27.01.2016 Mapping 'P: _0572', 'P:_0573' entfernt */
/*  ElseIf p_suffixIn='P: _0572' Then                */
/*    Set p_suffixOut = '_0571-0572';                */
/*    Set p_suffixMapped = 1;                        */
/*  ElseIf p_suffixIn='P:_0573' Then                 */
/*    Set p_suffixOut = '_0573-0574';                */
/*    Set p_suffixMapped = 1;                        */
/*****************************************************/

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `prepUpdateDWB` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `prepUpdateDWB`;
DELIMITER ;;
CREATE PROCEDURE `prepUpdateDWB`()
main_block: Begin
/**************** Aenderungen ***********************************************************/
/* V1 neues Feld assemNotes                                                             */
/* V2 neue Felder assemPlateSuffix, assemContam                                         */
/* V3 neue Felder assem_failure_reason_id, assem_failure_reason, assem_failure_detail   */
/* V4 neue Felder workflowDate, extractionDate, pcrDate                                 */
/* V5 ignoriere Faelle assemProgress=failed and assem_failure_reason<>Parasite CON      */
/* V6 date Feld umbenannt in exportDate, workflowDate Type date anstelle von timestamp  */
/* V7 Eingangsstatus nur new                                                            */
/* V7 Alle failed-Eintraege auf Status ignore_failed setzen                             */
/* V7 Max Durchlaeufe=10000                                                             */
/* V7 Erfolgsstatus ist prepCheck                                                       */
/* V8 Neue Selection-Logik fuer assemNotes(1:8)='PlateSeq' fuer Cyclesequencing Platten */
/* V9 04.11.2015 Aendere longtext Typ in varchar(20000)                                 */
/****************************************************************************************/
  Declare param_max_anzahl int(10);  -- maximale Durchlaeufe der Verarbeitungsloop
  /* Declares fuer Tabelle assembly_export_COI */
  Declare e_id int(10);
  Declare e_exportDate timestamp;
  Declare e_workflowId int(10);
  Declare e_workflowDate date;
  Declare e_extractionTblId int(10);
  Declare e_extractionId varchar(45);
  Declare e_extractionDate timestamp;
  Declare e_dwb_CollectionSpecimenId int(10);
  Declare e_sampleId varchar(45);
  Declare e_status varchar(999);
  Declare e_note varchar(999);
  Declare e_assemDate timestamp;
  Declare e_assemProgress varchar(45);
  Declare e_assemTechnician varchar(255);
  Declare e_assemNotes varchar(20000);
  Declare e_assemConsensus varchar(20000);
  Declare e_assemPlateSuffix varchar(999);
  Declare e_assemContam varchar(999);
  Declare e_assem_failure_reason_id int;
  Declare e_assem_failure_reason varchar(80);
  Declare e_assem_failure_detail varchar(20000);
  Declare e_locus varchar(45);
  Declare e_pcrAnzahl int;
  Declare e_pcrId int(11);
  Declare e_pcrDate timestamp;
  Declare e_pcrPrName varchar(64);
  Declare e_pcrPrSequence varchar(999);
  Declare e_pcrRevPrName varchar(64);
  Declare e_pcrRevPrSequence varchar(999);
  Declare e_cycleSeqForwAnzahl int;
  Declare e_cycleSeqForwId int(11);
  Declare e_cycleSeqForwPrimerName varchar(64);
  Declare e_cycleSeqForwPrimerSequence varchar(999);
  Declare e_cycleSeqForwTraceAnzahl int;
  Declare e_cycleSeqForwTraceId int(10);
  Declare e_cycleSeqForwTraceName varchar(999);
  Declare e_cycleSeqForwTechnician varchar(90);
  Declare e_cycleSeqForwDate timestamp;
  Declare e_cycleSeqForwTraceFormat varchar(45);
  Declare e_cycleSeqRevAnzahl int;
  Declare e_cycleSeqRevId int(11);
  Declare e_cycleSeqRevPrimerName varchar(64);
  Declare e_cycleSeqRevPrimerSequence varchar(999);
  Declare e_cycleSeqRevTraceAnzahl int;
  Declare e_cycleSeqRevTraceId int(10);
  Declare e_cycleSeqRevTraceName varchar(999);
  Declare e_cycleSeqRevTechnician varchar(90);
  Declare e_cycleSeqRevDate timestamp;
  Declare e_cycleSeqRevTraceFormat varchar(45);

  Declare v_count int;  -- Zeilen Zaehler
  Declare v_error int;  -- Fehler Zaehler
  Declare v_done int;   -- Ende der Ergebnismenge
  Declare v_procRc int; -- Prozedur Return Code
  Declare v_count_test1 int;  -- Zaehler fuer Testzwecke
  Declare v_count_test2 int;  -- Zaehler fuer Testzwecke

  Declare c_extr Cursor For Select id, workflowId, extractionId, status, assemPlateSuffix, assemProgress, assem_failure_reason
    From assembly_export_COI
    Where status='new'
    Order By id;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set v_count  = 0;
  Set v_error  = 0;
  Set v_done   = 0;
  Set v_procRc = 8;
  Set v_count_test1 = 0;
  Set v_count_test2 = 0;
  Set param_max_anzahl = 10000;  -- maximale Durchlaeufe der Verarbeitungsloop

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into e_id, e_workflowId, e_extractionId, e_status, e_assemPlateSuffix, e_assemProgress, e_assem_failure_reason;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_count = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
    Set v_count = v_count+1;

    /* Lade Felder aus Tabelle assembly, falls noch nicht geschehen */
    if e_status='new' Then
		Call loadAssemblyData(e_id, v_procRc, e_note, e_extractionId, e_workflowId,
          e_assemProgress, e_assemDate, e_assemTechnician, e_assemNotes, e_assemConsensus,
          e_assemPlateSuffix, e_assemContam, e_assem_failure_reason_id, e_assem_failure_reason, e_assem_failure_detail );
		If (v_procRc = 4) Then
			Iterate l_fetch_data;
		ElseIf (v_procRc = 8) Then
			Set v_error = v_error+1;
			Update assembly_export_COI Set status='error', note=e_note Where id=e_id;
			Iterate l_fetch_data;
		End If;
        Set e_status='prep_assembly';
		Update assembly_export_COI Set status=e_status, note=e_note, extractionId=e_extractionId, workflowId=e_workflowId,
          assemProgress=e_assemProgress, assemDate=e_assemDate, assemTechnician=e_assemTechnician,
          assemNotes=e_assemNotes, assemConsensus=e_assemConsensus, assemPlateSuffix=e_assemPlateSuffix, assemContam=e_assemContam,
          assem_failure_reason_id=e_assem_failure_reason_id, assem_failure_reason=e_assem_failure_reason,
          assem_failure_detail=e_assem_failure_detail
          Where id=e_id;
	End If;

    /* Lade Felder aus Tabelle workflow und extraction, falls noch nicht geschehen */
    if e_status='prep_assembly' Then
		Call loadExtractionData(e_workflowId, e_extractionId, v_procRc, e_note, e_locus, e_extractionTblId,
          e_workflowDate, e_extractionDate, e_sampleId, e_dwb_CollectionSpecimenId );
		If (v_procRc = 4) Then
			Iterate l_fetch_data;
		ElseIf (v_procRc = 8) Then
			Set v_error = v_error+1;
			Update assembly_export_COI Set status='error', note=e_note Where id=e_id;
			Iterate l_fetch_data;
		End If;
		Set e_status='prep_extraction';
		Update assembly_export_COI Set status=e_status, note=e_note, locus=e_locus, extractionTblId=e_extractionTblId,
          workflowDate=e_workflowDate, extractionDate=e_extractionDate,
          sampleId=e_sampleId, dwb_CollectionSpecimenId=e_dwb_CollectionSpecimenId
          Where id=e_id;
	End If;

    /* Lade Felder aus Tabelle cyclesequencing, direction=forward */
    if e_status='prep_extraction' Then
		Call loadCycleSequencingData(e_workflowId, e_extractionId, 'forward', e_assemPlateSuffix, e_assemNotes,
          v_procRc, e_note, e_cycleSeqForwAnzahl, e_cycleSeqForwId,
          e_cycleSeqForwPrimerName, e_cycleSeqForwPrimerSequence, e_cycleSeqForwTraceAnzahl, e_cycleSeqForwTraceId, e_cycleSeqForwTraceName,
          e_cycleSeqForwTechnician, e_cycleSeqForwDate, e_cycleSeqForwTraceFormat );
		If (v_procRc = 4) Then
			Iterate l_fetch_data;
		ElseIf (v_procRc = 8) Then
			Set v_error = v_error+1;
			Update assembly_export_COI Set status='error', note=e_note Where id=e_id;
			Iterate l_fetch_data;
		End If;
		Set e_status='prep_cycleseqforw';
		Update assembly_export_COI Set status=e_status, note=e_note, cycleSeqForwAnzahl=e_cycleSeqForwAnzahl, cycleSeqForwId=e_cycleSeqForwId,
          cycleSeqForwPrimerName=e_cycleSeqForwPrimerName, cycleSeqForwPrimerSequence=e_cycleSeqForwPrimerSequence,
          cycleSeqForwTraceAnzahl=e_cycleSeqForwTraceAnzahl, cycleSeqForwTraceId=e_cycleSeqForwTraceId,
          cycleSeqForwTraceName=e_cycleSeqForwTraceName, cycleSeqForwTechnician=e_cycleSeqForwTechnician,
          cycleSeqForwDate=e_cycleSeqForwDate, cycleSeqForwTraceFormat=e_cycleSeqForwTraceFormat
          Where id=e_id;
	End If;

    /* Lade Felder aus Tabelle cyclesequencing, direction=reverse */
    if e_status='prep_cycleseqforw' Then
		Call loadCycleSequencingData(e_workflowId, e_extractionId, 'reverse', e_assemPlateSuffix, e_assemNotes,
          v_procRc, e_note, e_cycleSeqRevAnzahl, e_cycleSeqRevId,
          e_cycleSeqRevPrimerName, e_cycleSeqRevPrimerSequence, e_cycleSeqRevTraceAnzahl, e_cycleSeqRevTraceId, e_cycleSeqRevTraceName,
          e_cycleSeqRevTechnician, e_cycleSeqRevDate, e_cycleSeqRevTraceFormat );
		If (v_procRc = 4) Then
			Iterate l_fetch_data;
		ElseIf (v_procRc = 8) Then
			Set v_error = v_error+1;
			Update assembly_export_COI Set status='error', note=e_note Where id=e_id;
			Iterate l_fetch_data;
		End If;
		Set e_status='prep_cycleseqrev';
		Update assembly_export_COI Set status=e_status, note=e_note, cycleSeqRevAnzahl=e_cycleSeqRevAnzahl, cycleSeqRevId=e_cycleSeqRevId,
          cycleSeqRevPrimerName=e_cycleSeqRevPrimerName, cycleSeqRevPrimerSequence=e_cycleSeqRevPrimerSequence,
          cycleSeqRevTraceAnzahl=e_cycleSeqRevTraceAnzahl, cycleSeqRevTraceId=e_cycleSeqRevTraceId,
          cycleSeqRevTraceName=e_cycleSeqRevTraceName, cycleSeqRevTechnician=e_cycleSeqRevTechnician,
          cycleSeqRevDate=e_cycleSeqRevDate, cycleSeqRevTraceFormat=e_cycleSeqRevTraceFormat
          Where id=e_id;
	End If;

    /* Lade Felder aus Tabelle pcr */
    if e_status='prep_cycleseqrev' Then
		Call loadPcrData(e_workflowId, e_extractionId, e_assemPlateSuffix, v_procRc, e_note, e_pcrAnzahl, e_pcrId, e_pcrDate,
          e_pcrPrName, e_pcrPrSequence, e_pcrRevPrName, e_pcrRevPrSequence );
		If (v_procRc = 4) Then
			Iterate l_fetch_data;
		ElseIf (v_procRc = 8) Then
			Set v_error = v_error+1;
			Update assembly_export_COI Set status='error', note=e_note Where id=e_id;
			Iterate l_fetch_data;
		End If;
		Set e_status='prepCheck';
		Update assembly_export_COI Set status=e_status, note=e_note, pcrAnzahl=e_pcrAnzahl, pcrId=e_pcrId, pcrDate=e_pcrDate,
          pcrPrName=e_pcrPrName, pcrPrSequence=e_pcrPrSequence, pcrRevPrName=e_pcrRevPrName, pcrRevPrSequence=e_pcrRevPrSequence
          Where id=e_id;
	End If;

  --  If ((e_assemProgress = 'failed') AND (e_assem_failure_reason <> 'Parasite CON')) Then
    If (e_assemProgress = 'failed') Then
      Set e_status='ignore_failed';
      Update assembly_export_COI Set status=e_status Where id=e_id;
    End If;

  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_count AS CHAR)),' neue Fehler=',(CAST(v_error AS CHAR)) );

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `scIds` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `scIds`;
DELIMITER ;;
CREATE PROCEDURE `scIds`(IN p_start_id int(10) )
Begin
/**************** Aenderungen *********************************************************/
/*                                                            */
/**************************************************************************************/
  Declare param_max_anzahl int(10);  -- maximale Durchlaeufe der Verarbeitungsloop
  Declare v_id int(10);  -- id der assembly Tabelle
  Declare v_count int;   -- Zeilen Zaehler
  Declare v_done int;    -- Ende der Ergebnismenge

  Declare c_extr Cursor For Select id
    From assembly
    Where id>=p_start_id
    Order By id Limit 2000;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set param_max_anzahl = 1000;  -- maximale Durchlaeufe der Verarbeitungsloop
  Set v_count  = 0;
  Set v_done   = 0;

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into v_id;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_count = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
    Set v_count = v_count+1;

    Call scSingleId(v_id);

  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_count AS CHAR)) );

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `scPlate` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `scPlate`;
DELIMITER ;;
CREATE PROCEDURE `scPlate`(IN p_assembly_notes varchar(10000) )
Begin
/**************** Aenderungen *********************************************************/
/*                                                            */
/**************************************************************************************/
  Declare param_max_anzahl int(10);  -- maximale Durchlaeufe der Verarbeitungsloop
  Declare v_id int(10);  -- id der assembly Tabelle
  Declare v_count int;   -- Zeilen Zaehler
  Declare v_done int;    -- Ende der Ergebnismenge

  Declare c_extr Cursor For Select id
    From assembly
    Where notes=p_assembly_notes
    Order By id Limit 2000;
  -- Declare CONTINUE HANDLER FOR SQLSTATE '02000' Set v_done = 1;
  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set param_max_anzahl = 500;  -- maximale Durchlaeufe der Verarbeitungsloop
  Set v_count  = 0;
  Set v_done   = 0;

  Open c_extr;
  l_fetch_data: Loop
    Fetch c_extr Into v_id;
    If v_done Then
      Leave l_fetch_data;
    End If;

    If v_count = param_max_anzahl Then
      Leave l_fetch_data;
    End If;
    Set v_count = v_count+1;

    Call scSingleId(v_id);

  End Loop l_fetch_data;
  Close c_extr;

  Select CONCAT('Zeilenverarbeitet=',(CAST(v_count AS CHAR)) );

End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `scSingleId` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `scSingleId`;
DELIMITER ;;
CREATE PROCEDURE `scSingleId`(IN p_ass_id int(10) )
main_block: Begin
/*******************************************************************************************************/
/* Programmlogik                                                                                       */
/*   Suche Eintrag in der Tabelle assembly. Mache nichts, falls nicht vorhanden.                       */
/*   Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly, notes Feld darf nicht leer sein. */
/*   Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly.                                  */
/*   Schneide _NW von Platten-Suffix ab.                                                               */
/*   Ermittle die ParentFolderId mit Hilfe des Platten-Suffix.                                         */
/*   Ermittle die ConsensusFolderId.                                                                   */
/*   Ueberpruefe den Namen                                                                             */
/*   Ueberpruefe die consensus Sequenz                                                                 */
/*   Schreibe Ergebnis in Tabelle L2FscTable                                                      */
/*   09.11.2015 Speichere auch gen_consensus in Tabelle L2FscTable                                */
/*   12.11.2015 Ignoriere Eintrag mit status=ignore                                                    */
/*                                                                                                     */
/*******************************************************************************************************/
  /* Variable */
  Declare v_count int(10);             -- Anzahl Eintraege
  Declare v_error_indicator int(10);   -- Fehler aufgetreten
  Declare v_ann_doc_id int(11);        -- Annotated Document Id
  -- Declare v_consensus varchar(10000);  -- consensus aus Tabelle assembly
  Declare v_chars varchar(999);        -- Hilfsvariable
  Declare v_int1 int(10);              -- Hilfsvariable
  Declare v_int2 int(10);              -- Hilfsvariable
  Declare v_mapped int;                -- Hilfsvariable Suffixmapping
  Declare v_name varchar(999);         -- Hilfsvariable zur Namenssuche


  /* Variable zum Aufruf der Prozedur ExtractInfo */
  Declare h_procRc int;
  Declare h_reason varchar(99);
  Declare h_assemContam varchar(999);
  Declare h_assemNotes varchar(999);


  /* Variable fuer Tabelle L2FscTable  */
  Declare t_id int(10);
  Declare t_status varchar(999);
  Declare t_note varchar(999);
  Declare t_workflow_id int(10);         -- workflow aus Tabelle assembly
  Declare t_extraction_id varchar(999);  -- extraction_id aus Tabelle assembly
  Declare t_ass_notes varchar(10000);    -- notes aus Tabelle assembly
  Declare t_plate_suffix varchar(999);   -- Plattensuffix zur Bestimmung der parentfolder_id
  Declare t_consensus varchar(10000);    -- consensus aus Tabelle assembly
  Declare t_consensus_length int(10);
  Declare t_gen_parentfolder_id int(11);    -- parentfolder_id aus Tabelle gbol_geneious.folder
  Declare t_gen_nameparentfolder varchar(255);
  Declare t_gen_consensusfolder_id int(11); -- consensusfolder_id aus Tabelle gbol_geneious.folder
  Declare t_gen_ann_doc_id int(11);         -- id aus Tabelle gbol_geneious.annotated_document
  Declare t_gen_extraction_id varchar(999); -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document
  Declare t_gen_workflow varchar(999);      -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document
  Declare t_gen_name varchar(999);          -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document
  Declare t_gen_consensus varchar(10000);   -- Suchzeichenfolge in Tabelle gbol_geneious.annotated_document

  Set t_id = p_ass_id;
  Set t_status = 'Fehler';
  Set t_note = 'Interner Fehler';
  Set t_workflow_id = 0;
  Set t_extraction_id = 'leer';
  Set t_ass_notes = 'leer';
  Set t_plate_suffix = 'leer';
  Set t_consensus = 'leer';
  Set t_consensus_length = 0;
  Set t_gen_parentfolder_id = 0;
  Set t_gen_nameparentfolder = 'leer';
  Set t_gen_consensusfolder_id = 0;
  Set t_gen_ann_doc_id = 0;
  Set t_gen_extraction_id = 'leer';
  Set t_gen_workflow = 'leer';
  Set t_gen_name = 'leer';
  Set t_gen_consensus = 'leer';

  Set v_error_indicator = 0; -- Noch ist kein Fehler aufgetreten

  /* Suche Eintrag in der Tabelle assembly. Beende Verarbeitung falls nicht da */
  Select count(*), workflow, extraction_id, notes, consensus, Length(consensus)
    into v_count, t_workflow_id, t_extraction_id, t_ass_notes, t_consensus, t_consensus_length
    from assembly Where id=t_id;
  If v_count=0 Then
    Leave main_block;
  End If;

  /* Ignoriere Eintrag mit status=ignore */
  Select count(*) into v_count from L2FscTable Where status='ignore' and id=t_id;
  If v_count=1 Then
    Leave main_block;
  End If;


  /* Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly, notes Feld darf nicht leer sein */
  If ((t_ass_notes IS NULL) OR (Length(t_ass_notes) = 0)) Then
    Set t_status = 'Fehler';
    Set t_note = 'Notes Feld der Tabelle Assembly ist leer';
    Set v_error_indicator = 1; -- Fehler aufgetreten
  End If;

  /* Ermittle Platten-Suffix aus dem notes Feld der Tabelle assembly */
  If v_error_indicator=0 Then
    Set v_mapped = 0; -- Assembly notes Feld nicht auf Plattensuffix abgebildet
    Call mapSuffix(t_ass_notes, t_plate_suffix, v_mapped);
    If v_mapped = 0 Then
      Call ExtractInfo(t_ass_notes, 'P:', 'C:', h_procRc, h_reason, t_plate_suffix, h_assemContam, h_assemNotes);
      If (h_procRc > 0) Then
        Set t_status = 'Fehler';
        Set t_note = CONCAT('ExtractInfo_Reason=', h_reason, ';Notes=', t_ass_notes);
        Set v_error_indicator = 1; -- Fehler aufgetreten
      End If;
    End If;
  End If;

  /* Schneide _NW von Platten-Suffix ab */
  If v_error_indicator=0 Then
    Set v_int1=Locate('_NW', t_plate_suffix);
    If v_int1>1 then
      Set t_plate_suffix=Substring(t_plate_suffix,1,v_int1-1);
    End if;
  End If;

  /* Ermittle die ParentFolderId mit Hilfe von Platten-Suffix */
  If v_error_indicator=0 Then
    Select count(*), id, name
      Into v_count, t_gen_parentfolder_id, t_gen_nameparentfolder
      From gbol_geneious.folder
      Where name like CONCAT('GBOL\\', t_plate_suffix, '%') and name not like CONCAT('GBOL\\', t_plate_suffix, '\\_%')
        and name not like CONCAT('GBOL\\', t_plate_suffix, '-%');
    -- Where name like 'GBOL\_0505%' and name not like 'GBOL\_0505\_%' and name not like 'GBOL\_0505-%';  -- id=14215 name=GBOL_0505 (Col - Het)
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ermittle_Parentfolderid, Id ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_parentfolder_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Parentfolderid is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ermittle die ConsensusFolderId */
  If v_error_indicator=0 Then
    Select count(*), id
      Into v_count, t_gen_consensusfolder_id
      From gbol_geneious.folder
      Where parent_folder_id=t_gen_parentfolder_id and name='Consensus';  -- id=14219
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ermittle_Consensusfolder_id, Id ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_consensusfolder_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Consensusfolder_id is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ermittle den Namen aus der extraction_id, der Name muss die GBOL-Nr=sampleId enthalten */
  If v_error_indicator=0 Then
    /* Schneide den extraction-Suffix ab */
    -- Select Locate('.', 'abcd.z');  -- 5
    -- Select Substring('abcd.z',1,5-1);  -- abcd
    Set v_int1=Locate('.', t_extraction_id);
    If v_int1>1 then
      Set v_name=Substring(t_extraction_id,1,v_int1-1);
    Else
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Extraction_id ist ungueltig, ExtractionId=', t_extraction_id);
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ueberpruefe den Namen */
  If v_error_indicator=0 Then
    Set t_gen_name=CONCAT('<XML%<name>%', v_name, '%</name>%');
    Select count(*), id
      Into v_count, t_gen_ann_doc_id
      From gbol_geneious.annotated_document
      Where folder_id=t_gen_consensusfolder_id
        And plugin_document_xml like t_gen_name;
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ueberpruefe Namen, DocumentId ist nicht da oder nicht eindeutig, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    ElseIf (t_gen_ann_doc_id IS NULL) Then
      Set t_status = 'Fehler';
      Set t_note = 'Ueberpruefe Namen, Annotated_document_id is NULL';
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  /* Ueberpruefe die consensus Sequenz */
  If v_error_indicator=0 Then
    Set t_gen_consensus=CONCAT('<XML%<charSequence>', t_consensus, '</charSequence>%');
    Select count(*), id
      Into v_count, v_ann_doc_id
      From gbol_geneious.annotated_document
      Where folder_id=t_gen_consensusfolder_id and id=t_gen_ann_doc_id
        And plugin_document_xml like t_gen_consensus;
    If v_count<>1 Then
      Set t_status = 'Fehler';
      Set t_note = CONCAT('Ueberpruefe Consensus, Daten stimmen nicht ueberein, Count=', CAST(v_count AS CHAR) );
      Set v_error_indicator = 1; -- Fehler aufgetreten
    End if;
  End if;  -- v_error_indicator=0

  If v_error_indicator=0 Then
    Set t_status = 'ok';
    Set t_note = 'SmallConsensusCheck ok';
  End if;  -- v_error_indicator=0

  /* Schreibe Ergebnis in Tabelle L2FscTable */
  Select Count(id) into v_count From L2FscTable Where id = t_id;
  If v_count=0 Then
    /* insert, da Eintrag nicht vorhanden */
    -- Insert Into L2FcheckConsensus (id, note, ...) Values (1002, 'noteABC123', ...);
    Insert Into L2FscTable
     (id, status, note, workflow_id, extraction_id, ass_notes, plate_suffix, consensus, consensus_length,
      gen_parentfolder_id, gen_nameparentfolder, gen_consensusfolder_id, gen_ann_doc_id, gen_extraction_id, gen_workflow, gen_name,
      gen_consensus)
     Values (t_id, t_status, t_note, t_workflow_id, t_extraction_id, t_ass_notes, t_plate_suffix, t_consensus, t_consensus_length,
      t_gen_parentfolder_id, t_gen_nameparentfolder, t_gen_consensusfolder_id, t_gen_ann_doc_id,
      t_gen_extraction_id, t_gen_workflow, t_gen_name, t_gen_consensus);
  Else
    /* update, da Eintrag vorhanden */
    -- Update L2FcheckConsensus Set status=..., note=... Where id=t_id;
    Update L2FscTable
     Set status=t_status, note=t_note, workflow_id=t_workflow_id, extraction_id=t_extraction_id, ass_notes=t_ass_notes,
      plate_suffix=t_plate_suffix, consensus=t_consensus, consensus_length=t_consensus_length, gen_parentfolder_id=t_gen_parentfolder_id,
      gen_nameparentfolder=t_gen_nameparentfolder, gen_consensusfolder_id=t_gen_consensusfolder_id,
      gen_ann_doc_id=t_gen_ann_doc_id, gen_extraction_id=t_gen_extraction_id, gen_workflow=t_gen_workflow, gen_name=t_gen_name,
      gen_consensus=t_gen_consensus
     Where id=t_id;
  End If;

End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `syncAssemblyTables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `syncAssemblyTables`;
DELIMITER ;;
CREATE PROCEDURE `syncAssemblyTables`()
Begin




  Declare v_id int(10);
  Declare v_status varchar(999);
  Declare v_count int;
  Declare v_done int;



  Declare c_sync Cursor For Select id From assembly Where (id Not In (SELECT id From assembly_export_COI)) Order By id;


  Declare CONTINUE HANDLER FOR NOT FOUND Set v_done = 1;

  Set v_status = 'new';
  Set v_count  = 0;
  Set v_done   = 0;

  Open c_sync;

  Repeat
    Fetch c_sync Into v_id;
    If Not v_done Then

          Insert Into assembly_export_COI (id, workflowId, `status`, `exportDate`) Values (v_id, 0, v_status, CURRENT_TIMESTAMP);
          Set v_count = v_count+1;

    End If;
  Until v_done End Repeat;
  Close c_sync;

  Select CONCAT('Zeileneingefuegt=',(CAST(v_count AS CHAR)));
End ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `TestParseNotes` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DROP PROCEDURE IF EXISTS `TestParseNotes`;
DELIMITER ;;
CREATE PROCEDURE `TestParseNotes`(IN p_notes longtext,
   OUT p_procRc int, OUT p_reason varchar(999), OUT p_platte varchar(999), OUT p_contamination varchar(999), OUT p_note varchar(999) )
main_block: Begin

  Declare k_platte varchar(99);
  Declare k_contamination varchar(99);
  Declare k_note varchar(99);
  Declare k_platte_klein varchar(99);
  Declare k_contamination_klein varchar(99);
  Declare k_note_klein varchar(99);

  Declare v_locate_platte int;
  Declare v_locate_contamination int;
  Declare v_locate_note int;
  Declare v_length_notes int;
  Declare v_mehrfach int;

  Set k_platte = 'P:';
  Set k_contamination = 'C:';
  Set k_note = 'N:';
  Set k_platte_klein = 'p:';
  Set k_contamination_klein = 'c:';
  Set k_note_klein = 'n:';

  Set p_procRc = 8;
  Set p_reason = 'error';
  Set p_platte = 'leer';
  Set p_contamination = 'leer';
  Set p_note = 'leer';

  Set v_length_notes = Length(p_notes);
  If (v_length_notes = 0) Then
	Set p_procRc = 4;
	Set p_reason = 'Leerer NotesString';
    Leave main_block;
  End if;

  Set v_locate_platte = LOCATE(k_platte, p_notes);
  If (v_locate_platte = 0) then
    Set v_locate_platte = LOCATE(k_platte_klein, p_notes);
  End if;

  Set v_locate_contamination = LOCATE(k_contamination, p_notes);
  If (v_locate_contamination = 0) then
    Set v_locate_contamination = LOCATE(k_contamination_klein, p_notes);
  End if;

  Set v_locate_note = LOCATE(k_note, p_notes);
  If (v_locate_note = 0) then
    Set v_locate_note = LOCATE(k_note_klein, p_notes);
  End if;


  If (v_locate_platte > 0) Then
    Set v_mehrfach = LOCATE(k_platte, p_notes, v_locate_platte + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Platteninformation kommt mehrfach vor';
      Set p_platte = 'leer';
      Set p_contamination = 'leer';
      Set p_note = 'leer';
      Leave main_block;
    End if;
    Set v_mehrfach = LOCATE(k_platte_klein, p_notes, v_locate_platte + 1);
    If (v_mehrfach > 0) Then
      Set p_procRc = 8;
      Set p_reason = 'Platteninformation kommt mehrfach vor';
      Set p_platte = 'leer';
      Set p_contamination = 'leer';
      Set p_note = 'leer';
      Leave main_block;
    End if;
    If ((v_locate_platte < v_locate_contamination) and (v_locate_platte < v_locate_note)) then
      If (v_locate_contamination < v_locate_note) then
        If (v_locate_contamination = v_locate_platte + 2) then
          Set p_platte = 'leer';
        Else
          Set p_platte = Substring(p_notes,v_locate_platte+2,v_locate_contamination-v_locate_platte-2);
        End if;
      Else
        If (v_locate_note = v_locate_platte + 2) then
          Set p_platte = 'leer';
        Else
          Set p_platte = Substring(p_notes,v_locate_platte+2,v_locate_note-v_locate_platte-2);
        End if;
      End if;
    ElseIf (v_locate_platte < v_locate_contamination) Then
      If (v_locate_contamination = v_locate_platte + 2) then
        Set p_platte = 'leer';
      Else
        Set p_platte = Substring(p_notes,v_locate_platte+2,v_locate_contamination-v_locate_platte-2);
      End if;
    ElseIf (v_locate_platte < v_locate_note) Then
      If (v_locate_note = v_locate_platte + 2) then
        Set p_platte = 'leer';
      Else
        Set p_platte = Substring(p_notes,v_locate_platte+2,v_locate_note-v_locate_platte-2);
      End if;
    Else
      If (v_length_notes = v_locate_platte + 1) then
        Set p_platte = 'leer';
      Else
        Set p_platte = Substring(p_notes,v_locate_platte+2,v_length_notes-v_locate_platte-1);
      End if;
    End if;
    Set p_platte = Trim(p_platte);
  End if;

  Set p_procRc = 0;
  Set p_reason = 'Notes Eintrag zerlegt';







End main_block ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Final view structure for view `sampleId_numeric`
--

/*!50001 DROP TABLE IF EXISTS `sampleId_numeric`*/;
/*!50001 DROP VIEW IF EXISTS `sampleId_numeric`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE */
/*!50001 VIEW `sampleId_numeric` AS select `e`.`sampleId` AS `sampleId`,if((locate('GBOL',`e`.`sampleId`) = 1),cast(concat('1',cast(right(`e`.`sampleId`,(length(`e`.`sampleId`) - length('GBOL-'))) as char(32) charset utf8)) as signed),if((locate('Ar',`e`.`sampleId`) > 0),cast(concat('1',cast(right(`e`.`sampleId`,(length(`e`.`sampleId`) - length('ZFMK Ar'))) as char(32) charset utf8)) as signed),if((locate('DNA',`e`.`sampleId`) > 0),cast(concat('1',cast(right(`e`.`sampleId`,(length(`e`.`sampleId`) - length('ZFMK-DNA-'))) as char(32) charset utf8)) as signed),if((locate('TIS',`e`.`sampleId`) > 0),cast(concat('1',cast(right(`e`.`sampleId`,(length(`e`.`sampleId`) - length('ZFMK-TIS-'))) as char(32) charset utf8)) as signed),'')))) AS `sampleId_numeric`,`e`.`extractionId` AS `extractionId`,`p`.`name` AS `plate` from (`extraction` `e` left join `plate` `p` on((`p`.`id` = `e`.`plate`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-04-20 22:06:20
