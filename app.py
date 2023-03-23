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
modely_values = {   "y_blval": "120",
                    "y_accl": "1",
                    "y_fetal_mov": "0",
                    "y_uc": "1",
                    "y_ldc": "1",
                    "y_sdc": "0",
                    "y_prodc": "0",
                    "y_abst": "17",
                    "y_mvst": "2.1",
                    "y_twabtrv": "0",
                    "y_mltv": "10",
                    "y_hist_wdth": "130",
                    "y_hist_min": "68",
                    "y_hist_max": "198",
                    "y_hist_npeak": "6",
                    "y_hist_zeros": "1",
                    "y_hist_mode": "141",
                    "y_hist_mean": "136",
                    "y_hist_median": "140",
                    "y_hist_var": "12",
                    "y_hist_tend": "0",
                    "y_hist_mean": "136",
                    "y_hist_median": "140",
                    "y_hist_var": "12",
                    "y_hist_tend": "0"
                }

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
lrcl_model_url = os.path.join(SITE_ROOT, "static/models", "lrcl.pkl")
kncl_model_url = os.path.join(SITE_ROOT, "static/models", "kncl.pkl")
svcl_model_url = os.path.join(SITE_ROOT, "static/models", "svmcl.pkl")
dtcl_model_url = os.path.join(SITE_ROOT, "static/models", "dtcl.pkl")
rfcl_model_url = os.path.join(SITE_ROOT, "static/models", "rfcl.pkl")

lrfh_cl_model_url = os.path.join(SITE_ROOT, "static/models", "lr_fh_cl.pkl")
knfh_cl_model_url = os.path.join(SITE_ROOT, "static/models", "kn_fh_cl.pkl")
svfh_cl_model_url = os.path.join(SITE_ROOT, "static/models", "svm_fh_cl.pkl")
dtfh_cl_model_url = os.path.join(SITE_ROOT, "static/models", "dtcl.pkl")
rffh_cl_model_url = os.path.join(SITE_ROOT, "static/models", "rfcl.pkl")

lgmodel = pickle.load(open(lrcl_model_url, 'rb'))
knmodel = pickle.load(open(kncl_model_url, 'rb'))
svmodel = pickle.load(open(svcl_model_url, 'rb'))
dtmodel = pickle.load(open(dtcl_model_url,'rb'))
rfmodel = pickle.load(open(rfcl_model_url, 'rb'))

lgclmodel = pickle.load(open(lrfh_cl_model_url, 'rb'))
knclmodel = pickle.load(open(knfh_cl_model_url, 'rb'))
svclmodel = pickle.load(open(svfh_cl_model_url, 'rb'))
dtclmodel = pickle.load(open(dtfh_cl_model_url,'rb'))
rfclmodel = pickle.load(open(rffh_cl_model_url, 'rb'))

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
        elif hd_model == "5":
            return lgclmodel
        elif hd_model == "6":
            return knclmodel
        elif hd_model == "7":
            return svclmodel
        elif hd_model == "8 ":
            return dtclmodel
        elif hd_model == "9":
            return rfclmodel
    
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

@app.route('/fetal', methods = ['POST'])
def result_y():
     if request.method == 'POST':
        to_predict_list = request.form.to_dict()
         #get screen values and store it local variable for reload
        for key,val in to_predict_list.items():
             if key in modely_values.keys():
                 modely_values[key] = val
        model_yid = to_predict_list['Model_y']
        to_predict_list = list(modely_values.values())
        to_predict_list = list(map(int, to_predict_list))
        result = ValuePredictor(model_yid, 21, to_predict_list)        
        if int(result)== 1:
            yprediction = "Fetal is in good health"
        if int(result) == 2:
         yprediction = "Suspect"
        if int(result) == 3:
            yprediction = "Pachogenic"
        return render_template("index.html", modelx_values = modelx_values, yprediction = yprediction, yresult = result)
   
if __name__ == "__main__":
    app.run(debug=True)
