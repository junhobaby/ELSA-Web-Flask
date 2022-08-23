import json
import googlemaps
from os import environ
from flask import Blueprint, render_template
from flask.globals import request
from models import db
from api.positionstack import PositionStack
from services.database import Database

owners_bp = Blueprint('owners',
                      __name__,
                      template_folder='templates',
                      url_prefix='/owners')


@owners_bp.route('/')
def show_owners():
    # list all customers from `src_owners` table
    #SrcOwners, SRCSchools join them by owner Id, write sql table
    #Join them by owner ID, records, raw_address_id is null,
    query = """
    SELECT
        o.*
    FROM src_owners o
    INNER JOIN src_schools s 
        ON s.owner_id = o.id
    WHERE s.raw_address_id is NULL
    """

    result_set = db.engine.execute(query).fetchall()
    return render_template('pages/owners.html',
                           customers=[dict(i) for i in result_set])


@owners_bp.route('/<owner_id>/')
def show_owner(owner_id):
    # list customer from `src_owners` table
    query = f"""
    SELECT
        o.id as owner_id,
        o.name as owner_name,
        o.email as owner_email,
        o.phone as owner_phone,
        s.id as school_id,
        s.alias_name as school_name,
        s.billing_address as school_address
    FROM
        src_owners o
    inner join src_schools s on o.id = s.owner_id
    where o.id = {owner_id}
    """
    result = db.engine.execute(query).fetchall()
    owner_details = dict(result[0])
    school_details = [{
        "school_id": school['school_id'],
        "school_name": school['school_name'],
        "address": school['school_address']} for school in result]

    owner_id = owner_details['owner_id']
    owner_name = owner_details['owner_name']
    owner_email = owner_details['owner_email']
    owner_phone = owner_details['owner_phone']

    return render_template('pages/owner.html',
                           owner_id=owner_id,
                           owner_name=owner_name,
                           owner_email=owner_email,
                           owner_phone=owner_phone,
                           school_details=school_details)


@owners_bp.route('/geocode/', methods=['POST'])
def geocode_school():

    # initiate classes
    gmaps = googlemaps.Client(key=environ.get('GOOGLE_MAPS_API_KEY'))
    pg_db = Database(db.engine)

    # get data from JS
    data = request.json
    try:
        address_query = data['query']

        # geocode using Google Maps
        result = gmaps.geocode(address_query)[0]
        print(result)
        raw_address_pk = pg_db.insert_raw_json('raw_address', json.dumps(result))
        payload = dict(address_pk=raw_address_pk, data=result)
        return payload

    except KeyError as e:
        return dict(data=[])


@owners_bp.route('/<owner_id>/schools/', methods=['POST'])
def standardise_school(owner_id):
    data = request.json
    # payload: {"owner_id": 1, schools: [{"school_id": 1, "raw_address_id": 1}, {"school_id": 2, "raw_address_id": 2}]}
    owner_id = data['owner_id']
    schools = data['schools']

    with db.engine.connect() as conn:
        for school in schools:
            query = f"""
                UPDATE src_schools
                SET raw_address_id = {school['raw_address_id']}
                WHERE owner_id = {owner_id} and id = {school['school_id']}
            """
            conn.execute(query)

    return dict(message='success')
