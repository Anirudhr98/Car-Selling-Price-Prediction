from flask import Flask , render_template,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
model = pickle.load(open('rfr_model.pkl','rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods = ['POST'])
def predict():
    Fuel_Type_Diesel = 0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Showroom_Price = float(request.form['Showroom_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven=np.log(Kms_Driven)
        Previous_Car_Owners = int(request.form['Previous_Car_Owners'])
        Fuel_Type = (request.form['Fuel_Type'])
        if(Fuel_Type == 'Petrol'):
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1

        Year = 2020 - Year
        
        Individual_Or_Dealer = (request.form['Individual_Or_Dealer'])
        if (Individual_Or_Dealer == 'Individual'):
            Seller_Type = 0
        else :
            Seller_Type = 1
        Transmission_Type = (request.form['Transmission_Type'])
        if (Transmission_Type == 'Manual'):
            Transmission_Type = 1
        else :
            Transmission_Type = 0
        prediction =  model.predict([[Showroom_Price,Kms_Driven,Previous_Car_Owners,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type,Transmission_Type]])
        output = round(prediction[0],2)

        if output<0:
            return render_template('index.html',prediction_text="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} lakhs".format(output))
    else:
        return render_template('index.html', prediction_text = "Sorry there is an error")
                
if __name__== "__main__":
    app.run(debug = True)
    

