from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.database.models import User

class EditClientForm(FlaskForm):
    client_name = StringField('Client Name')
    email = StringField('Email')
    phone = StringField('Phone')
    fax = StringField('Fax')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    country = StringField('Country')
    mc_number = StringField('MC#')
    dot_number = StringField('DOT#')
    quickpay = SelectField('Quickpay Available', choices=[('1', 'Yes'), ('0', 'No')])
    submitClient = SubmitField('Save Changes')

class EditQuickpayForm(FlaskForm):
    pay_percentage = StringField('Percentage')
    send_to = StringField('Send To')
    send_to_type = SelectField('Send-To Type', choices=[('Address', 'Address'), ('Email', 'Email'), ('Fax', 'Fax')])
    submitQuickpay = SubmitField('Save Changes')

class DeleteClient(FlaskForm):
    submitDelete = SubmitField('Confirm Deletion')