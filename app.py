import numpy as np
import datetime as dt
import pickle
import os
from config import heart_class_fields
from flask import Flask, render_template,request

# https://www.geeksforgeeks.org/how-to-use-web-forms-in-a-flask-application/
# Initalize Flask
app = Flask(__name__)
app.config["DEBUG"] = True

accordian_state = { "heart" : "false",
                    "fetal" : "false"
                  }
modelx_values = { "age": "70", 
                  "sex": "1", 
                  "cp": "2", 
                  "trestbps": "140",
                  "chol": "234",
                  "fbs": "0",
                  "restecg": "0",
                  "thalach": "172",
                  "exang": "1",
                  "oldpeak": "1",
                  "slope": "1",
                  "ca": "1",
                  "thal": "3"
                   }

# modely_values = { "age": "70", 
#                   "sex": "1", 
#                   "cp": "2", 
#                   "trestbps": "140",
#                   "chol": "234",
#                   "fbs": "0",
#                   "restecg": "0",
#                   "thalach": "172",
#                   "exang": "1",
#                   "oldpeak": "1",
#                   "slope": "1",
#                   "ca": "1",
#                   "thal": "3"
#                    }

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
lrcl_model_url = os.path.join(SITE_ROOT, "static/models", "lrcl.pkl")
kncl_model_url = os.path.join(SITE_ROOT, "static/models", "kncl.pkl")
svcl_model_url = os.path.join(SITE_ROOT, "static/models", "svmcl.pkl")
dtcl_model_url = os.path.join(SITE_ROOT, "static/models", "dtcl.pkl")
rfcl_model_url = os.path.join(SITE_ROOT, "static/models", "rfcl.pkl")

lgmodel = pickle.load(open(lrcl_model_url, 'rb'))
knmodel = pickle.load(open(kncl_model_url, 'rb'))
svmodel = pickle.load(open(svcl_model_url, 'rb'))
dtmodel = pickle.load(open(dtcl_model_url,'rb'))
rfmodel = pickle.load(open(rfcl_model_url, 'rb'))

def switch_model(hd_model):
    if hd_model == "0":
        return lgmodel
    elif hd_model == "1":
        return knmodel
    elif hd_model == "2":
        return svmodel
    elif hd_model == "3 ":
        return dtmodel
    elif hd_model == "4":
        return rfmodel
    
# prediction function
def ValuePredictor(model_id, max_predictor, to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, max_predictor)    
    result = switch_model(model_id).predict(to_predict)
    return result[0]

@app.route('/') # Homepage
def home():
    return render_template('index.html', modelx_values = modelx_values)

@app.route('/heart', methods = ['POST'])
def result():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()

        #get screen values and store it local variable for reload
        for key,val in to_predict_list.items():
            if key in modelx_values.keys():
                modelx_values[key] = val
        model_id = to_predict_list['Model_x']
        to_predict_list = list(modelx_values.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(model_id, 13, to_predict_list)        
        if int(result)== 1:
            xprediction = "Probable Heart Disease"
        else:
            xprediction = "Heart Disease Improbable"
        return render_template("index.html", modelx_values = modelx_values, prediction = xprediction, xresult = result)

# @app.route('/fetal', methods = ['POST'])
# def result():
#     if request.method == 'POST':
#         to_predict_list = request.form.to_dict()

#         #get screen values and store it local variable for reload
#         for key,val in to_predict_list.items():
#             if key in modelx_values.keys():
#                 modelx_values[key] = val
#         model_id = to_predict_list['Model_y']
#         to_predict_list = list(modely_values.values())
#         to_predict_list = list(map(int, to_predict_list))
#         result = ValuePredictor(model_id, 13, to_predict_list)        
#         if int(result)== 1:
#             xprediction = "Probable Heart Disease"
#         else:
#             xprediction = "Heart Disease Improbable"
#         return render_template("index.html", modelx_values = modelx_values, prediction = xprediction, xresult = result)
    
if __name__ == "__main__":
    app.run(debug=True)