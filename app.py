import numpy as np
import datetime as dt
import pickle
import os
from flask import Flask, render_template,request

# https://www.geeksforgeeks.org/how-to-use-web-forms-in-a-flask-application/
# Initalize Flask
app = Flask(__name__)
app.config["DEBUG"] = True

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
lgcl_model_url = os.path.join(SITE_ROOT, "static/models", "lgcl.pkl")
kncl_model_url = os.path.join(SITE_ROOT, "static/models", "kncl.pkl")
svcl_model_url = os.path.join(SITE_ROOT, "static/models", "svcl.pkl")
dtcl_model_url = os.path.join(SITE_ROOT, "static/models", "dtcl.pkl")
rfcl_model_url = os.path.join(SITE_ROOT, "static/models", "rfcl.pkl")

# lgmodel = pickle.load(open(lgcl_model_url, 'rb'))
# knmodel = pickle.load(open(kncl_model_url, 'rb'))
# svmodel = pickle.load(open(svcl_model_url, 'rb'))
# dtmodel = pickle.load(open(dtcl_model_url,'rb'))
rfmodel = pickle.load(open(rfcl_model_url, 'rb'))

# prediction function
def ValuePredictor(to_predict_list):
    to_predict = np.array(to_predict_list).reshape(1, 12)
    result = rfmodel.predict(to_predict)
    return result[0]

@app.route('/') # Homepage
def home():
    return render_template('index.html')
 
@app.route('/heart', methods = ['POST'])
def result():
    if request.method == 'POST':
        init_features = [float(x) for x in request.form.values()]
        # xto_predict_list = [np.array(init_features)]

        # to_predict_list = request.form.to_dict()
        # to_predict_list = list(to_predict_list.values())
        # to_predict_list = list(map(int, to_predict_list))
        # result = ValuePredictor(to_predict_list)       
        # if int(result)== 1:
            #  prediction ='Probable Heart Disease '
        # else:
            #  prediction ='Heart Disease improbable'

        value_list = {"1"}
        prediction = {"xxxxx"}
        return render_template("index.html", values_list = value_list, prediction = prediction)


if __name__ == "__main__":
    app.run(debug=True)