from flask import Blueprint, render_template
from models import db

customers_bp = Blueprint('customers_bp',
                         __name__,
                         template_folder='templates',
                         url_prefix='/customers')


@customers_bp.route('/')
def show_customers():
    # list all customers from `src_customers` table
    query = "SELECT * FROM src_customers"
    result_set = db.engine.execute(query).fetchall()
    return render_template('pages/customers.html',
                           customers=[dict(i) for i in result_set])


@customers_bp.route('/<customer_id>')
def show_customer(customer_id):
    # list customer from `src_customers` table
    query = f"SELECT * FROM src_customers WHERE id = {customer_id}"
    result = db.engine.execute(query).first()
    return render_template('pages/customer.html',
                           customer=dict(result))
