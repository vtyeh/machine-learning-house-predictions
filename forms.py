from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField
from wtforms.validators import DataRequired,optional

building_type = [("BldgType_1Fam","Single Family Detached"),("BldgType_2Fam", "Two-Family Conversion"), ("BldgType_Duplx", "Duplex"), ("BldgType_TwnhsE", "Townhouse End Unit"), ("BldgType_Twnhs", "Townhouse Inside Unit")]
house_style = [("HouseStyle_1Story","One Story"),("HouseStyle_1.5Fin","1.5 stories: 2nd level finished"),("HouseStyle_1.5Unf","1.5 stories: 2nd level unfinished"),("HouseStyle_2Story","Two Stories"),("HouseStyle_2.5Fin","2.5 Stories: 2nd level finished"),("HouseStyle_2.5Unf","2.5 Stories: 2nd level unfinished"),("HouseStyle_SFoyer","Split Foyer"),("HouseStyle_SLvl","Split Level")]
central_air = [("CentralAir_Y","Yes"),("CentralAir_N","No")]

overall_quality_choice = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)]
bedrooms_choice = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8)]
bathrooms_choice = [(1,1),(2,2),(3,3)]
garage_choice = [(0,0),(1,1),(2,2),(3,3),(4,4)]

class HouseForms(FlaskForm):
    buildingType = SelectField('Type of House', choices = building_type)
    houseStyle = SelectField('Style of House', choices = house_style)
    centralAir = SelectField('Central air condition', choices = central_air)
    overallQuality = SelectField('Overall Quality of the House (1 = Poor, 10 = Excellent)', choices=overall_quality_choice)
    bedrooms  = SelectField('Number of Bedrooms', choices=bedrooms_choice)
    bathrooms= SelectField('Number of Bathrooms', choices=bathrooms_choice)
    garage= SelectField('Number of Garage Cars', choices=garage_choice)
    area = FloatField("Squarefeet", validators = [DataRequired()])
    yearBuilt = FloatField("Year Built", validators = [DataRequired()])