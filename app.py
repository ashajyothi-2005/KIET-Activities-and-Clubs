from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

# ------------------ Flask App Setup ------------------
app = Flask(__name__)
app.secret_key = "your_secret_key"   # Required for session management

# ------------------ MongoDB Connection ------------------
# Local MongoDB
app.config["MONGO_URI"] = "mongodb+srv://kietactivities:Asha@098@cluster0.cmcf776.mongodb.net/college_activities"

# For MongoDB Atlas (Cloud), replace with your connection string:
# app.config["MONGO_URI"] = "mongodb+srv://<username>:<password>@cluster0.mongodb.net/college_activities"

mongo = PyMongo(app)

# Collections
users = mongo.db.users
contacts = mongo.db.contacts

# ------------------ General Routes ------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("home.html")

# ------------------ Register ------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        rollno = request.form.get("rollno", "").strip()
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        if not rollno or not name or not email or not password:
            flash("Please fill all fields", "warning")
            return redirect(url_for("register"))

        if users.find_one({"email": email}):
            flash("Email already registered! Please login.", "warning")
            return redirect(url_for("login"))

        users.insert_one({
            "rollno": rollno,
            "name": name,
            "email": email,
            "password": generate_password_hash(password)
        })

        flash("Registered successfully! Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")   # ✅ Fixed: should render register.html, not home.html

# ------------------ Login ------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = users.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            session["user"] = email
            flash("Login successful!", "success")
            return redirect(url_for("about"))
        else:
            flash("Invalid email or password!", "danger")

    return render_template("login.html")

# ------------------ About ------------------
@app.route("/about")
def about():
    if "user" not in session:
        flash("Please login first", "warning")
        return redirect(url_for("login"))
    return render_template("about.html")

# ------------------ Activities ------------------
@app.route("/activities")
def activities():
    return render_template("activities.html")

# ------------------ Clubs ------------------
@app.route("/clubs")
def clubs():
    return render_template("clubs.html")

# ------------------ Contact ------------------
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not message:
            flash("Please fill all fields", "warning")
            return redirect(url_for("contact"))

        contacts.insert_one({
            "name": name,
            "email": email,
            "message": message
        })

        flash("Your message has been sent!", "success")
        return redirect(url_for("contact"))

    return render_template("contact.html")

# ------------------ Logout ------------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

# ------------------ Club Detail Pages ------------------
@app.route("/gcc")
def gcc():
    return render_template("gcc.html")

@app.route("/khub")
def khub():
    return render_template("khub.html")

@app.route("/toastmaster")
def toastmaster():
    return render_template("toastmaster.html")

@app.route("/robotics")
def robotics():
    return render_template("robotics.html")

@app.route("/smartcity")
def smartcity():
    return render_template("smartcity.html")

@app.route("/ncc")
def ncc():
    return render_template("ncc.html")

@app.route("/nss")
@app.route("/national-social-service")
def nss():
    return render_template("nss.html")

# ------------------ Run App ------------------
if __name__ == "__main__":
    app.run(debug=True)
