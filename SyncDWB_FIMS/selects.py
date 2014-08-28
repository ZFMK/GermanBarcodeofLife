#!/usr/bin/python
# -*- coding: utf8 -*-
"""
	All Queries for communication to databases
"""


class queries():
	def __init__(self, project=1):
		if project==1:
			self.project = "p.ProjectID<=30000 AND p.ProjectID>=26778"
		elif project==2:
			self.project = "p.ProjectID=26793"
		self.target_table = 'GBOL_FIMS'
		self.temp_table = "GBOL_FIMS_tmp"

	def dwb_all(self):
		q = """SELECT c.CollectionSpecimenID
		,p.ProjectID
		,cast(pp.Project as varchar(50)) as Projectname
		,CAST(c.AccessionNumber AS VARCHAR(50)) AS GBOL_Nr
		,CAST(c.DepositorsName AS VARCHAR(255)) AS Einsender
		,CAST(c.DepositorsAccessionNumber AS VARCHAR(255)) AS EinsenderNummer
		,CAST(e.CollectorsEventNumber AS VARCHAR(50)) AS Feldnummer
		,CAST(iu.OrderCache AS VARCHAR(255)) AS Ordnung
		,CAST(iu.FamilyCache AS VARCHAR(255)) AS Familie
		,CAST(i.TaxonomicName AS VARCHAR(255)) AS Taxon_Name
		,CAST(i.IdentificationQualifier AS VARCHAR(50)) AS Taxon_Qualifier
		,CAST(i.ResponsibleName AS VARCHAR(255)) AS Bestimmer_Name
		,CAST(i.NameURI AS VARCHAR(255)) AS Taxon_URI
		,ISNULL(cast(i.IdentificationDay as varchar(2))+'.'+cast(i.IdentificationMonth as varchar(2))+'.'+cast(i.IdentificationYear as varchar(4)), cast(i.IdentificationDateSupplement as varchar(255))) AS Bestimmungs_Datum
		,CAST(i.Notes AS VARCHAR(max)) AS Bem_Taxonomie
		,CAST(iu.LifeStage AS VARCHAR(255)) AS Entwicklungsstadium
		,CAST(iu.Gender AS VARCHAR(50)) AS Sex
		,CAST(iu.NumberOfUnits AS SMALLINT) AS Number_of_Units
		,CAST(iu.Notes AS VARCHAR(max)) AS Bem_Probe
		,CAST(iu.UnitDescription AS VARCHAR(max)) AS Tissue_Description
		,CAST(cp.AccessionNumber AS VARCHAR(50)) AS Number_Part
		,CAST(cp.PreparationMethod AS VARCHAR(max)) AS Fixierungsmethode
		,CAST(e.RowGUID AS VARCHAR(50)) AS CollectionEventGUID
		,CAST(e.CountryCache AS VARCHAR(50)) AS Land
		,CAST(el13.Location1 AS VARCHAR(255)) AS Bundesland
		,CAST(el13.Location2 AS VARCHAR(255)) AS Bundesland_URI
		,CAST(el7.Location1 AS VARCHAR(max)) AS Fundort
		,CAST(e.LocalityDescription AS VARCHAR(max)) AS Fundortbeschreibung
		,CAST(el8.Location1 AS VARCHAR(255)) AS Longitude
		,CAST(el8.Location2 AS VARCHAR(255)) AS Latitude
		,CAST(el2.Location1 AS VARCHAR(255)) AS GKS_R
		,CAST(el2.Location2 AS  VARCHAR(255)) AS GKS_H
		,CASE WHEN el8.Location1 is null
			THEN cast(el2.LocationAccuracy AS  VARCHAR(50))
			ELSE cast(el8.LocationAccuracy AS  VARCHAR(50)) END AS Geo_Accuracy
		,CASE WHEN el8.Location1 is null
			THEN cast(el2.RecordingMethod AS  VARCHAR(500))
			ELSE cast(el8.RecordingMethod AS  VARCHAR(500)) END AS Geo_Method
		,CASE WHEN el8.Location1 is null
			THEN cast(el2.LocationNotes AS  VARCHAR(max))
			ELSE cast(el8.LocationNotes AS  VARCHAR(max)) END AS Geo_Notes
		,CAST(el4.Location1 AS VARCHAR(255)) AS Altitude_from
		,CAST(el4.Location2 AS  VARCHAR(255)) AS Altitude_to
		,cast(el4.LocationAccuracy AS  VARCHAR(50)) as Altitude_accuracy
		,cast(el4.LocationNotes AS  VARCHAR(max)) as Altitude_notes
		,CAST((select CollectorsName + '; ' AS 'data()' from CollectionAgent where CollectionSpecimenID=c.CollectionSpecimenID order by CollectorsSequence ASC for xml path('')) AS VARCHAR(255)) AS Sammler
		,ISNULL(cast(e.CollectionDay as varchar)+'.'+cast(e.CollectionMonth as varchar)+'.'+cast(e.CollectionYear as varchar), e.CollectionDateSupplement) AS Sammel_Datum
		,CAST(e.CollectingMethod AS VARCHAR(max)) AS Sammelmethode
		,CAST(ca.Notes AS VARCHAR(max)) AS Bem_Sammeln
		,CAST(e.HabitatDescription AS VARCHAR(max)) AS Habitat
		,CAST(a.AnalysisResult AS VARCHAR(max)) AS Barcode
		,CAST(a.ResponsibleName AS VARCHAR(255)) AS Analysis_Person
		,CAST(a.AnalysisDate AS VARCHAR(50)) AS Analysis_Date
		,CAST(a.AnalysisNumber AS VARCHAR(50)) AS Analysis_Number
		,CAST(c.Problems AS VARCHAR(max)) AS Problems
		,CAST(c.OriginalNotes AS VARCHAR(max)) AS Original_Notes
		,CAST(c.AdditionalNotes AS VARCHAR(max)) AS Additional_Notes
		,CAST(c.InternalNotes AS VARCHAR(max)) AS Sammeltabelle
		,CAST(co.CollectionName AS VARCHAR(255)) AS Collection
		,CAST(ma.DisplayText AS VARCHAR(50)) AS Material_Category
		,CAST(cp.StorageLocation AS VARCHAR(255)) AS Storage_Location
		,convert(datetime, cp.PreparationDate, 120) AS Preparation_Date
		,CAST(cp.Notes AS VARCHAR(max)) AS Notes_for_part
		,c.RowGUID
		,CAST(c.DataWithholdingReason AS VARCHAR(255)) AS BlockedUntil
		,CAST(c.LogCreatedBy AS VARCHAR(50)) AS Specimen_Created_by
		,CAST(c.LogUpdatedBy AS VARCHAR(50)) AS Specimen_Changed_by
		,convert(datetime, c.LogCreatedWhen, 120) AS Specimen_Created
		,convert(datetime, c.LogUpdatedWhen, 120) AS Specimen_Changed
		FROM CollectionSpecimen AS c
			LEFT JOIN CollectionAgent AS ca ON ca.CollectionSpecimenID=c.CollectionSpecimenID
			LEFT JOIN IdentificationUnit AS iu ON (iu.CollectionSpecimenID=c.CollectionSpecimenID AND iu.DisplayOrder=1)
			LEFT JOIN IdentificationUnitAnalysis a on (a.IdentificationUnitID=iu.IdentificationUnitID and a.CollectionSpecimenID=iu.CollectionSpecimenID and a.AnalysisID=95)
			LEFT JOIN Identification AS i ON (i.CollectionSpecimenID=c.CollectionSpecimenID AND i.IdentificationUnitID=iu.IdentificationUnitID)
			LEFT JOIN CollectionSpecimenPart AS cp ON cp.CollectionSpecimenID=c.CollectionSpecimenID
			LEFT JOIN CollectionEvent AS e ON e.CollectionEventID=c.CollectionEventID
			LEFT JOIN CollectionEventLocalisation AS el7 ON (el7.CollectionEventID=e.CollectionEventID AND el7.LocalisationSystemID=7)
			LEFT JOIN CollectionEventLocalisation AS el8 ON (el8.CollectionEventID=e.CollectionEventID AND el8.LocalisationSystemID=8)
			LEFT JOIN CollectionEventLocalisation AS el4 ON (el4.CollectionEventID=e.CollectionEventID AND el4.LocalisationSystemID=4)
			LEFT JOIN CollectionEventLocalisation AS el2 ON (el2.CollectionEventID=e.CollectionEventID AND el2.LocalisationSystemID=2)
			LEFT JOIN CollectionEventLocalisation AS el13 ON (el13.CollectionEventID=e.CollectionEventID AND el13.LocalisationSystemID=13)
			LEFT JOIN IdentificationUnitAnalysis iua ON (iua.CollectionSpecimenID=c.CollectionSpecimenID AND iua.IdentificationUnitID=iu.IdentificationUnitID and iua.AnalysisID=104)
			LEFT JOIN CollectionProject p ON p.CollectionSpecimenID=c.CollectionSpecimenID
			LEFT JOIN ProjectProxy pp ON pp.ProjectID=p.ProjectID
			LEFT JOIN Collection co ON co.CollectionID=cp.CollectionID
			LEFT JOIN COLLMaterialCategory_enum ma ON cp.MaterialCategory=ma.Code
		WHERE %s""" % self.project
		return q.replace('\t','').replace('\n',' ')

	def columns_headers(self):
		""" helps to build `insert` query """
		q = """SELECT `COLUMN_NAME`
			FROM `INFORMATION_SCHEMA`.`COLUMNS`
			WHERE `TABLE_NAME`='%s'""" % self.temp_table
		return q.replace('\t','').replace('\n',' ')

	def all_ids(self):
		""" All Collection Specimen IDs from target table """
		return """select p.CollectionSpecimenID from %s p where %s order by p.CollectionSpecimenID""" % (self.target_table, self.project)

	def finish(self):
		""" truncate GBOL_FIMS table, copy all entries from temp table into GBOL_FIMS, empty temp-table """
		q = """insert into {0} select * from {1}""".format(self.target_table, self.temp_table)
		return q


class DictDiffer(object):
	# http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary/1165552#1165552
	"""
	Calculate the difference between two dictionaries as:
	(1) items added
	(2) items removed
	(3) keys same in both but changed values
	(4) keys same in both and unchanged values
	"""
	def __init__(self, current_dict, past_dict):
		self.current_dict, self.past_dict = current_dict, past_dict
		self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
		self.intersect = self.set_current.intersection(self.set_past)
	def added(self):
		return self.set_current - self.intersect
	def removed(self):
		return self.set_past - self.intersect
	def changed(self):
		return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
	def unchanged(self):
		return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])
