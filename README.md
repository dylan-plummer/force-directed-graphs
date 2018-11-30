# GRAPHMON JOHNSQL

DYLAN PLUMMER		| FRONTEND

MICHAEL TUCCI		| BACKEND

KEVIN SZMYD		| DBA

LUCAS INVERNIZZI	| MANAGER

////////////////////////////////////////////////////////////////////////////////

SQL TABLES:

	VERT					EDGE
	|-> ID 		<INT, PRIMARY>		|-> SOURCE <FOREIGN KEY [ID]>
	|-> COLOR	<INT>			|-> TARGET <FOREIGN KEY [ID]>
	|-> DEGREE	<INT>			|-> WEIGHT <INT>

	CLIQUE
	|-> ID		<INT, PRIMARY>
	|-> AMMO	<INT>
	|-> MEMBERS	<JSON>

///////////////////////////////////////////////////////////////////////////////

INSTALLATION:
	CONFIGURE HOST IN config.ini UNDER [app]

	LOG ONTO MYSQL SERVER WITH GRANT USER PRIVILEGE (USING -p FOR WHEEL SQL USER)

	RUN -> SOURCE setup.sql

	EXIT BACK TO BASH

	PIP INSTALL ANY MISSING LIBRARIES

	RUN -> sudo python run.py
