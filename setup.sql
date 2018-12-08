-- create db and use
DROP DATABASE IF EXISTS `FORCE_DIRECTED_GRAPHS`;
CREATE DATABASE `FORCE_DIRECTED_GRAPHS`;

CREATE USER 'tempuser'@'localhost' IDENTIFIED BY 'temppass';
GRANT ALL PRIVILEGES ON FORCE_DRIECTED_GRAPHS.* TO 'tempuser'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

USE `FORCE_DIRECTED_GRAPHS`;

-- create tables for nodes and edges
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `VERT`;
SET FOREIGN_KEY_CHECKS = 1;
CREATE TABLE `VERT` (
	`ID` 		INT 	NOT NULL AUTO_INCREMENT,
	`COLOR` 	INT 	NOT NULL,
	`DEGREE`	INT 	NOT NULL,
	PRIMARY KEY (`ID`)
);

DROP TABLE IF EXISTS `EDGE`;
CREATE TABLE `EDGE` (
	`SOURCE`	INT	NOT NULL,
	`TARGET` 	INT	NOT NULL,
	`WEIGHT` 	INT	NOT NULL,
	FOREIGN KEY (`SOURCE`) REFERENCES VERT(`ID`),
       	FOREIGN KEY (`TARGET`) REFERENCES VERT(`ID`)
);

DROP TABLE IF EXISTS `CLIQUE`;
CREATE TABLE `CLIQUE` (
	`ID`	 	INT 		NOT NULL AUTO_INCREMENT,
	`AMMO`	 	INT 		NOT NULL,
	`MEMBERS`	LONGTEXT	NOT NULL,
	CHECK (JSON_VALID(`MEMBERS`)),
	PRIMARY KEY (`ID`)
);
