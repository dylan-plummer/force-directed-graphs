import configparser
import os
from flask import Flask, render_template, request, flash, redirect, url_for
from GraphGen import GenerateGraph, GraphToJSON, FindCliques, ExtractCliques
import mysql.connector
import json


# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Choices for types of graphs generated
choices = {'Random':'k', 'Tree':'t', 'Planar':'p', 'Component':'c'}

# Set up application server.
app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

# Create a function for fetching data from the database.
def sql_query(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result


def sql_execute(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

def sql_execute_file(sql):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor()
    fd = open(sql, 'r')
    sqlFile = fd.read()
    fd.close()
    sqlCommands = sqlFile.split(';')

    for command in sqlCommands:
        try:
            if command.strip() != '':
                cursor.execute(command)
        except IOError:
            print("Command skipped: ")
    db.close()


def process_form(form, graph_types):
    '''
    Generates a graph based on the user entered values
    '''
    try:
        num_verts = request.form['num-verts']
        edge_prob = request.form['edge-prob']
        max_weight = request.form['max-weight']
        graph_type = graph_types[request.form['graph-type']]
        if not 0.0 <= float(edge_prob) <= 1.0: # make sure edge_prob is a probability
            flash('Edge probability must be between 0 and 1')
        else:
            print("gen")
            G = GenerateGraph(int(num_verts), float(edge_prob), int(max_weight), graph_type)
            GraphToJSON(G)
            #Store Graph in SQL
            print("Resetting DB")
            reset_db()
            for n in G['nodes']:
                for l in G['links']:
                    d = 0
                    if l['target'] == n['name'] or l['source'] == n['name']:
                        d += 1
                print("Adding Node to SQL: ", n,d)
                insert_vert(int(n['name'])+1,int(n['group']),int(d))
            for l in G['links']:
                print("Adding Link to SQL: ",int(l['source']), int(l['target']), int(l['value']))
                insert_edge(int(l['source'])+1, int(l['target'])+1, int(l['value']))
            C = FindCliques()
            for c in C:
                print("Adding Clique to SLQ: ", str(c))
                insert_clique(len(c),str(c))

    except TypeError as e1:
        print(e1)
        flash('Number of vertices must be an integer')
    except ValueError as e2:
        print(e2)
        flash('Number of vertices must not be empty')
    except KeyError as e3:
        print(e3)
        print('Could not find the resource you selected')


def startup_form(request_form):
    '''
    Set form values to previously entered values
    If none, set to default values
    '''
    form = {}
    try:
        num_verts = request_form['num-verts']
        form['num-verts'] = int(num_verts)
    except:
        form['num-verts'] = 10
    try:
        edge_prob = request_form['edge-prob']
        form['edge-prob'] = float(edge_prob)
    except:
        form['edge-prob'] = 0.1
    try:
        max_weight = request_form['max-weight']
        form['max_weight'] = int(max_weight)
    except:
        form['max_weight'] = 10
    try:
        graph_type = request_form['graph-type']
        form['graph-type'] = graph_type
    except:
        form['graph-type'] = 'Random'
    try:
        extract_cliques = request_form['cliques']
        form['cliques'] = int(extract_cliques)
    except:
        form['cliques'] = 0
    print('form', form)
    return form


@app.route('/', methods=['POST', 'GET'])
def template_response_with_data():
    '''
    Refreshes and renders the page when opening the site and updating the graph
    Extracts cliques if the user checked the box
    '''
    form = startup_form(request.form)
    selected = form['graph-type']
    state = {'choice': selected}
    if form['cliques'] == 1:
        extract_cliques()
    else:
        process_form(form, choices)
    metrics = get_metrics()
    return render_template('index.html', choices=list(choices.keys()), state=state, metrics=metrics)

def reset_db():
    '''
    Resets the database
    '''
    sql_execute_file('setup_no_usr.sql')

def insert_vert(name, color, degree):
    '''
    Insert vertex of specific color and degree into the database.
    '''
    sql = 'INSERT INTO VERT(ID, COLOR, DEGREE) VALUES (' + str(int(name)) + ', ' + str(color) + ', ' + str(degree) + ')'
    sql_execute(sql)

def insert_edge(sourceID, targetID, weight):
    '''
    Insert edge of specific source and target id as well as weight
    into the database.
    '''
    sql = 'INSERT INTO EDGE(SOURCE, TARGET, WEIGHT) VALUES (' + str(sourceID) + ', ' + str(targetID) + ', ' + str(weight) + ')'
    sql_execute(sql)

def insert_clique(size, members):
    '''
    Insert clique with size as weight and members, members should be
    a LONGTEXT complient JSON file.
    '''
    sql = 'INSERT INTO CLIQUE(ID, AMMO, MEMBERS) VALUES (0, ' + str(size) + ', \'' + str(members) + '\')'
    sql_execute(sql)

def get_lowest_degree():
    '''
    Get the lowest degree from the database.
    '''
    sql = 'SELECT * FROM VERT ORDER BY DEGREE LIMIT 1'
    return sql_query(sql)

def get_highest_degree():
    '''
    Get the highest degree from the database.
    '''
    sql = 'SELECT * FROM VERT ORDER BY DEGREE DESC LIMIT 1'
    return sql_query(sql)

def get_avg_degree():
    '''
    Get the average of the degrees of the VERT database table.
    '''
    sql = 'SELECT AVG(DEGREE) FROM VERT'
    return sql_query(sql)

def get_lowest_weight():
    '''
    Get the edge with the lowest weight from the database.
    '''
    sql = 'SELECT * FROM EDGE ORDER BY WEIGHT LIMIT 1'
    return sql_query(sql)

def get_highest_weight():
    '''
    Get the edge with the highest weight from the database.
    '''
    sql = 'SELECT * FROM EDGE ORDER BY WEIGHT DESC LIMIT 1'
    return sql_query(sql)

def get_avg_weight():
    '''
    Get the average of weights from the EDGE table. 
    '''
    sql = 'SELECT AVG(WEIGHT) FROM EDGE'
    return sql_query(sql)

def get_largest_clique():
    '''
    Get the largest clique from database.
    '''
    sql = 'SELECT * FROM CLIQUE ORDER BY AMMO LIMIT 1'
    return sql_query(sql)

def get_clique_amt():
    '''
    Enumerate the cliques on the database.
    '''
    sql = 'SELECT COUNT(*) FROM CLIQUE'
    return sql_query(sql)

def get_clique_by_id(cliqueID):
    '''
    Get a clique by cliqueID from the database.
    '''
    sql = 'SELECT * FROM CLIQUE WHERE ID=' + str(cliqueID)

def get_vert_by_id(nodeID):
    '''
    Get vert by nodeID from the database.
    '''
    sql = 'SELECT * FROM VERT WHERE ID=' + str(nodeID)


def extract_cliques():
    '''
    Take the current graph.json file and recolor the nodes to show Cliques
    The graph display is updated after this function is called above
    '''
    ExtractCliques(FindCliques())

def get_metrics():
    '''
    Return a list of metric titles and values to be displayed below the graph.
    The elements of the list returned should be the exact string to be displayed.
    '''
    # ToDo:
    # Get metrics from sql
    try:
        minDeg = get_lowest_degree()[0][2]
        maxDeg = get_highest_degree()[0][2]
        avgDeg = get_avg_degree()[0]
        minWgt = get_lowest_weight()[0][2]
        maxWgt = get_highest_weight()[0][2]
        avgWgt = get_avg_weight()[0]
        lrgClq = get_largest_clique()
        numClq = get_clique_amt()
    except IndexError:
        minDeg = "null, pls refresh"
        maxDeg = "null, pls refresh"
        avgDeg = "null, pls refresh"
        minWgt = "null, pls refresh"
        maxWgt = "null, pls refresh"
        avgWgt = "null, pls refresh"
        lrgClq = "null, pls refresh"
        numClq = "null, pls refresh"

    metrics = ['Min Degree: '+ str(minDeg), 'Max Degree: '+ str(maxDeg), 'Average Degree: '+ str(avgDeg),
               'Min Weight: '+ str(minWgt), 'Max Weight: '+ str(maxWgt), 'Average Weight: '+ str(avgWgt),
               'Number of Cliques: '+ str(numClq), 'Largest Clique: '+ str(lrgClq)]
    return metrics

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
    app.secret_key = 'shhh it\'s a secret'
    app.run(**config['app'])
