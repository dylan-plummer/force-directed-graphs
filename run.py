import configparser
from flask import Flask, render_template, request
from GraphGen import GenerateGraph, GraphToJSON
from nocache import nocache
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


@app.route('/', methods=['GET', 'POST'])
@nocache
def template_response_with_data():
    print(request.form)
    template_data = {}
    num_verts = request.form['num-verts']
    try:
	    GraphToJSON(GenerateGraph(int(num_verts), 0.05, 10))
    except TypeError as e1:
	    print('Number of vertices must be an integer')
    except ValueError as e2:
	    print('Number of vertices must not be empty')
    return render_template('index.html', template_data=template_data)

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
    app.run(host='127.3.4.1', port=3000, debug=True)
