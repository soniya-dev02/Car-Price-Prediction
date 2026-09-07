## Car Price Prediction

A machine learning-based web application that predicts the estimated price of a used car based on its specifications.

### Project Overview

This project uses a Linear Regression model to predict used car prices. The trained machine learning model is integrated with a Flask web application, allowing users to enter car details and receive an estimated price.

The application also uses MySQL for database management and user authentication.

### Technologies Used

- Python
- Flask
- Pandas
- NumPy
- Scikit-learn
- Joblib
- MySQL
- MySQL Connector
- HTML
- CSS

### Features

- Used car price prediction
- Linear Regression machine learning model
- Flask-based web application
- MySQL database integration
- User registration and login
- Car make selection
- Car model selection
- Year input
- Engine size input
- Transmission selection
- Mileage input
- Fuel type selection
- Estimated price prediction

### Machine Learning

The project uses a Linear Regression model to estimate used car prices based on vehicle specifications.

### Input Features

- Year
- Engine Size
- Mileage
- Transmission
- Car Make
- Car Model
- Fuel Type

### Machine Learning Workflow

- Data preprocessing
- Feature encoding
- Model training
- Model evaluation
- Price prediction

### Web Application

The Flask application provides the following pages:

- Home
- About
- Services
- Contact
- Prediction
- Registration
- Login

Users can enter vehicle details and receive an estimated car price.

### Project Structure

```text
Car-Price-Prediction/
│
├── static/
├── templates/
├── Car Price Prediction.ipynb
├── Transmission.pkl
├── app.py
├── car.sql
├── lr_car_price_prediction.pkl
├── scaler_lr_model_car_price_prediction.pkl
└── README.md
