/*
SQLyog Ultimate v11.33 (64 bit)
MySQL - 5.7.16-0ubuntu0.16.04.1 : Database - olx
*********************************************************************
*/


/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`olx` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `olx`;

/*Table structure for table `cars` */

DROP TABLE IF EXISTS `cars`;

CREATE TABLE `cars` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `province` varchar(255) DEFAULT NULL,
  `description` mediumtext,
  `price` int(255) DEFAULT NULL,
  `contact_person` varchar(255) DEFAULT NULL,
  `source_site` varchar(50) DEFAULT NULL,
  `year` int(11) DEFAULT NULL,
  `brand` varchar(255) DEFAULT NULL,
  `model` varchar(150) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `ownership` varchar(10) DEFAULT NULL,
  `engine_capacity` smallint(6) DEFAULT NULL,
  `engine_type` varchar(25) DEFAULT NULL,
  `transmission` varchar(25) DEFAULT NULL,
  `doors` smallint(6) DEFAULT NULL,
  `color` varchar(20) DEFAULT NULL,
  `airbags` varchar(20) DEFAULT NULL,
  `satnav` varchar(20) DEFAULT NULL,
  `radio` varchar(10) DEFAULT NULL,
  `cd_player` varchar(10) DEFAULT NULL,
  `posted` varchar(50) DEFAULT NULL,
  `nego` varchar(20) NOT NULL,
  `uploaded_by` varchar(25) NOT NULL,
  `phone` varchar(25) NOT NULL,
  `seen` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4637 DEFAULT CHARSET=latin1;
