import configparser
from flask import Flask, render_template, request, flash, redirect, url_for
from GraphGen import GenerateGraph, GraphToJSON, FindCliques, ExtractCliques
import mysql.connector

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
            GraphToJSON(GenerateGraph(int(num_verts), float(edge_prob), int(max_weight), graph_type))
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


def extract_cliques():
    '''
    Take the current graph.json file and recolor the nodes to show Cliques
    The graph display is updated after this function is called above
    '''
    print('Cliques!')
    ExtractCliques(FindCliques())

def get_metrics():
    '''
    Return a list of metric titles and values to be displayed below the graph.
    The list returned should be the exact string to be displayed.
    '''
    metrics = ['Min Degree: x', 'Max Degree: y', 'Etc'] # Example list
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
    app.run(host='127.3.4.1', port=3000, debug=True)
