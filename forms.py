from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired,optional,NumberRange

building_type = [("BldgType_1Fam","Single Family Detached"),("BldgType_2Fam", "Two-Family Conversion"), ("BldgType_Duplx", "Duplex"), ("BldgType_TwnhsE", "Townhouse End Unit"), ("BldgType_Twnhs", "Townhouse Inside Unit")]
house_style = [("HouseStyle_1Story","One Story"),("HouseStyle_1.5Fin","1.5 stories: 2nd level finished"),("HouseStyle_1.5Unf","1.5 stories: 2nd level unfinished"),("HouseStyle_2Story","Two Stories"),("HouseStyle_2.5Fin","2.5 Stories: 2nd level finished"),("HouseStyle_2.5Unf","2.5 Stories: 2nd level unfinished"),("HouseStyle_SFoyer","Split Foyer"),("HouseStyle_SLvl","Split Level")]
central_air = [("CentralAir_Y","Yes"),("CentralAir_N","No")]

overall_quality_choice = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)]
bedrooms_choice = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
bathrooms_choice = [(1,1),(2,2),(3,3)]
# garage_choice = [(0,"None"),(1,"One Car"),(2,"Two Cars"),(3,"Three Cars"),(4,"Four Cars")]
garage_choice = [(0,0),(1,1),(2,2),(3,3),(4,4)]

class HouseForms(FlaskForm):
    buildingType = SelectField('Type of House', choices = building_type)
    houseStyle = SelectField('Style of House', choices = house_style)
    centralAir = SelectField('Central air condition', choices = central_air)
    overallQuality = SelectField('Overall Quality of the House (1 = Poor, 10 = Excellent)', choices=overall_quality_choice)
    bedrooms  = SelectField('Number of Bedrooms', choices=bedrooms_choice)
    bathrooms= SelectField('Number of Bathrooms', choices=bathrooms_choice)
    garage= SelectField('Garage Size', choices=garage_choice)
    area = FloatField("Squarefeet", validators = [DataRequired()])
    yearBuilt = FloatField("Year Built", validators = [DataRequired()])

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

class MortgageInputForm(FlaskForm):
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
