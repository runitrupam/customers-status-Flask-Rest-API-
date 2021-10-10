from flask import Flask,jsonify,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Prof(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False )
    dob = db.Column(db.Date , nullable=True)
    status = db.Column(db.String(200), nullable=False , default = 'Active' )
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    def __repr__(self) -> str:
        return f"{self.sno} - {self.name} - {self.dob}"




@app.route("/",methods =  ['GET','POST'])
def hello_world():
    print(datetime.utcnow())
    if request.method == 'POST':
        print(request.form['Prof_Name'])
        name = request.form['Prof_Name']
        date_str = str(request.form['DOB'])  
        yy , mm ,dd = int(date_str[:4]) , date_str[5:7] , date_str[8:10]
        dob = datetime(yy, int(mm), int(dd))
        status = request.form['Status']  
        t1 = Prof(name = name,dob = dob , status = status) # object of class Prof
        db.session.add(t1) 
        db.session.commit()
    allProf = Prof.query.all()
    #print(allProf)
    return render_template("index.html",allProf = allProf  )

@app.route("/paused",methods =  ['GET'])
def show_paused():
    #print(datetime.utcnow())
    print("in pauesrf")
    allProf = Prof.query.filter_by(status ='Paused').all()
    #print(allProf)
    return render_template("paused_index.html",allProf = allProf  )

@app.route("/active",methods =  ['GET'])
def show_active():
    #print(datetime.utcnow())
    print("in active")
    allProf = Prof.query.filter_by(status ='Active').all()
    #print(allProf)
    return render_template("active_index.html",allProf = allProf  )


@app.route("/update/<int:sno>",methods = ['POST','GET'])
def update(sno):
    if request.method == 'POST':
        name = request.form['Prof_Name']
        date_str = str(request.form['DOB'])  
        yy , mm ,dd = date_str[:4] , date_str[5:7] , date_str[8:10]
        dob = datetime(int(yy), int(mm), int(dd))
        status = request.form['Status']  
        prof = Prof.query.filter_by(sno=sno).first()
        prof.name = name
        prof.dob = dob
        prof.status = status
        db.session.add(prof)
        db.session.commit()
        return redirect("/")
    prof = Prof.query.filter_by(sno=sno).first()
    return render_template("update.html",prof = prof)


@app.route('/delete/<int:sno>')
def delete(sno ):
    #print(request.method,'inside the delete')
    if True:
        prof = Prof.query.filter_by(sno=sno).first()
        db.session.delete(prof)
        db.session.commit()
    return redirect("/")

@app.route("/show")
def profiles():
    allProf = Prof.query.all()
    print(allProf)
    return 'this is profiles page'

# adding all the endpoints for the postman app
@app.route("/allProfiles",methods = ['GET'])
def show_all_profiles():
    allProf = Prof.query.all()
    i = 0
    js = []
    for pr in allProf:
        js.append([pr.sno,pr.name , pr.dob,pr.status])
        i+=1
    #print(allProd,js)
    return jsonify(js)

@app.route('/delete_prof/<int:sno>' , methods=["DELETE"])
def delete_a_profile(sno):
    #print(request.method,'inside the delete')
    if request.method == 'DELETE':
        prof = Prof.query.filter_by(sno=sno).first()
        db.session.delete(prof)
        db.session.commit()
    return str("deleted : " + prof.name   )

'''
@app.route("/update_profile/<int:sno>,<string:name>,<string:dob>,<string:status> ",methods = ['PUT'])
def update_profile(sno,name,dob,status):
    if request.method == 'PUT':
        #name = request.form['Prof_Name']
        date_str = str(dob)  
        yy , mm ,dd = date_str[:4] , date_str[5:7] , date_str[8:10]
        DOB = datetime(int(yy), int(mm), int(dd))
        status = request.form['Status']  
        prof = Prof.query.filter_by(sno=sno).first()
        prof.name = name
        prof.dob = DOB
        prof.status = status
        db.session.add(prof)
        db.session.commit()
    return redirect("/")
    
'''

if __name__ == "__main__":
    app.run(debug=True, port = 8000)



