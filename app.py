from flask import Flask, render_template, request, redirect, flash, url_for, session
import re
import os
import csv
import joblib
import sklearn
import pandas as pd
import mysql.connector
from werkzeug.security import generate_password_hash,check_password_hash

# Load saved model
model=joblib.load('lr_car_price_prediction.pkl')
              
app = Flask(__name__)
app.secret_key='3344'

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cardb"
    )

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/services')
def methodology():
    return render_template("services.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':
        # take user input
        Make = request.form['Make']
        Year = int(request.form['Year'])
        Engine_Size = float(request.form['Engine_Size'])
        Transmission = request.form['Transmission']
        Mileage = int(request.form['Mileage'])
        Model = request.form['Model']
        Fuel_Type = request.form['Fuel_Type']

        if Transmission=='Automatic':
            Transmission=0
        else:
            Transmission=1
  
        Make_Audi,Make_BMW,Make_Ford,Make_Honda,Make_Toyota=0,0,0,0,0
        if Make=='Audi':
             Make_Audi=1
        elif Make=='BMW':
            Make_BMW=1
        elif Make=='Ford':
            Make_Ford=1
        elif Make=='Honda':
            Make_Honda=1    
        else:
            Make_Toyota=1 

        Model_Model_A,Model_Model_B, Model_Model_C,Model_Model_D,Model_Model_E=0,0,0,0,0
        if Model=='Model A':
            Model_Model_A=1
        elif Model=='Model B':
            Model_Model_B=1
        elif Model=='Model C':
            Model_Model_C=1 
        elif Model=='Model D':
            Model_Model_D=1    
        else:
            Model_Model_E=1 

        Fuel_Type_Diesel,Fuel_Type_Electric,Fuel_Type_Petrol=0,0,0
        if Fuel_Type=='Diesel':
            Fuel_Type_Diesel=1
        elif Fuel_Type=='Electric':
            Fuel_Type_Electric=1    
        else:
             Fuel_Type_Petrol=1  

        data=pd.DataFrame([[Year,Engine_Size,Mileage,Transmission,Make_Audi,Make_BMW,Make_Ford,Make_Honda,Make_Toyota,
                             Fuel_Type_Diesel,Fuel_Type_Electric,Fuel_Type_Petrol,
                             Model_Model_A,Model_Model_B, Model_Model_C,Model_Model_D,Model_Model_E]],
                        columns=['Year', 'Engine Size', 'Mileage', 'Transmission', 'Make_Audi',
                'Make_BMW', 'Make_Ford', 'Make_Honda', 'Make_Toyota',
                'Fuel Type_Diesel', 'Fuel Type_Electric', 'Fuel Type_Petrol',
                'Model_Model A', 'Model_Model B', 'Model_Model C', 'Model_Model D',
                'Model_Model E'])

        result=model.predict(data)[0]
        prediction = round(result, 2)

        return render_template("prediction.html", prediction=prediction)


    return render_template("prediction.html")


@app.route('/register',methods=['GET','POST'])
def register_page():
    if request.method=='POST':
        uname=request.form['uname']
        email=request.form['email']
        password=request.form['password']

   
        if not uname.strip():
            flash("Username is required","danger")
            return redirect(url_for('/register')) 


        if not re.match(r"[^@]+@[^@]+\.[^@]",email):
            flash("Invalid email address","danger")
            return redirect('/register')


        if len(password)<6:
            flash("Password must be atleast 6 characters","danger")
            return redirect('/register') 
        hashed_password=generate_password_hash(password)
        conn=get_db_connection()
        cursor=conn.cursor() 


        cursor.execute("SELECT u_id FROM users WHERE email=%s",(email,))
        if cursor.fetchone():
            flash("Email already registered","danger")
            cursor.close()
            conn.close()
            return redirect('/register')

        cursor.execute(
            "INSERT INTO users (uname,email,password) VALUES (%s,%s,%s)",
            (uname,email,hashed_password)
        )
        conn.commit()
        cursor.close()
        conn.close()

        flash("Registration is successful,Please Login","success")
        return redirect('/login')

   
    return render_template('register.html')


@app.route('/login',methods=['GET','POST'])
def login_page():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if not re.match(r"[^@]+@[^@]+\.[^@]",email):
            flash("Invalid email address","danger")
            return redirect('/register')

        if len(password)<6:
            flash("Password must be atleast 6 characters","danger")
            return redirect('/register') 

        conn=get_db_connection()
        cursor=conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s",(email,))
        user=cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'],password):
            session['user_id']=user['u_id']
            session['username']=user['uname']
            return redirect('/')
        else:
            flash("Invalid email or password","danger")
            return redirect('/login')
        


    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True, port=4000)
