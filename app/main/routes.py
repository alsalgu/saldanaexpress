from flask import render_template, current_app, redirect, flash, url_for
from flask import request
from app import db
from app.main import bp
from flask_login import current_user, login_user, logout_user, login_required
from app.database.models import User, Client, Quickpay
from werkzeug.urls import url_parse

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/dashboard')
def dashboard_re():
    return redirect(url_for('main.dashboard'))

@bp.route('/dashboard/main')
@login_required
def dashboard():
    return render_template('dashboard/dash-main.html')

@bp.route('/dashboard/clients', methods=['GET', 'POST'])
@login_required
def clients():
    if request.method == "POST":
        formatted_address = request.form['street_number'] + " " + request.form['route']
        newClient = Client(client_name = request.form['client-name'],
                            email = request.form['client-email'],
                            phone = request.form['phone-number'],
                            fax = request.form['fax-number'],
                            address = formatted_address,
                            zipcode = request.form['postal_code'],
                            state = request.form['administrative_area_level_1'],
                            country = request.form['country'],
                            user_id = current_user.id,
                            mc_number = request.form['mc-number'],
                            dot_number = request.form['dot-number'],
                            quickpay = request.form['quickpayCheck'])
        db.session.add(newClient)
        flash('Added New Client')
        db.session.commit()
        return render_template('dashboard/dash-clients.html')
    else:
        return render_template('dashboard/dash-clients.html')

@bp.route('/dashboard/clients/<int:client_id>', methods=['GET', 'POST'])
@login_required
def singleClient(client_id):
    current_client = Client.query.filter_by(id=client_id, user_id=current_user.id).first()
    current_client_quickpay = Quickpay.query.filter_by(client_id = client_id).first()
    if current_client_quickpay is None and request.method == "POST":
        newQuickpay = Quickpay(pay_percentage = request.form['qp-percentage'],
                                send_to = request.form['send-to'],
                                send_to_type = request.form['send-to-type'],
                                client_id = current_client.id)
        db.session.add(newQuickpay)
        flash('New Quickpay Info')
        db.session.commit()
        return render_template('dashboard/dash-client-view.html', current_client=current_client, current_client_quickpay = current_client_quickpay)
    elif request.method == "POST":
        if request.form['qp-percentage']:
            current_client_quickpay.pay_percentage = request.form['qp-percentage']
        if request.form['send-to']:
            current_client_quickpay.send_to = request.form['send-to']
        if request.form['send-to-type']:
            current_client_quickpay.send_to_type = request.form['send-to-type']
        db.session.add(current_client_quickpay)
        flash('Quickpay Updated')
        db.session.commit()
    else:
        return render_template('dashboard/dash-client-view.html', current_client=current_client, current_client_quickpay = current_client_quickpay)