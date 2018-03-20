##change the validators of age to number 
## del the sql table and add new one
## chnage the validators and limit of text allowed. 

from flask import Flask, render_template , redirect ,session,  url_for, request, make_response

from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, PasswordField, validators, validators, ValidationError, TextAreaField, TextField
from wtforms.validators import InputRequired, Email, Length, URL, NumberRange
from flask_wtf import Form
from flask_wtf import FlaskForm

from flask_bootstrap import Bootstrap
from datetime import datetime
import random, string
from sqlalchemy import desc


app = Flask(__name__)
Bootstrap(app)



#SQLALCHEMY_DATABASE_URI='mysql://username:password@server/databasename'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://lol1:Sb11?gb2N_hB@den1.mysql3.gear.host/lol1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = "some_string"

#3 creating the mysql table!
class posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))   #
    book = db.Column(db.String(80))  # book is not used anywhere 
    age = db.Column(db.String(2))   # 
    tvshow = db.Column(db.String(80))
    color = db.Column(db.String(30))
    car= db.Column(db.String(80))
    HomeAdress= db.Column(db.String(200))#
    email = db.Column(db.String(90))#
    officeAdress = db.Column(db.String(80))#
    phoneNumber= db.Column(db.String(20))#
    favPhone = db.Column(db.String(70))#

#For 1st page of form 
class Post_Form(Form):
    name = TextField('Your Name',validators=[InputRequired(), Length(min=5, max=60, message="The field must be between 5 and 80 characters long")],render_kw={"placeholder": "Your Name"})
    age= TextField("Your Age", validators=[InputRequired()],render_kw={"placeholder": "Age"})
    email = TextField("Email Address",validators=[InputRequired(),Email(message='Enter a valid email'), Length(min=10, max=90)],render_kw={"placeholder": "Your Email Address"}) 
    HomeAdress = TextField("your home address",validators=[InputRequired(), Length(min=3, max=80, message="The field must be between 5 and 80 characters long")],render_kw={"placeholder": "enter your home address"}) # name of the author
    
   
    
##for 2nd page of form 
class form2(Form):
    officeAdress = TextField('Your Office address', validators=[InputRequired(), Length(min=5, max=80, message="The field must be between 5 and 80 characters long")] ,render_kw={"placeholder": "Address of your office"})
    phoneNumber = TextField("Your Phone Number",validators=[InputRequired(), Length(min=3, max=12, message="The field must be between 5 and 11 characters long")],render_kw={"placeholder": "Enter your phone number"})
    tvshow = TextField('Your Favroute TV show', validators=[InputRequired(), Length(min=5, max=80, message="The field must be between 5 and 80 characters long")] ,render_kw={"placeholder": "Subtitle Of Your Post"})

##for 3rd page of form 
class form3(Form):
    favPhone = TextField('Your favourite phone', validators=[InputRequired(), Length(min=5, max=70, message="The field must be between 5 and 70 characters long")] ,render_kw={"placeholder": "your favourite phone"})
    car = TextField('Your favourite car', validators=[InputRequired(), Length(min=5, max=80, message="The field must be between 5 and 80 characters long")] ,render_kw={"placeholder": "your favourite car"})
    color = TextField('Your favourite colour', validators=[InputRequired(), Length(min=5, max=30, message="The field must be between 5 and 30 characters long")] ,render_kw={"placeholder": "your favourite colour"})
    
    
    
#To give the random endpoint to the url
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))





@app.route('/form', methods = ['GET','POST'])
def form():
    form = Post_Form(request.form)   
    if request.method == "GET":
        session.pop('name', None)
        return render_template('form.html', form=form)
    elif request.method == "POST":
        if form.validate_on_submit():
            url_genrator = randomword(5)
            postedDate = datetime.utcnow().strftime("%d-%m-%y")
            session['name'] = form.name.data
            session['age'] = form.age.data
            session['email'] = form.email.data
            return redirect(url_for('form_2'))
        else : 
            return render_template("form.html",form=form)





@app.route('/form2', methods = ['GET', 'POST'])
def form_2():
    form = form2(request.form)
    if request.method == 'GET':
        if 'name' in session:
            return render_template('form2.html', form= form)
        else: 
            return "fill the 1st from to access this form! (Or I can just redirect the user to first page of the form.) "  # or redirect to form1 
    elif request.method == "POST":
        if form.validate_on_submit():
            session['officeAdress'] = form.officeAdress.data
            session['phoneNumber'] = form.phoneNumber.data
            session['tvshow'] = form.tvshow.data

            return redirect(url_for('form_3'))
        else :
            return render_template ('form2.html', form = form)
            
        
@app.route ('/form3', methods=['GET', 'POST'])
def form_3():
    form =  form3(request.form)
    if request.method == 'GET':
        if 'phoneNumber' in session:
            return render_template('form3.html', form= form)
        else: 
            return "fill the 2nd from to access this form! (Or I can just redirect the user to the first page of the form. )"
    elif request.method == 'POST':
        if form.validate_on_submit():
            session['favPhone'] = form.favPhone.data
            session['car'] = form.car.data
            session['color'] = form.color.data
            return redirect(url_for('form_submitted'))
        else :
            return render_template ('form3.html', form = form)
            

@app.route("/form-submitted")
def form_submitted():
    if 'color' in session:
        
        d = session['age']
        e = session['tvshow']
        f = session['color']
        g = session['car']
        #h = session['HomeAdress']
        i = session['email']
        j = session['officeAdress']
        k = session['phoneNumber']
        l = session['favPhone']
        b = session['name']
        Data = posts(name=b , age= d, tvshow= e , color= f , car= g,  email= i, officeAdress= j, phoneNumber= k, favPhone= l  )
        db.session.add(Data)
        db.session.commit()
        session.pop('name', None)
        session.pop('phoneNumber', None)
        session.pop('color', None)
        return render_template("form-submitted.html") 
        
    else:     
        return 'Fill the complete form first'
 




##This endpoint will show the list of all the guest posts
@app.route('/posts', methods= ['GET'])
def submitted_posts():
    dbData = posts.query.order_by(posts.id.desc()).all()  
    return render_template('post_submitted.html', dbData= dbData  )



#this endpoint will the specific post and the post will have a randon endpoint
@app.route('/guest-post/<random_id>')
def guest_post(random_id):
    article = posts.query.filter_by(random=random_id ).one()
    return render_template ('guest_post.html', post = article)
    
@app.route('/')
def index():
    return render_template ('index.html')
    


@app.errorhandler(404)
def page_not_found(e) :
    return render_template("404.html")

# using the same image as 404 error so that if someone tries something mischief, it will still give a 404 error. 
@app.errorhandler(500)
def function(e) :
    return render_template("404.html")


if __name__ == "__main__":
    app.run(port=5556 ,debug=True)
	  
