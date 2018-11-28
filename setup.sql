-- create db and user
CREATE DATABASE FORCE_DIRECTED_GRAPHS
CREATE USER 'mysql'@'localhost' IDENTIFIED BY 'mysql_password';
GRANT ALL ON FORCE_DRIECTED_GRAPHS.* TO 'mysql'@'localhost';
FLUSH PRIVILEGES;

-- create tables for nodes and edges
USE FORCE_DIRECTED_GRAPHS
CREATE TABLE NODES(
	GROUP INT NOT NULL,
	NAME VARCHAR(255) NOT NULL PRIMARY KEY
);

CREATE TABLE EDGES(
	SOURCE INT NOT NULL,
	TARGET INT NOT NULL,
	VALUE INT NOT NULL
);
