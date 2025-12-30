from flask import Flask, request, session as flask_session,render_template,flash,redirect,url_for
from flask_bcrypt import Bcrypt
from models import RegisterApp, session as db_session
#new

import jwt
from datetime import datetime, timedelta
from functools import wraps
from dotenv import load_dotenv
import os

load_dotenv()


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRES_IN = 60 * 60

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")  # No default value
bcrypt = Bcrypt(app)
#Flask secret key for session
#1
#app.secret_key = "this is secret key"

#jwt
      #1HOUR

#new
@app.before_request
def before_request():
    if request.method == 'POST' and '_method' in request.form:
        request.environ['REQUEST_METHOD'] = request.form['_method'].upper()

#JWT CREATE FUNCTION
def create_jwt_token(username):
    try:
        payload = {
            #"username":username,
            "username":username,
            "exp":datetime.now() + timedelta(seconds=JWT_EXPIRES_IN)
        }
        token = jwt.encode(payload,JWT_SECRET_KEY,algorithm="HS256")
        return token
    except Exception as e:
        return str(e)

def verify_jwt_token(token):
    try:
        payload = jwt.decode(token,JWT_SECRET_KEY,algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token has Expired"
    except jwt.InvalidTokenError:
        return "Invalid Token"

def login_required(f):
    @wraps(f)
    def wrapper(*args,**kwargs):
        token = request.cookies.get("jwt_token")
        if not token:
            flash("you need to login first","error")
            return redirect(url_for("login"))
        verification_result = verify_jwt_token(token)

        if isinstance(verification_result,str):
            flash(verification_result,"error")
            return redirect(url_for("login"))
        
        #payload ko request m store kr diya
        request.user = verification_result  #isiliye kr rhe h ye kuki ye fr updation m kam aayega
        return f(*args,**kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


#ADD CONTEXT PROCESSOR HERE
@app.context_processor
def inject_user():
    #Make current_user available in all templates
    def get_current_user():
        token = request.cookies.get("jwt_token")
        if token:
            result = verify_jwt_token(token)
            if not isinstance(result, str):
                return result
        return None
    return dict(current_user=get_current_user())

#jwt work done in this now in login part

@app.route("/")
def home():
    #return "this is home page"
    return render_template("home.html")

@app.route("/register",methods = ["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')   
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

    
        if not username or " " in username or username[0].isdigit() or not username.isalnum():
            #return "Username required, no spaces, must start with letter, only letter and numbers allowed"
            flash("Username required, no spaces, must start with letter, only letter and numbers allowed", "error")
            return render_template("register.html")

        if not email or "@" not in email or "." not in email.split("@")[-1]:
            #return "Invalid email"
            flash("Invalid email", "error")
            return render_template("register.html")

        if not password or password != confirm_password:
            #return "Password required and match confirm password"
            flash("Password required and must match confirm password", "error")
            return render_template("register.html")
        
        if db_session.query(RegisterApp).filter_by(username=username).first():
            #return "Username already exist"
            flash("Username already exists", "error")
            return render_template("register.html")
        if db_session.query(RegisterApp).filter_by(email=email).first():
            #return " email is already exists"
            flash("Email already exists", "error")
            return render_template("register.html")
        
        hashedPassword = bcrypt.generate_password_hash(password).decode("utf-8")

        new_user = RegisterApp(username=username,email = email,password = hashedPassword)
        db_session.add(new_user)
        db_session.commit()

        #return "Registeration Successful"
        flash("Registration Successful! Please login.", "success")
        return redirect(url_for("login"))
    #return "this is registeration page"
    return render_template("register.html")


#here jwt
# @login_required
@app.route("/login",methods = ["GET","POST"])
#@login_required   #create chicken and egg problem
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            #return "username and password is required"
            flash("Username and password are required", "error")
            return render_template("login.html")
        user = db_session.query(RegisterApp).filter_by(username = username).first()

        if not user:
            #return "user not found"
            flash("User not found", "error")
            return render_template("login.html")
    
        if not bcrypt.check_password_hash(user.password,password):
            #return "incorrect password"
            flash("Incorrect password", "error")
            return render_template("login.html")
        
        #session
        # flask_session["user_id"] = user.id
        # flask_session["username"] = user.username
        #return "login successful"

        #jwt
        token = create_jwt_token(user.username)
        # resp = "login Successful"
        # response = app.make_response(resp)
        response = redirect(url_for("home"))

        response.set_cookie(
            "jwt_token",
            token,
            httponly=True,
            samesite="Lax",
            secure=False,  
            max_age=3600  
            )
        flash("Login successful!", "success")
        return response

        #return "login successful"
    
    return render_template("login.html")
#1
@app.route("/logout",methods = ["POST"])
def logout():
    # response = app.make_response("logout successfull")
    response = redirect(url_for("home")) 
    response.set_cookie("jwt_token","",expires=0)
    flash("Logged out successfully", "success")
    return response
#2alternative and secure way to logout
# @app.route("/logout", methods=["POST"])
# def logout():
#     response = app.make_response("logout successful")

#     response.set_cookie(
#         "jwt_token",
#         "",
#         expires=0,
#         httponly=True,
#         samesite="Lax",
#         secure=False
#     )

#     return response


# @app.route("/logout",methods = ["POST"])
# def logout():
#     if "user_id" not in flask_session:
#         return "no user is logged in"

#     flask_session.clear()
    
#     return "logout successful"

@app.route('/partial/<string:username>', methods=["PATCH","POST"])
#jwt
@login_required
def partial(username):
    # if "user_id" not in flask_session:
    #     return "login required"
    logged_in_username = request.user["username"]
    
    #check if user is updating their own file    
    # if flask_session["username"] != username:
    #     return "you can only update your own profile"
    if logged_in_username != username:
        #return "you can only update your own profile"
        flash("you can only update your own profile","error")
        return redirect(url_for("home"))
    target_user = db_session.query(RegisterApp).filter_by(username=username).first()
    if not target_user:
       # return "user not found"
       flash("user not found","error")
       return redirect(url_for("home"))
    
    new_username = request.form.get("username") #here define
    email = request.form.get("email")
    password = request.form.get("password")

    updated = False

    # ADD USERNAME UPDATE LOGIC
    if new_username:
        if " " in new_username or new_username[0].isdigit() or not new_username.isalnum():
            flash("Username required, no spaces, must start with letter, only letter and numbers allowed", "error")
            return redirect(url_for("home"))
        
        if new_username != username and db_session.query(RegisterApp).filter_by(username=new_username).first():
            flash("Username already exists", "error")
            return redirect(url_for("home"))
        
        target_user.username = new_username
        updated = True
    

    if email:
          if "@" not in email or "." not in email.split("@")[-1]:
            #return "invalid email"
            flash("inmvalid email","error")
            return redirect(url_for("home"))
          target_user.email = email
          updated = True

    if password:
        if len(password) < 6:
            flash("password must be atleast 6 characters","error")
            return redirect(url_for("home"))
        hashed = bcrypt.generate_password_hash(password).decode("utf-8")
        target_user.password = hashed
        updated = True

    # if updated:
    #     db_session.commit()
    #     flash("profile partially updated successfully","success")
    # else:
    #     flash("No chamnges made","info")
    
    # return redirect(url_for("home"))
    if updated:
        db_session.commit()
        
        # If username was changed, update JWT token
        if new_username:
            token = create_jwt_token(new_username)
            response = redirect(url_for("home"))
            response.set_cookie(
                "jwt_token",
                token,
                httponly=True,
                samesite="Lax",
                secure=False,
                max_age=3600
            )
            flash("Profile partially updated successfully! Username changed.", "success")
            return response
        
        flash("Profile partially updated successfully!", "success")
    else:
        flash("No changes made", "info")
    
    return redirect(url_for("home"))


    #return f"user '{username}' partially updated successfully"


@app.route('/update/<string:username>', methods=["PUT","POST"])
@login_required
def update(username):
    # if "user_id" not in flask_session:
    #     return "login required"
    logged_in_username = request.user["username"]
    #Check if user is updating their own profile
    # if flask_session["username"] != username:
    #     return "u can only update your own profile"
    if logged_in_username != username:
        #return "u can only update your own profile"
        flash("You can only update your own profile", "error")
        return redirect(url_for("home"))
    

    updated_user = db_session.query(RegisterApp).filter_by(username=username).first()
    if not updated_user:
       # return "user not found"
        flash("User not found", "error")
        return redirect(url_for("home"))
    
    #require all to updte fully
    newUsername = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not newUsername or not email or not password:
        #return "all fields are required to update fully"
        flash("All fields are required for full update", "error")
        return redirect(url_for("home"))
    
    if not newUsername or " " in newUsername or newUsername[0].isdigit() or not newUsername.isalnum():
           # return "Username required, no spaces, must start with letter, only letter and numbers allowed"
           flash("Username required, no spaces, must start with letter, only letter and numbers allowed", "error")
           return redirect(url_for("home"))

    if not email or "@" not in email or "." not in email.split("@")[-1]:
            #return "Invalid email"
            flash("Invalid email", "error")
            return redirect(url_for("home"))
    
    if len(password) < 6:
        flash("Password must be at least 6 characters", "error")
        return redirect(url_for("home"))
    
    if newUsername != username and db_session.query(RegisterApp).filter_by(username = newUsername).first():
        #return "username already exist"
        flash("Username already exists", "error")
        return redirect(url_for("home"))
    
    if email != updated_user.email and db_session.query(RegisterApp).filter_by(email=email).first():
        #return "email already  exists"
        flash("Email already exists", "error")
        return redirect(url_for("home"))
    #update krre
    updated_user.username = newUsername
    updated_user.email = email
    updated_user.password = bcrypt.generate_password_hash(password).decode("utf-8")

    if newUsername != username:
        flask_session[username]= newUsername
    
    db_session.commit()
    #return f"user {username} updated successfully to {newUsername}"
    # Update the JWT token with new username
    token = create_jwt_token(newUsername)
    response = redirect(url_for("home"))
    response.set_cookie(
        "jwt_token",
        token,
        httponly=True,
        samesite="Lax",
        secure=False,
        max_age=3600
    )
    
    flash(f"Profile fully updated successfully! Username changed to {newUsername}", "success")
    return response



if __name__ == "__main__":
    app.run(debug=True)