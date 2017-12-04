/*
SQLyog Ultimate v11.11 (64 bit)
MySQL - 5.5.52-MariaDB : Database - warframe
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`warframe` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `warframe`;

/*Table structure for table `build_item` */

DROP TABLE IF EXISTS `build_item`;

CREATE TABLE `build_item` (
  `id` int(16) NOT NULL AUTO_INCREMENT,
  `name_en` varchar(32) NOT NULL,
  `name_zh` varchar(32) DEFAULT NULL,
  `item_type` int(16) DEFAULT NULL COMMENT '1 warframe',
  `build_id` int(16) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=382 DEFAULT CHARSET=utf8;

/*Table structure for table `item` */

DROP TABLE IF EXISTS `item`;

CREATE TABLE `item` (
  `id` int(6) NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name_en` varchar(32) NOT NULL COMMENT '英文物品名',
  `name_zh` varchar(32) DEFAULT NULL,
  `type` varchar(32) DEFAULT NULL,
  `category` varchar(32) DEFAULT '',
  `rarity` varchar(16) DEFAULT '',
  `mod_max_rank` tinyint(6) DEFAULT '0',
  `wiki` varchar(64) DEFAULT NULL,
  `wiki_zh` varchar(64) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `upload_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `build_item_id` varchar(32) DEFAULT NULL COMMENT 'wf.build的物品ID',
  `item_img` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `name` (`name_en`),
  KEY `namezh` (`name_zh`),
  KEY `type` (`type`)
) ENGINE=InnoDB AUTO_INCREMENT=1595 DEFAULT CHARSET=utf8;

/*Table structure for table `item_build_record` */

DROP TABLE IF EXISTS `item_build_record`;

CREATE TABLE `item_build_record` (
  `id` bigint(16) NOT NULL AUTO_INCREMENT,
  `item_type` tinyint(4) DEFAULT NULL,
  `build_item_id` bigint(16) NOT NULL,
  `name_en` varchar(32) NOT NULL,
  `name_zh` varchar(128) DEFAULT NULL,
  `url` varchar(256) NOT NULL,
  `build_des` varchar(128) DEFAULT NULL,
  `pop` float DEFAULT NULL,
  `formas` tinyint(4) DEFAULT NULL,
  `record_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `build_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8799 DEFAULT CHARSET=utf8;

/*Table structure for table `item_price_record` */

DROP TABLE IF EXISTS `item_price_record`;

CREATE TABLE `item_price_record` (
  `id` bigint(10) unsigned NOT NULL AUTO_INCREMENT,
  `item_id` bigint(10) DEFAULT NULL,
  `name_en` varchar(32) NOT NULL,
  `type` varchar(32) NOT NULL,
  `cheapest_price` int(11) NOT NULL,
  `top_avg` int(11) NOT NULL,
  `top_count` int(11) NOT NULL,
  `all_avg` int(11) NOT NULL,
  `all_count` int(11) NOT NULL,
  `top_rec` varchar(64) NOT NULL DEFAULT '',
  `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `record_time` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=723303 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
