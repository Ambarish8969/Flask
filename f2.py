from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]= "mysql://root:@localhost/clients2"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

class Users2(db.Model):
    Username=db.Column(db.String,primary_key=True)
    Password=db.Column(db.String)

    # def __init__(self,Username,Password):
    #     self.Username=Username
    #     self.Password=Password 

@app.route('/showall')
def show_all():
   return render_template('Show_all.html', users2 = Users2.query.all() )

@app.route('/showall/<string:user>')
def show_employee(user):
    user=Users2.query.filter_by(Username=user).first()
    return [user.Username,user.Password]

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
    return render_template('Delete.html')

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

app.run(debug=True)