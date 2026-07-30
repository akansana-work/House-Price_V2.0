import pickle
from flask import Flask,request,app,jsonify,url_for,render_template
import numpy as np
import pandas as pd

app = Flask(__name__)
model = pickle.load(open('housepred.pkl','rb'))
scaler = pickle.load(open('scaler.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    a_data = (np.array(list(data.values())).reshape(1,-1))
    new_data = scaler.transform(a_data)
    output = model.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict',methods=['POST'])
def predict():
    # Retrieve the user inputs
    rm_input = request.form.get('RM')
    age_input = request.form.get('Age')
    dis_input = request.form.get('DIS')
    tax_input = request.form.get('TAX')
    
    # 1. Backend Validation: Make sure the user actually selected options
    if not rm_input or not age_input or not dis_input or not tax_input:
        return render_template("home.html", prediction_text="Error: Please select an option for all 4 fields before running the AI.")
        
    rm = float(rm_input)
    age = float(age_input)
    dis = float(dis_input)
    tax = float(tax_input)
    
    # 2. Hardcode the remaining 9 features (using Boston dataset averages)
    # This simulates the backend fetching complex neighborhood data from a DB or API
    crim = 3.613
    zn = 11.36
    indus = 11.13
    chas = 0.0
    nox = 0.554
    rad = 9.54
    ptratio = 18.45
    b = 356.67
    lstat = 12.65
    
    # 3. Combine them in the exact order the ML model expects (13 features total)
    data = [crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat]
    
    final_input = scaler.transform(np.array(data).reshape(1,-1))
    print("Final Model Input Array:", final_input)
    
    output = model.predict(final_input)[0]
    
    # The Boston dataset predicts prices in $1000s (from 1978). 
    # Let's format it nicely as a dollar amount.
    formatted_price = "${:,.2f}".format(output * 1000)
    
    return render_template("home.html", prediction_text=f"Estimated AI Valuation: {formatted_price}")


if __name__ =="__main__":
    app.run(debug=True)