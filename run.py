import configparser
from flask import Flask, render_template, request, flash
from GraphGen import GenerateGraph, GraphToJSON
import mysql.connector

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

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


@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    print(request.form)
    choices = {'Random':'k', 'Tree':'t'}
    selected = request.form['graph-type']
    state = {'choice': selected}
    template_data = {}
    process_form(request.form, choices)
    return render_template('index.html', choices=list(choices.keys()), state=state)

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
