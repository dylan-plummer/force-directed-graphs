# GRAPHMON JOHNSQL

### Extracted Cliques:
<img src="https://github.com/jumproper/force-directed-graphs/blob/master/demos/cliques.JPG" alt="drawing" width="400"/>

### Component Graphs:
<img src="https://github.com/jumproper/force-directed-graphs/blob/master/demos/component.JPG" alt="drawing" width="400"/>

### Trees:
<img src="https://github.com/jumproper/force-directed-graphs/blob/master/demos/trees.JPG" alt="drawing" width="400"/>

### Planar Graphs:
<img src="https://github.com/jumproper/force-directed-graphs/blob/master/demos/planar.JPG" alt="drawing" width="400"/>

### Sparse Random:
<img src="https://github.com/jumproper/force-directed-graphs/blob/master/demos/random_sparse.JPG" alt="drawing" width="400"/>

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
