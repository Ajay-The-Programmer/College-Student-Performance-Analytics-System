# College Student Performance Analytics System

A clean and simple Flask web application designed for a diploma college project to manage student records, track attendance, manage marks, view performance charts with Plotly, and predict student PASS or FAIL status using a simple Decision Tree machine learning model.

---

## 🎯 Project Modules

1. **Authentication**: Admin Login and Faculty Login
2. **Student Management**: Add, Edit, Delete, and Search Student records
3. **Attendance**: Mark Attendance and calculate Attendance Percentage
4. **Marks**: Add Marks, Edit Marks, and calculate Total Marks
5. **Dashboard**: View Total Students, Average Attendance, Pass/Fail Percentages, and Plotly Charts
6. **Machine Learning**: Predict PASS or FAIL status using a Decision Tree model
7. **Reports**: PDF Report generation

---

## 🛠️ Technology Stack

- **Python 3.12+**
- **Flask Framework**
- **MySQL & SQLAlchemy**
- **Bootstrap 5 UI**
- **Pandas & NumPy**
- **Scikit-learn** (Decision Tree Classifier)
- **Plotly** (Interactive Charts)

---

## 📁 Project Structure

```text
College-Student-Performance-Analytics-System/
├── app/
│   ├── admin/             # Admin Module Routes
│   ├── analytics/         # Performance Charts & ML Prediction Routes
│   ├── attendance/        # Attendance Tracking Routes
│   ├── auth/              # Login Routes (Admin & Faculty)
│   ├── marks/             # Marks & Scores Routes
│   ├── models/            # Database Models
│   ├── static/
│   │   ├── css/           # Styling Stylesheets
│   │   ├── images/        # Static Images
│   │   └── js/            # Client JavaScript
│   ├── students/          # Student Management Routes
│   ├── templates/         # HTML Page Templates
│   ├── extensions.py      # Flask Extensions Initialization
│   └── __init__.py        # Application Factory & Blueprint Registration
├── datasets/              # Dataset Files
├── docs/                  # Project Documentation
├── migrations/            # Database Migration Files
├── tests/                 # Unit Test Files
├── .env.example           # Environment Configuration Template
├── .gitignore             # Git Ignore File
├── config.py              # Application Configuration
├── requirements.txt       # Project Dependencies
├── run.py                 # Application Runner
└── README.md              # Project Readme
```

---

## ⚡ How to Run

```bash
# 1. Activate Virtual Environment
source venv/bin/activate

# 2. Install Required Dependencies
pip install -r requirements.txt

# 3. Run Application
python run.py
```

Access the application in your web browser at: `http://127.0.0.1:5000`