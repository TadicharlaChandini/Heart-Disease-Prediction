from flask import Flask, render_template, request, redirect, url_for
import joblib
import numpy as np

app = Flask(__name__)

# Load the trained model (make sure the model file is in the same directory)
model = joblib.load('random_forest_model.joblib')

# Route for the main input form
@app.route('/')
def home():
    return render_template('heart1.html')

# Route to handle form submission
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        age = int(request.form['age'])
        serum_cholesterol = int(request.form['serum_cholesterol'])
        # Add more features as necessary

        # Prepare the input data for the model (assuming you have more features, adjust accordingly)
        input_data = np.array([[age, serum_cholesterol]])  # Reshaping for the model
        
        # Make prediction using the trained model
        prediction = model.predict(input_data)

        # Redirect based on prediction
        if prediction[0] == 1:
            return redirect(url_for('high_risk'))
        else:
            return redirect(url_for('healthy'))

    except Exception as e:
        # Handle errors (e.g., incorrect inputs)
        return f"Error: {str(e)}"

# Route for high-risk page
@app.route('/result2')
def high_risk():
    return render_template('result2.html')

# Route for healthy page
@app.route('/result3')
def healthy():
    return render_template('result3.html')

if __name__ == '__main__':
    app.run(debug=True)
