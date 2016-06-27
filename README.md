German Barcode of Life
===================

![GBoL Logo](https://raw.githubusercontent.com/ZFMK/GermanBarcodeofLife/master/WebPortal/gbol_portal/static/images/logo.png)


## Web portal and data broker for the German Barcode of Life Project (GBoL) ##

### Web Portal: ###
The GBoL web portal [www.bolgermany.de](https://www.bolgermany.de) is a central part of the GBoL infrastructure.
Main aspects of the portal are:

* presentation of the GBoL project
* up to date informaton about the project
* registration for specialists
* order material for field collection
* presentation and publication of results
* interdisciplinary access
* multilangual

### Data Broker: ###
The GBoL data broker is used to transfer and mediate data between 
different systems that interact with GBoL; either for data management, 
data storage or publication. It consists of the following three modules:

* __Lims2Fims__: Data exchange between Laboratory Management System
  and the DiversityWorkbench module DiversityCollection
* __sync_gbol_data__: mediation and integration of GBoL data between 
  collection management system(s) of GBoL partners and the GBoL web portal
* __publish_gbol_data__: allocation of GBoL data to external data systems
  via BioCASE provider software

