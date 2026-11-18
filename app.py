from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.errors import InvalidId
from datetime import datetime


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = "college_complaint_secret_key_123"


# =========================================================
# MONGODB CONNECTION
# =========================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["college_complaint_db"]

students = db["students"]
complaints = db["complaints"]


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# STUDENT REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        department = request.form.get("department", "").strip()
        year = request.form.get("year", "").strip()
        roll_number = request.form.get("roll_number", "").strip()

        # Check required fields
        if not name or not email or not password or not roll_number:

            return render_template(
                "register.html",
                error="Please fill all required fields."
            )

        # Check existing email
        existing_student = students.find_one({
            "email": email
        })

        if existing_student:

            return render_template(
                "register.html",
                error="Email already registered. Please login."
            )

        # Check existing roll number
        existing_roll = students.find_one({
            "roll_number": roll_number
        })

        if existing_roll:

            return render_template(
                "register.html",
                error="Roll number already registered."
            )

        # Create student
        students.insert_one({

            "name": name,
            "email": email,
            "password": password,
            "department": department,
            "year": year,
            "roll_number": roll_number,
            "created_at": datetime.now()

        })

        # After registration go to student login
        return redirect(url_for("student_login"))

    return render_template("register.html")


# =========================================================
# STUDENT LOGIN
# =========================================================

@app.route("/student/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        # Find student
        student = students.find_one({
            "email": email,
            "password": password
        })

        # Wrong details
        if student is None:

            return render_template(
                "login.html",
                error="Invalid email or password."
            )

        # Login session
        session["student_logged_in"] = True
        session["student_email"] = email
        session["student_name"] = student.get("name", "")
        session["student_roll_number"] = student.get(
            "roll_number",
            ""
        )

        # Go to dashboard
        return redirect(url_for("student_dashboard"))

    return render_template("login.html")


# =========================================================
# LOGIN ALIAS
# =========================================================

@app.route("/student/login", endpoint="login")
def login_alias():

    return redirect(url_for("student_login"))


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/student/dashboard")
def student_dashboard():

    if not session.get("student_logged_in"):

        return redirect(url_for("student_login"))

    email = session.get("student_email")

    student = students.find_one({
        "email": email
    })

    student_complaints = list(
        complaints.find({
            "student_email": email
        }).sort("_id", -1)
    )

    return render_template(
        "student_dashboard.html",
        student=student,
        complaints=student_complaints
    )


# =========================================================
# MY COMPLAINTS
# =========================================================

@app.route("/student/complaints")
def my_complaints():

    if not session.get("student_logged_in"):

        return redirect(url_for("student_login"))

    email = session.get("student_email")

    student_complaints = list(
        complaints.find({
            "student_email": email
        }).sort("_id", -1)
    )

    return render_template(
        "my_complaints.html",
        complaints=student_complaints
    )


# =========================================================
# SUBMIT COMPLAINT PAGE
# =========================================================

@app.route("/student/complaint/new")
def complaint_form():

    if not session.get("student_logged_in"):

        return redirect(url_for("student_login"))

    return render_template("complaint_form.html")


# =========================================================
# SUBMIT COMPLAINT
# =========================================================

@app.route("/student/complaint/submit", methods=["POST"])
def submit_complaint():

    if not session.get("student_logged_in"):

        return redirect(url_for("student_login"))

    email = session.get("student_email")
    name = session.get("student_name", "")

    title = request.form.get("title", "").strip()
    category = request.form.get("category", "").strip()
    description = request.form.get("description", "").strip()

    if not title or not category or not description:

        return render_template(
            "complaint_form.html",
            error="Please fill all fields."
        )

    complaints.insert_one({

        "student_name": name,
        "student_email": email,
        "title": title,
        "category": category,
        "description": description,
        "status": "Pending",
        "created_at": datetime.now(),
        "updated_at": datetime.now()

    })

    return redirect(url_for("my_complaints"))


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        # Demo admin credentials
        if email == "admin@gmail.com" and password == "admin123":

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        return render_template(
            "admin_login.html",
            error="Invalid admin email or password."
        )

    return render_template("admin_login.html")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
def admin_dashboard():

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin_login"))

    all_complaints = list(
        complaints.find().sort("_id", -1)
    )

    total = complaints.count_documents({})

    pending = complaints.count_documents({
        "status": "Pending"
    })

    in_progress = complaints.count_documents({
        "status": "In Progress"
    })

    resolved = complaints.count_documents({
        "status": "Resolved"
    })

    return render_template(
        "admin_dashboard.html",
        complaints=all_complaints,
        total=total,
        pending=pending,
        in_progress=in_progress,
        resolved=resolved
    )


# =========================================================
# ADMIN COMPLAINT DETAILS
# =========================================================

@app.route("/admin/complaint/<complaint_id>")
def complaint_details(complaint_id):

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin_login"))

    try:

        complaint = complaints.find_one({
            "_id": ObjectId(complaint_id)
        })

    except (InvalidId, TypeError):

        return "Invalid complaint ID", 400

    if complaint is None:

        return "Complaint not found", 404

    return render_template(
        "complaint_details.html",
        complaint=complaint
    )


# =========================================================
# UPDATE COMPLAINT STATUS
# =========================================================

@app.route(
    "/admin/complaint/<complaint_id>/status",
    methods=["POST"]
)
def update_status(complaint_id):

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin_login"))

    status = request.form.get("status", "").strip()

    allowed_status = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if status not in allowed_status:

        return "Invalid status", 400

    try:

        complaints.update_one(

            {
                "_id": ObjectId(complaint_id)
            },

            {
                "$set": {
                    "status": status,
                    "updated_at": datetime.now()
                }
            }

        )

    except (InvalidId, TypeError):

        return "Invalid complaint ID", 400

    return redirect(
        url_for(
            "complaint_details",
            complaint_id=complaint_id
        )
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("home"))


# =========================================================
# STUDENT LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("home"))


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )