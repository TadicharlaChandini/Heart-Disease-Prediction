#  Heart Disease Prediction 

A full-stack web application that predicts the likelihood of heart disease based on user health data. It enables users to securely log in, input their health parameters, receive risk predictions, and download a personalized report.

This system aims to assist individuals and healthcare providers in early detection and informed decision-making for heart health management.

---

## 🚀 Features

- 🔐 User Registration & Login with secure authentication
- 📝 Input health parameters through a user-friendly form
- 🤖 Machine Learning-powered heart disease risk prediction
- 🧾 Downloadable personalized health and prediction report
- 🗃️ SQLite database for storing user data and predictions
- 🎨 Clean, responsive UI styled with HTML5 and CSS3
- 🖥️ Frontend integrated via Jupyter Notebook for ease of visualization and updates

---

## 💻 Tech Stack

| Layer         | Technology                        |
|---------------|---------------------------------|
| Backend       | Python (Flask)                  |
| Frontend      | HTML5, CSS3                     |
| Styling       | Custom CSS                      |
| Database      | SQLite3                        |
| Machine Learning | Scikit-learn, Pandas, NumPy  |
| Tool           | Jupyter Notebook                        |
| Deployment    | Local / Planned cloud deployment|

---

## 🗂️ Folder Structure

heart-disease-prediction/  
│  
├── static/          # CSS and other static files  
├── templates/       # HTML templates for Flask  
├── notebooks/       # Jupyter Notebook frontend files  
├── reports/         # Generated reports for users  
│  
├── app.py           # Flask backend app  
├── model.pkl        # Trained ML model file  
├── requirements.txt # Dependencies  
├── database.db      # SQLite database file  
└── README.md        # Project overview  

---

## 🧠 How It Works

1. User registers or logs in to their account.  
2. User inputs health data (age, blood pressure, cholesterol, etc.) via the frontend form.  
3. Flask backend processes inputs and uses the ML model to predict heart disease risk.  
4. Prediction results are displayed on the frontend.  
5. User can download a detailed report containing inputs and prediction outcome.  
6. All user data and predictions are securely stored in an SQLite database.

---

## 🧑‍💻 Developed By

**Tadicharla Chandini**  
B.Tech in AI & Data Science  
[LinkedIn 🔗](https://www.linkedin.com/in/chandini-tadicharla-5952022a6/)  
[GitHub 🔗](https://github.com/TadicharlaChandini)  

---

## 📦 Installation (Local Setup)

```bash
git clone https://github.com/TadicharlaChandini/heart-disease-prediction.git
cd heart-disease-prediction
pip install -r requirements.txt
python app.py

🌐 Deployment
The project can be deployed on platforms like Render or Heroku for free public access. Deployment instructions coming soon!

📜 License
This project is open-source and free to use for academic and personal purposes.

Feel free to reach out for questions or collaboration!
Email: tadicharlachandini@gmail.com
GitHub: https://github.com/TadicharlaChandini
LinkedIn: https://www.linkedin.com/in/chandini-tadicharla-5952022a6/
