from flask import render_template, request, flash, redirect, Flask
from forms import HouseForms, MortgageInputForm
import pickle
import dill
import pandas as pd
import os.path
# from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# csrf = CSRFProtect()

current_path = os.path.split(os.path.abspath(__file__))[0]
with open(os.path.join(current_path,"models/clf_model_new.pkl"), "rb")as f:
    model = pickle.load(f)

def default_none(input_data):
    if input_data != None:
        return input_data
    else:
        return None

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/economic")
def economicPage():
    return render_template("economic.html")

@app.route("/contacts")
def contactPage():
    return render_template("contacts.html")

@app.route("/priceForm")
def root():
    global model
    form = HouseForms(csrf_enabled=False)  
    return render_template("index1.html",
    title = "House Price Prediction",
    form = form, prediction = "Awaiting You")

@app.route("/calculate", methods = ["POST"])
def index():
    global model
    form = HouseForms(csrf_enabled=False)

    overallquality = []
    garagecars = []
    area = []
    fullbaths = []
    yearbuilt = []
    bedrooms = []
    buildingtype = ""
    centralair = ""
    housestyle = ""

    overallquality.append(form.overallQuality.data)
    garagecars.append(form.garage.data)
    area.append(form.area.data)
    fullbaths.append(form.bathrooms.data)
    yearbuilt.append(form.yearBuilt.data)
    bedrooms.append(form.bedrooms.data)
    buildingtype = form.buildingType.data
    centralair = form.centralAir.data
    housestyle = form.houseStyle.data


    # print(model)
    # test_case = pd.DataFrame.from_dict({
    #     "Overall Quality": [form.overallQuality.data],
    #     "Squarefeet": [form.area.data],
    #     "Bedrooms":[form.bedrooms.data],
    #     "Full Baths":[form.bathrooms.data],
    #     "Garage Cars":[form.garage.data],
    #     "Year Built":[form.yearBuilt.data],
    # })
    # print(test_case)
    test_case = pd.DataFrame()

    test_case["Overall Quality"] = overallquality
    test_case["Squarefeet"] = area
    test_case["Bedrooms"] = bedrooms
    test_case["Full Baths"] = fullbaths
    test_case["Garage Cars"] = garagecars
    test_case["Year Built"] = yearbuilt

    dummylist = []
    dummylist = 15*[0]
    dummy_df = pd.DataFrame([dummylist])
    test_case[["BldgType_1Fam",'BldgType_2fmCon', 'BldgType_Duplex', 'BldgType_Twnhs',
    'BldgType_TwnhsE', 'CentralAir_N', 'CentralAir_Y', 'HouseStyle_1.5Fin',
    'HouseStyle_1.5Unf', 'HouseStyle_1Story', 'HouseStyle_2.5Fin',
    'HouseStyle_2.5Unf', 'HouseStyle_2Story', 'HouseStyle_SFoyer',
    'HouseStyle_SLvl']]=dummy_df
    test_case.loc[0, buildingtype] = 1
    test_case.loc[0, centralair] = 1
    test_case.loc[0, housestyle] = 1
    print(test_case)
    
    prediction = model.predict(test_case)
    print(prediction)
    prediction = round(prediction[0],2)
    prediction = "${:,.2f}".format(prediction)
    print(prediction)

    return render_template("index1.html",
    title = "House Price Prediction",
    form = form,
    prediction = prediction)

with open(os.path.join(current_path, "models/sgd-model.dill"), "rb") as g:
    sgd_model = dill.load(g)

@app.route('/mortgageForm', methods=['GET', 'POST'])
def mortgageForm():
    global sgd_model
    form = MortgageInputForm(csrf_enabled=False)
    return render_template("mortgage.html",
                           title='Mortgage Risk Assessment',
                           form=form)
                           

@app.route('/mortgageCalc', methods=['GET', 'POST'])
def mortgageCalc():
    global sgd_model
    form = MortgageInputForm(csrf_enabled=False)

    test_case = pd.DataFrame.from_dict({
        'ORIG_AMT': [float(form.loan_amount.data)],
        'CSCORE_B': [float(form.buyer_credit.data)],
        'CSCORE_C': [default_none(form.cobuyer_credit.data)],
        'OCLTV': [float(form.loan_to_value.data)],
        'DTI': [float(form.debt_to_income.data)],
        'STATE': [form.loan_state.data],
        'PURPOSE': [form.loan_purpose.data],
        'PROP_TYP': [form.property_type.data],
        'OCC_STAT': [form.occupancy_type.data]
    }
    )

    prediction = sgd_model.predict(test_case)[0]
    print(prediction)

    if prediction == 0:
        result = 'OK'
        status = 'Success'
    elif prediction == 1:
        result = 'Caution!'
        status = 'Failure'
    else:
        result = 'Check Input'
        status = 'Alert'

    return render_template("mortgage.html",
                           title='Mortgage Risk Assessment',
                           form=form,
                           result=result,
                           prediction=prediction,
                           status=status)


if __name__ == ("__main__"):
    app.run(debug=True)