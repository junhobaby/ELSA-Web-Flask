from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

# GLOBAL VARIABLES
DB_USER = 'postgresuser'
DB_PASSWORD = 'password'
DB_HOST = 'localhost'
DB_NAME = 'postgres'
DB_PORT = 5432
DB_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # removes warning of significant overhead for Flask SQLAlchemy
app.debug = True
db = SQLAlchemy(app)


# Creating homepage and link it to index.html
@app.route("/")
def home():
    # render the index.html file from the `templates` table
    return render_template('html/index.html')


# Create about page
@app.route("/about")
def about():
    return "<p>This is about!</p>"


# Dummy testing for dynamic for <profile uid>
@app.route("/profile/<profile_uid>")
def greeting(profile_uid):
    return f"<p>Profile {profile_uid}</p>"


# dummy test to return {"message":"hello"} dictionary
@app.route("/api")
def get_api():
    return {"message": "hello"}


# connect to database
@app.route("/raw_data/<raw_data_id>/")
def get_raw_data(raw_data_id):
    """
    Raw Data ID: 1

    Expected output: {"__typename": "Registration", "active": "yes", "searchable": "holly bennett", "status":
    "Expected", "createdAt": "2022-05-10T02:24:09.074Z", "address": "", "lastUpdatedAt": "2022-05-10T02:24:09.074Z",
    "id": "f09cd746bf454971232f1622f21765f614b7af4c873b7be0367c267016fbe9d8", "phone": "0438874057", "preschoolId":
    "2021LarapintaPreschoolELSAP", "name": "Holly Bennett"}

    :return: JSON data
    """

    engine = db.engine
    with engine.connect() as conn:
        query = f"""
            SELECT
                raw_data
            FROM raw_educator_history
            WHERE "id" = {raw_data_id}
        """
        # executes SQL query and fetches all the rows from the query
        result = conn.execute(query).fetchall()
        return dict(result[0])
        # Confirm with Noel [0]?


# -------------
# NOEL

# API route to extract `raw_data` from the database
# endpoint: /raw_data/
@app.route("/raw_data/")
def get_list_data():
    engine = db.engine
    with engine.connect() as conn:
        query = f"""
                SELECT
                    raw_data
                FROM raw_educator_history
                WHERE raw_data ->> 'address' != ''
            """
        # executes SQL query and fetches all the rows from the query
        result = conn.execute(query).fetchall()
        # print(result)TO DO NOEL!!!!

        # data sample
        # {"result": [
        #   {raw_data_1},
        #   {raw_data_2},
        #   ...
        #   {{raw_data_100}}
        # ]}

        # empty list
        new_result = []
        for data in result:  # data is of `LegacyRow` type
            transformed_data = dict(data)  # transformed_data is of `dict` type
            new_result.append(transformed_data)  # adds transformed data in empty list

        # list comprehensions | reference: https://www.w3schools.com/python/python_lists_comprehension.asp
        # dict(result=[dict(i) for i in result])

        # expected data to be sent: {"data": [... new_result]}
        return dict(data=new_result)
        # {"data": new_result}
    # draw a diagram to why back and forth TO DO !!!!!!


@app.route("/view/")
def get_view_data():
    response = requests.get(f'http://127.0.0.1:5000/raw_data/')
    return render_template(
        'html/view.html',  # html file to serve
        # data 1 (raw_data) to be sent to html

        # Confirm whether this below is still useful?
        raw_data=response.json()['data'],

        # data 2 (datatable_data) to be sent to html
        datatable_data=[[i['raw_data']['active'], i['raw_data']['address'], i['raw_data']['name']] for i in
                        response.json()['data']]  # where is this data from ?

    )

#Reuben
# TODO: Create a function (get_updates)
@app.route("/updates_data/")  # create an api
def get_updates(): # to activate api portal, click on the localhost and paste the app.route directory
    # TODO: Create an engine
    engine = db.engine
    with engine.connect() as conn:
        # TODO: Write SQL to extract data from DB
        query = """
        SELECT
            recent_update,
            "Name",
            mobile_number
        FROM
            update_list_table
                """
        # result ->> [{LegacyRow}, {...}]
        result = conn.execute(query).fetchall()

        # TODO: Convert List to a Dictionary
        empty_bracket_list = []
        for data in result:
            converted_result = dict(data)
            empty_bracket_list.append(converted_result)


        # TODO: Return Converted List/Dictionary
        return dict(ELSA_Data=empty_bracket_list) #preparation


# Winnie Code
# extract data from the view
@app.route("/active_w_name_and_school/")
def get_user_data():
    engine = db.engine
    with engine.connect() as conn:
        query = f"""
                SELECT
                    "Name", school_id
                FROM active_w_name_and_school
            """
        # executes SQL query and fetches all the rows from the query
        result = conn.execute(query).fetchall()

        name_and_school_result = []
        for user in result:
            dict_user = dict(user)
            name_and_school_result.append(dict_user)

        return dict(user=name_and_school_result)


# Winnie
@app.route("/user/")
def get_view_user_data():
    response = requests.get(f'http://127.0.0.1:5000/active_w_name_and_school/')

    # TODO: create a list here:
    user_list = []
    for i in response.json()['user']:
        # i = {"name": "some_name", "preschool_id": "some_school_name"}
        print(i)
        # TODO: create a variable to store the `value` of name
        name_list = i['Name']
        # TODO: create a variable to store the `value` of preschool_id
        school_list = i['school_id']
        # TODO: append to an empty list the values name and school id
        user_list.append([name_list, school_list])

    return render_template(
        'html/user.html',
        database_data=user_list  # TODO: replace with a list
    )
# create html page
