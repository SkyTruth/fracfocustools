# Sequel Pro dump
# Version 1191
# http://code.google.com/p/sequel-pro
#
# Host: ewn2.skytruth.org (MySQL 5.1.66-0ubuntu0.10.04.3)
# Database: NRC_Data
# Generation Time: 2013-01-17 16:58:41 -0500
# ************************************************************

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table EXPORT_FracFocusChemical
# ------------------------------------------------------------

DROP VIEW IF EXISTS `EXPORT_FracFocusChemical`;

CREATE TABLE `EXPORT_FracFocusChemical` (
   `c_seqid` INT(11) NOT NULL DEFAULT '0',
   `pdf_seqid` INT(11) NOT NULL DEFAULT NULL,
   `api` VARCHAR(20) NOT NULL DEFAULT NULL,
   `fracture_date` DATE NOT NULL DEFAULT NULL,
   `row` INT(11) NOT NULL DEFAULT NULL,
   `trade_name` VARCHAR(200) NOT NULL DEFAULT '',
   `supplier` VARCHAR(50) NOT NULL DEFAULT '',
   `purpose` VARCHAR(200) NOT NULL DEFAULT '',
   `ingredients` VARCHAR(100) NOT NULL DEFAULT '',
   `cas_number` VARCHAR(50) NOT NULL DEFAULT '',
   `additive_concentration` VARBINARY(22) NOT NULL DEFAULT '',
   `hf_fluid_concentration` VARBINARY(22) NOT NULL DEFAULT '',
   `comments` VARCHAR(200) NOT NULL DEFAULT '',
   `cas_type` VARCHAR(20) NOT NULL DEFAULT ''
) ENGINE=MyISAM;;



# Dump of table EXPORT_FracFocusCombined
# ------------------------------------------------------------

DROP VIEW IF EXISTS `EXPORT_FracFocusCombined`;

CREATE TABLE `EXPORT_FracFocusCombined` (
   `r_seqid` INT(11) NOT NULL DEFAULT '0',
   `pdf_seqid` INT(11) NOT NULL DEFAULT NULL,
   `api` VARCHAR(20) NOT NULL DEFAULT NULL,
   `fracture_date` DATE NOT NULL DEFAULT NULL,
   `state` VARCHAR(20) NOT NULL DEFAULT '',
   `county` VARCHAR(20) NOT NULL DEFAULT '',
   `operator` VARCHAR(50) NOT NULL DEFAULT '',
   `well_name` VARCHAR(50) NOT NULL DEFAULT '',
   `production_type` VARCHAR(10) NOT NULL DEFAULT '',
   `latitude` VARBINARY(22) NOT NULL DEFAULT '',
   `longitude` VARBINARY(22) NOT NULL DEFAULT '',
   `datum` VARCHAR(8) NOT NULL DEFAULT '',
   `true_vertical_depth` VARBINARY(22) NOT NULL DEFAULT '',
   `total_water_volume` VARBINARY(22) NOT NULL DEFAULT '',
   `published` VARBINARY(19) NOT NULL DEFAULT '',
   `c_seqid` INT(11) NOT NULL DEFAULT '0',
   `row` INT(11) NOT NULL DEFAULT NULL,
   `trade_name` VARCHAR(200) NOT NULL DEFAULT '',
   `supplier` VARCHAR(50) NOT NULL DEFAULT '',
   `purpose` VARCHAR(200) NOT NULL DEFAULT '',
   `ingredients` VARCHAR(100) NOT NULL DEFAULT '',
   `cas_number` VARCHAR(50) NOT NULL DEFAULT '',
   `additive_concentration` VARBINARY(22) NOT NULL DEFAULT '',
   `hf_fluid_concentration` VARBINARY(22) NOT NULL DEFAULT '',
   `comments` VARCHAR(200) NOT NULL DEFAULT '',
   `cas_type` VARCHAR(20) NOT NULL DEFAULT ''
) ENGINE=MyISAM;;



# Dump of table EXPORT_FracFocusReport
# ------------------------------------------------------------

DROP VIEW IF EXISTS `EXPORT_FracFocusReport`;

CREATE TABLE `EXPORT_FracFocusReport` (
   `r_seqid` INT(11) NOT NULL DEFAULT '0',
   `pdf_seqid` INT(11) NOT NULL DEFAULT NULL,
   `api` VARCHAR(20) NOT NULL DEFAULT NULL,
   `fracture_date` DATE NOT NULL DEFAULT NULL,
   `state` VARCHAR(20) NOT NULL DEFAULT '',
   `county` VARCHAR(20) NOT NULL DEFAULT '',
   `operator` VARCHAR(50) NOT NULL DEFAULT '',
   `well_name` VARCHAR(50) NOT NULL DEFAULT '',
   `production_type` VARCHAR(10) NOT NULL DEFAULT '',
   `latitude` VARBINARY(22) NOT NULL DEFAULT '',
   `longitude` VARBINARY(22) NOT NULL DEFAULT '',
   `datum` VARCHAR(8) NOT NULL DEFAULT '',
   `true_vertical_depth` VARBINARY(22) NOT NULL DEFAULT '',
   `total_water_volume` VARBINARY(22) NOT NULL DEFAULT '',
   `published` VARBINARY(19) NOT NULL DEFAULT ''
) ENGINE=MyISAM;;





DROP TABLE `EXPORT_FracFocusReport`;
CREATE ALGORITHM=UNDEFINED DEFINER=`scraper`@`%` SQL SECURITY DEFINER VIEW `EXPORT_FracFocusReport`
AS select
   `FracFocusReport`.`seqid` AS `r_seqid`,
   `FracFocusReport`.`pdf_seqid` AS `pdf_seqid`,
   `FracFocusReport`.`api` AS `api`,
   `FracFocusReport`.`fracture_date` AS `fracture_date`,ifnull(`FracFocusReport`.`state`,'') AS `state`,ifnull(`FracFocusReport`.`county`,'') AS `county`,ifnull(`FracFocusReport`.`operator`,'') AS `operator`,ifnull(`FracFocusReport`.`well_name`,'') AS `well_name`,ifnull(`FracFocusReport`.`production_type`,'') AS `production_type`,ifnull(`FracFocusReport`.`latitude`,'') AS `latitude`,ifnull(`FracFocusReport`.`longitude`,'') AS `longitude`,ifnull(`FracFocusReport`.`datum`,'') AS `datum`,ifnull(`FracFocusReport`.`true_vertical_depth`,'') AS `true_vertical_depth`,ifnull(`FracFocusReport`.`total_water_volume`,'') AS `total_water_volume`,ifnull(`FracFocusReport`.`published`,'') AS `published`
from `FracFocusReport`;


DROP TABLE `EXPORT_FracFocusChemical`;
CREATE ALGORITHM=UNDEFINED DEFINER=`scraper`@`%` SQL SECURITY DEFINER VIEW `EXPORT_FracFocusChemical`
AS select
   `FracFocusReportChemical`.`seqid` AS `c_seqid`,
   `FracFocusReportChemical`.`pdf_seqid` AS `pdf_seqid`,
   `FracFocusReportChemical`.`api` AS `api`,
   `FracFocusReportChemical`.`fracture_date` AS `fracture_date`,
   `FracFocusReportChemical`.`row` AS `row`,ifnull(`FracFocusReportChemical`.`trade_name`,'') AS `trade_name`,ifnull(`FracFocusReportChemical`.`supplier`,'') AS `supplier`,ifnull(`FracFocusReportChemical`.`purpose`,'') AS `purpose`,ifnull(`FracFocusReportChemical`.`ingredients`,'') AS `ingredients`,ifnull(`FracFocusReportChemical`.`cas_number`,'') AS `cas_number`,ifnull(`FracFocusReportChemical`.`additive_concentration`,'') AS `additive_concentration`,ifnull(`FracFocusReportChemical`.`hf_fluid_concentration`,'') AS `hf_fluid_concentration`,ifnull(`FracFocusReportChemical`.`comments`,'') AS `comments`,ifnull(`FracFocusReportChemical`.`cas_type`,'') AS `cas_type`
from `FracFocusReportChemical`;


DROP TABLE `EXPORT_FracFocusCombined`;
CREATE ALGORITHM=UNDEFINED DEFINER=`scraper`@`%` SQL SECURITY DEFINER VIEW `EXPORT_FracFocusCombined`
AS select
   `r`.`r_seqid` AS `r_seqid`,
   `r`.`pdf_seqid` AS `pdf_seqid`,
   `r`.`api` AS `api`,
   `r`.`fracture_date` AS `fracture_date`,ifnull(`r`.`state`,'') AS `state`,ifnull(`r`.`county`,'') AS `county`,ifnull(`r`.`operator`,'') AS `operator`,ifnull(`r`.`well_name`,'') AS `well_name`,ifnull(`r`.`production_type`,'') AS `production_type`,ifnull(`r`.`latitude`,'') AS `latitude`,ifnull(`r`.`longitude`,'') AS `longitude`,ifnull(`r`.`datum`,'') AS `datum`,ifnull(`r`.`true_vertical_depth`,'') AS `true_vertical_depth`,ifnull(`r`.`total_water_volume`,'') AS `total_water_volume`,ifnull(`r`.`published`,'') AS `published`,
   `c`.`c_seqid` AS `c_seqid`,
   `c`.`row` AS `row`,ifnull(`c`.`trade_name`,'') AS `trade_name`,ifnull(`c`.`supplier`,'') AS `supplier`,ifnull(`c`.`purpose`,'') AS `purpose`,ifnull(`c`.`ingredients`,'') AS `ingredients`,ifnull(`c`.`cas_number`,'') AS `cas_number`,ifnull(`c`.`additive_concentration`,'') AS `additive_concentration`,ifnull(`c`.`hf_fluid_concentration`,'') AS `hf_fluid_concentration`,ifnull(`c`.`comments`,'') AS `comments`,ifnull(`c`.`cas_type`,'') AS `cas_type`
from (`EXPORT_FracFocusReport` `r` join `EXPORT_FracFocusChemical` `c` on((`r`.`pdf_seqid` = `c`.`pdf_seqid`)));



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
