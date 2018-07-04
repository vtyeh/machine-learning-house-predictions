from flask_wtf import FlaskForm
from wtforms import FloatField,SelectField
from wtforms.validators import DataRequired,optional,NumberRange

state_choices = [('CA', 'CA')
                 ]
loan_purpose_choices = [('P', 'Purchase'),
                        ('R', 'No Cash-out Refinance'),
                        ('C', 'Cash-out Refinance'),
                        ('U', 'Refinance Not Specified')
                        ]

property_type_choices = [('SF', 'Single Family'),
                         ('PU', 'Planned Urban Development'),
                         ('CO', 'Condo'),
                         ('MH', 'Manufactured Housing'),
                         ('CP', 'Co-Op')
                         ]
occupancies_type_choices = [('P', 'Primary Home'),
                            ('S', 'Secondary Home'),
                            ('I', 'Investment Home')
                            ]

class MorgageInputForm(FlaskForm):
    loan_amount = FloatField('Originated Amount ($)', validators=[DataRequired()])
    buyer_credit = FloatField('Buyer\'s credit score (Valid from 500 to 850)', validators=[DataRequired()])
    cobuyer_credit = FloatField('Cobuyer\'s credit score', validators=[optional(),NumberRange(500.0,850.0,"Check credit score")])
    loan_to_value = FloatField('Originated Loan to Value ratio (%)',validators=[DataRequired()])
    debt_to_income = FloatField('Debt to Income Ratio (%)', validators=[DataRequired()])
    loan_state = SelectField('State', choices=state_choices)
    loan_purpose = SelectField('Loan Purpose',
                               choices=loan_purpose_choices)
    property_type = SelectField('Property Type',
                                choices=property_type_choices)
    occupancy_type = SelectField('Occupancy Type',
                                 choices=occupancies_type_choices)
