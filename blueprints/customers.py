from flask import Blueprint, render_template
from models import db

customers_bp = Blueprint('customers_bp',
                         __name__,
                         template_folder='templates',
                         url_prefix='/customers')


@customers_bp.route('/')
def show_owners():
    # list all customers from `src_owners` table
    query = "SELECT * FROM src_owners"
    result_set = db.engine.execute(query).fetchall()
    return render_template('pages/customers.html',
                           customers=[dict(i) for i in result_set])


@customers_bp.route('/<customer_id>')
def show_owner(customer_id):
    # list customer from `src_owners` table
    query = f"""
    SELECT
        o.id as owner_id,
        o.name as owner_name,
        o.email as owner_email,
        o.phone as owner_phone,
        s.alias_name as school_name,
        s.billing_address as school_address
    FROM
        src_owners o
    inner join src_schools s on o.id = s.owner_id
    where o.id = {customer_id}
    """
    result = db.engine.execute(query).fetchall()
    owner_details = dict(result[0])
    school_details = [{"school_name": school['school_name'], "address": school['school_address']} for school in result]

    owner_id = owner_details['owner_id']
    owner_name = owner_details['owner_name']
    owner_email = owner_details['owner_email']
    owner_phone = owner_details['owner_phone']

    return render_template('pages/customer.html',
                           owner_id=owner_id,
                           owner_name=owner_name,
                           owner_email=owner_email,
                           owner_phone=owner_phone,
                           school_details=school_details)
