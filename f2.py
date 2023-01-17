from flask import Flask,render_template,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

# Init App
app=Flask(__name__)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"]= "mysql://root:@localhost/clients2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail Configuration
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'ambarish.bhagawati8653@gmail.com'
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

# Initalize DB
db = SQLAlchemy(app)
mail = Mail(app)
db.init_app(app)

class Users2(db.Model):
    Username=db.Column(db.String,primary_key=True)
    Password=db.Column(db.String)

    def __init__(self,Username,Password):
        self.Username=Username
        self.Password=Password 

@app.route('/mail')
def email():
    msg = Message( 'Hello Message', sender='ambarish.bhagawati8653@gmail.com', recipients=['ambarishbhagawati8969@gmail.com'])
    mail.send(msg)

@app.route('/showall')
def show_all():
   return render_template('Show_all.html', users2 = Users2.query.all() )

@app.route('/api/<string:user>')
def show_employee(user):
    user=Users2.query.filter_by(Username=user).first()
    data={
        'Username':user.Username,
        'Password':user.Password
    }
    return jsonify(data)

@app.route('/api')
def show_employees():
    users=Users2.query.all()
    data=[{
            "Username": user.Username,
            "Password": user.Password,
        } for user in users]
    return jsonify(data)

@app.route('/createuser',methods=['GET','POST'])
def create():
    if(request.method=='POST'):
        username2=request.form.get('username2')
        password2=request.form.get('password2')
        entry=Users2(Username=username2,Password=password2)
        db.session.add(entry)
        db.session.commit()
    return render_template('Create.html')      

@app.route('/delete/<string:username>',methods=['GET','POST','DELETE'])
def delete(username):
    if(request.method=='POST'):
        entry=Users2.query.get(username)
        db.session.delete(entry)
        db.session.commit()
        return f"<p>User {username} Deleted.</p> <a href='/showall'>Go to Showall Users</a>"
    return render_template('Delete.html',username=username)

@app.route('/edit/<string:username>',methods=['GET','POST'])
def edituser(username):
    update=Users2.query.get_or_404(username)
    if request.method=='POST':
        update.Password=request.form['password3']
        # entry=Users2(Password=password3)
        # db.session.add(entry)
        db.session.commit()
        return f"<p>User {username} Updated.</p> <a href='/showall'>Go to Showall Users</a>"
    return render_template('Edit.html',username3=username)


@app.route('/')
def Home():
    return render_template('Home.html')

@app.route('/info/<username>')
def Info(username):
    return render_template('Info.html',username1=username)

# Run Server
app.run(debug=True)