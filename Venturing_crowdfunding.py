from flask import Flask,render_template,request,session

from dbconnection import Db

app = Flask(__name__)
app.secret_key="kk"

@app.route('/')
def launch():
    return render_template('launch_index.html')


@app.route('/login')
def login():
    return render_template('log_index.html')

@app.route('/login_post',methods=["post"])
def login_post():
    uname=request.form["textfield"]
    password=request.form["textfield2"]
    q="select * from `login` where `Username`='"+uname+"' and `Password`='"+password+"'"
    d=Db()
    res=d.selectOne(q)
    if res!=None:
        session["lid"] = res["LId"]
        session["pass"] = password
        if res["Type"]=="admin":
            return '''<script>alert('Success');window.location='/admin_panel'</script>'''
        elif(res["Type"]=="user"):
            return '''<script>alert('Success');window.location='/home2'</script>'''

        else:
            return '''<script>alert('Invalid User');window.location='/login'</script>'''
    else:
        return '''<script>alert('Invalid User');window.location='/login'</script>'''


@app.route('/home')
def homr():
    return render_template('/admin/home.html')
@app.route('/admin_panel')
def admin_panel():
    return  render_template('/admin/admin_panel.html')
@app.route('/chngepsswrd')
def chngepsswrd():
    return render_template('/admin/Changepassword.html')
@app.route('/chngepsswrd_post',methods=["post"])
def chngepsswrd_post():
    current=request.form["textfield"]
    renew=request.form["textfield3"]
    if(current==session["pass"]):
        q="UPDATE `login` SET `Password`='"+renew+"' WHERE `LId`='"+str(session["lid"])+"'"
        d=Db()
        r=d.update(q)
    return login()

@app.route('/complaint')
def complaint():
    d=Db()
    q="SELECT `complaint`.*,`user`.`Name`,`user`.`Email`,`user`.Phone FROM `complaint` INNER JOIN `user` ON `complaint`.`ULId`=`user`.`ULId`"
    res=d.select(q)
    return render_template('/admin/Complaint.html',res=res)
@app.route('/complaint_upto',methods=["post"])
def complaint_upto():
    date1=request.form['date1']
    date2=request.form['date2']
    d=Db()
    q = "SELECT `complaint`.*,`user`.`Name`,`user`.`Email`,`user`.Phone FROM `complaint` INNER JOIN `user` ON `complaint`.`ULId`=`user`.`ULId` where `Complaint`.date BETWEEN '"+date1+"' and '"+date2+"'"
    res=d.select(q)
    return render_template("admin/Complaint.html", res=res)

@app.route('/reply/<CId>')
def rep(CId):
    d=Db()
    q = "SELECT `complaint`.*,`user`.`Name`,`user`.`Email`,`user`.Phone FROM `complaint` INNER JOIN `user` ON `complaint`.`ULId`=`user`.`ULId` WHERE complaint.CId='"+CId+"'"
    res = d.selectOne(q)
    return render_template('/admin/Replay.html',data=res)
@app.route('/replay_post',methods=["post"])
def replay_post():
    replay=request.form["com"]
    cid=request.form["cid"]
    d=Db()
    q="UPDATE `complaint` set Reply='"+replay+"',Status='Replied' where CId='"+cid+"'"
    r=d.update(q)
    return complaint()

@app.route('/crowdfunding')
def crwd():
    return render_template('/admin/crowdfunding form.html')
@app.route('/crowdfunding_post',methods=["post"])
def crowdfunding_post():
    bname=request.form["textfield"]
    address=request.form["textfield2"]
    city=request.form["textfield3"]
    email=request.form["textfield4"]
    website = request.form["textfield5"]
    phone = request.form["textfield6"]
    chck_one = request.form["RadioGroup1"]
    date=request.form["textfield8"]
    amount = request.form["textfield9"]
    des = request.form["textfield10"]
    db=Db()
    qry="INSERT INTO `crowdfunding_request`(`Buisness Name`,`Address`,`City`,`Email`,`Website`,`Phone`,`Check_One`,`Date`,`Amount`,`Description`)VALUES('"+bname+"','"+address+"','"+city+"','"+email+"','"+website+"','"+phone+"','"+chck_one+"','"+date+"','"+amount+"','"+des+"')"
    res=db.insert(qry)
    return "Ok"

@app.route('/registered')
def reg():
    d=Db()
    q="select * from user"
    r=d.select(q)
    return render_template('/admin/registered user.html',r=r)


@app.route('/response')
def response():
    return render_template('/admin/User Response.html')

@app.route('/viewcrwd')
def view_crwd():
    d=Db()
    que="select * from crowdfunding_request"
    res=d.select(que)
    return render_template('/admin/view crowdfunding form.html',res=res)

@app.route('/admin_delete_crwd_funding/<rid>')
def admin_delete_crwd_funding(rid):
    q="DELETE FROM `crowdfunding_request` WHERE `ReqNo`='"+rid+"'"
    d=Db()
    res=d.delete(q)
    return "<script>alert('Success');window.location='/viewcrwd'</script>"

@app.route('/crwdfunding_form_edit/<rid>')
def crwdfunding_form_edit(rid):
    q="SELECT * FROM `crowdfunding_request` WHERE ReqNo='"+rid+"'"
    d=Db()
    r=d.selectOne(q)
    return render_template('/admin/crowdfunding form_edit.html',r=r)
@app.route('/crwdfunding_form_edit_post',methods=['post'])
def crwdfunding_form_edit_post():
    bname1 = request.form["textfield"]
    address1 = request.form["textfield2"]
    city1 = request.form["textfield3"]
    email1 = request.form["textfield4"]
    website1 = request.form["textfield5"]
    phone1 = request.form["textfield6"]
    chck_one1 = request.form["RadioGroup1"]
    date1 = request.form["textfield8"]
    amount1 = request.form["textfield9"]
    des1 = request.form["textfield10"]
    reqno=request.form["ReqNo"]
    d=Db()
    q="UPDATE `crowdfunding_request` SET `Buisness Name`='"+bname1+"',`Address`='"+address1+"',`City`='"+city1+"',`Email`='"+email1+"',`Website`='"+website1+"',`Phone`='"+phone1+"',`Check_One`='"+chck_one1+"',`Date`='"+date1+"',`Amount`='"+amount1+"',`Description`='"+des1+"' WHERE `ReqNo`='"+reqno+"'"
    r=d.update(q)
    return view_crwd()

@app.route('/reguser')
def reguser():
    return render_template('user/user part registeration.html')
@app.route('/reguser_post',methods=["post"])
def reguserpost():
    name=request.form["textfield"]
    place=request.form["textfield2"]
    post = request.form["textfield3"]
    pin=request.form["textfield4"]
    phone=request.form["textfield5"]
    email=request.form["textfield6"]
    psswrd=request.form["textfield7"]
    new=request.form['textfield8']
    img=request.files["textfield9"]

    path="C:\\Users\\BEST\\PycharmProjects\\Venturing_crowdfunding\\static\\user_image\\"
    img.save(path+img.filename)
    p="/static/user_image/"+img.filename


    qry="INSERT INTO `login`(`Username`,`Password`,`Type`) VALUES('"+email+"','"+psswrd+"','user')"
    d=Db()
    res=d.insert(qry)
    qry1="INSERT INTO `user`(`Name`,`Place`,`Post`,`Pin`,`Phone`,`Email`,`ULId`,`Img`) VALUES ('"+name+"','"+place+"','"+post+"','"+pin+"','"+phone+"','"+email+"','"+str(res)+"','"+p+"')"
    d.insert(qry1)

    return "<script>alert('Success');window.location='/'</script>"
@app.route('/home2')
def home():
    return render_template('user/home.html')
    return "ok"
@app.route('/complaintsend')
def complaintsend():
    return render_template('user/complaint_sent.html')

@app.route('/complaintsend_post',methods=["post"])
def complaintsend_post():
    complaint=request.form["txt"]
    d=Db()
    q="INSERT INTO `complaint`(`ULId`,`Complaint`,`Reply`,`date`,`Status`) VALUES ('"+str(session['lid'])+"','"+complaint+"','',curdate(),'pending')"

    print(q)
    res = d.insert(q)
    print(res)
    return 'ok'
@app.route('/viewreply')
def viewreply():
    d=Db()
    q="SELECT * FROM `complaint` WHERE `ULId`='"+str(session['lid'])+"'"
    res=d.select(q)
    return render_template('user/view_reply.html',res=res)
@app.route('/viewreply_post',methods=["post"])
def viewreply_post():
    d1 = request.form['d1']
    d2 = request.form['d2']
    d = Db()
    q="SELECT * FROM `complaint` WHERE `ULId`='"+str(session['lid'])+"' AND `date` BETWEEN '"+d1+"' AND '"+d2+"'"
    res = d.select(q)
    return render_template("user/view_reply.html", res=res)

@app.route('/viewcrowdfnd_user')
def viewcrowdfnd_user():
    d = Db()
    que = "select * from crowdfunding_request"
    res = d.select(que)
    return render_template('user/view crowdfunding form.html', res=res)

if __name__ == '__main__':
    app.run(debug=True)
