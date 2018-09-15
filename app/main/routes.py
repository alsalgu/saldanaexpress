from flask import render_template, current_app, redirect, flash, url_for
from flask import request
from app import db
from app.main import bp
from flask_login import current_user, login_user, logout_user, login_required
from app.database.models import User, Client, Quickpay
from werkzeug.urls import url_parse
from app.main.forms import EditClientForm, EditQuickpayForm, DeleteClient

@bp.route('/')
def index():
    return render_template('main/index.html')

@bp.route('/about')
def about():
    return render_template('main/about.html')

@bp.route('/careers')
def careers():
    return render_template('main/careers.html')

@bp.route('/contact-us')
def contact():
    return render_template('main/contact.html')

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
                            city = request.form['locality'],
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
    current_client_quickpay = Quickpay.query.filter_by(client_id=client_id).first()
    form = EditClientForm()
    form2 = EditQuickpayForm()
    form3 = DeleteClient()
    if current_client_quickpay is None and form2.validate_on_submit():
        newQuickpay = Quickpay(pay_percentage = form2.pay_percentage.data,
                                send_to = form2.send_to.data,
                                send_to_type = form2.send_to_type.data,
                                client_id = current_client.id)
        db.session.add(newQuickpay)
        db.session.commit()
        flash('New Quickpay Info')
        return redirect(url_for('main.singleClient', client_id=current_client.id))
    if form2.submitQuickpay.data and form2.validate_on_submit():
        if form2.pay_percentage.data:
            current_client_quickpay.pay_percentage = form2.pay_percentage.data
        if form2.send_to.data:
            current_client_quickpay.send_to = form2.send_to.data
        if form2.send_to_type:
            current_client_quickpay.send_to_type = form2.send_to_type.data
        db.session.add(current_client_quickpay)
        db.session.commit()
        flash('Quickpay Updated!')
        return redirect(url_for('main.singleClient', client_id=current_client.id))
    if form3.submitDelete.data and form3.validate_on_submit():
        db.session.delete(current_client)
        db.session.commit()
        flash('Client Deleted!')
        return redirect(url_for('main.clients'))   
    if form.submitClient.data and form.validate_on_submit():
        if form.client_name.data:
            current_client.client_name = form.client_name.data
        if form.email.data:
            current_client.email = form.email.data
        if form.phone.data:
            current_client.phone = form.phone.data
        if form.fax.data:
            current_client.fax = form.fax.data
        if form.address.data:
            current_client.address = form.address.data
        if form.city.data:
            current_client.city = form.city.data
        if form.state.data:
            current_client.state = form.state.data
        if form.country.data:
            current_client.country = form.country.data
        if form.quickpay.data:
            current_client.quickpay = form.quickpay.data
        if form.mc_number.data:
            current_client.mc_number = form.mc_number.data
        if form.dot_number.data:
            current_client.dot_number = form.dot_number.data
        db.session.add(current_client)
        db.session.commit()
        flash('Client Updated!')
        return redirect(url_for('main.singleClient', client_id=current_client.id))  
    return render_template('dashboard/dash-client-view.html', current_client=current_client, current_client_quickpay = current_client_quickpay, form=form, form2=form2, form3=form3)

@bp.route('/dashboard/employees')
@login_required
def employees():
    return render_template('dashboard/employees/employees.html')

@bp.route('/dashboard/expenses')
@login_required
def expenses():
    return render_template('dashboard/expenses/expenses.html')

@bp.route('/dashboard/invoices')
@login_required
def invoices():
    return render_template('dashboard/invoices/invoices.html')

@bp.route('/dashboard/company')
@login_required
def my_company():
    return render_template('dashboard/my-company/company.html')

@bp.route('/dashboard/trips')
@login_required
def trips():
    return render_template('dashboard/trips/trips.html')

@bp.route('/dashboard/trucks')
@login_required
def trucks():
    return render_template('dashboard/trucks/trucks.html')