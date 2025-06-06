from flask import Flask, render_template, request, redirect, url_for, session, send_file,jsonify
import sqlite3
import bcrypt
import joblib
import numpy as np
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load the heart disease prediction model
model = joblib.load("random_forest_model_11features.joblib")

DB_PATH = "userdb.db"

def create_users_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usersdb (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_users_table()

def check_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM usersdb WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return True
    return False

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        username = data.get("username")
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usersdb WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return jsonify({"status": "error", "message": "Username already taken!"})

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute("INSERT INTO usersdb (username, email, phone, password) VALUES (?, ?, ?, ?)",
                    (username, email, phone, hashed_password.decode('utf-8')))
        conn.commit()
        conn.close()

        return jsonify({"status": "success", "message": "Account created successfully!"})
    return render_template('signup.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if check_login(username, password):
            session["user"] = username
            return jsonify({"status": "success", "message": "Login Successful!"})
        else:
            return jsonify({"status": "error", "message": "Invalid Credentials!"})
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if "user" in session:
        return render_template('heart1.html')
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    if "user" not in session:
        return redirect(url_for('login'))

    try:
        user_data = {
            "Age": request.form['age'],
            "Gender": request.form['gender'],
            "Chest Pain Type": request.form['chest_pain'],
            "Resting BP": request.form['resting_bp'],
            "Cholesterol": request.form['serum_cholesterol'],
            "Fasting Blood Sugar": request.form['fasting_blood_sugar'],
            "Resting ECG": request.form['resting_ecg'],
            "Max Heart Rate": request.form['max_heart_rate'],
            "Exercise Angina": request.form['exercise_angina'],
            "ST Depression": request.form['st_depression'],
            "Slope ST Segment": request.form['slope_st']
        }

        input_data = np.array([[float(user_data[key]) for key in user_data]])

        prediction = model.predict(input_data)[0]
        result = "High Risk of Heart Disease.You need to approach the doctor " if prediction > 0 else "Low Risk of Heart Disease"

        session["report_data"] = user_data
        session["prediction_result"] = result

        return redirect(url_for('high_risk' if prediction > 0 else 'healthy'))

    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/download_report')
def download_report():
    if "report_data" not in session or "prediction_result" not in session:
        return redirect(url_for('home'))

    user_data = session["report_data"]
    prediction_result = session["prediction_result"]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Add border for the whole page
    pdf.rect(5, 5, 200, 287)  # (x, y, width, height)

    # Report Title
    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(200, 10, "HEART DISEASE PREDICTION REPORT", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Person Details:", ln=True, align='L')

    pdf.set_font("Arial", size=10)

    col_width = 80
    row_height = 8

    pdf.ln(5)
    for key, value in user_data.items():
        pdf.set_font("Arial", style='B', size=10)  # Bold column name
        pdf.cell(col_width, row_height, f"{key}:", border=2)  # Double-line border
        pdf.set_font("Arial", size=10)
        pdf.cell(col_width, row_height, value, border=2)  # Double-line border
        pdf.ln(row_height)

    pdf.ln(10)
    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(200, 10, "Conclusion:", ln=True, align='L')

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, f"Prediction Result: {prediction_result}")

    report_path = "Heart_Disease_Report.pdf"
    pdf.output(report_path)

    return send_file(report_path, as_attachment=True)
@app.route('/result2')
def high_risk():
    return render_template('result2.html')

@app.route('/result3')
def healthy():
    return render_template('result3.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000) 