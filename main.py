import csv
import os
import random
from datetime import date, timedelta
import re
from difflib import SequenceMatcher
from random import randint, randrange
import uuid
from datetime import datetime
from urllib import request
import pymysql
from werkzeug.utils import secure_filename
import socket
import ar_master
import smtplib, ssl
from flask import Flask, render_template, request, session, Response, current_app, send_from_directory, redirect,url_for
mm = ar_master.master_flask_code()
app = Flask(__name__, static_folder='static',template_folder='templates',static_url_path='/static')
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
@app.route("/")
def homepage():
    return render_template('index.html')

@app.route("/user_login", methods = ['GET', 'POST'])
def user_login():
     return render_template('user_login.html')

@app.route("/user_login2/<string:name>/<string:password>", methods = ['GET', 'POST'])
def user_login1(name,password):
    session['qid']=0
    if 1 == 1:
        n = name
        g = password
        q = ("SELECT * from user_details where name='" + str(n) + "' and password='" + str(g) + "'")
        print(q)
        data = mm.select_direct_query(q)
        data1 = len(data)
        if data1 == 0:
            return redirect(url_for('homepage'))
        else:
            session['user'] = n
            session['bmi'] = str(data[0][6])
            session['bmi_type'] = str(data[0][7])
            session['height'] = str(data[0][8])
            session['weight'] = str(data[0][9])
            session['fat'] = str(data[0][11])
            session['fat_count'] = str(data[0][12])
            return redirect(url_for('user_home'))
    return homepage()

@app.route("/user_home")
def user_home():
    question=['What is your age','Are you working or studying'
        ,'What type of work you do'
        ,'How many days in a week you work/study'
        ,'How many hours you utilize your energy'
        ,'What is your favourite food '
        ,'what is your favourite drinks'
        ,'Food you dislike'
        ,'Food that might be allergic to you']
    user=session['user']
    bmi=session['bmi']
    bmi_type=session['bmi_type']
    height=session['height']
    weight=session['weight']
    fat=float(session['fat'])
    fat_count=float(session['fat_count'])
    if fat!=0:
        predict_fat = float(fat / fat_count)
    else:
        predict_fat = 1
    predict_img="unpredicted"#str(bmi_type).lower()
    info="loading..."
    bmi_type=str(bmi_type).lower()
    if predict_fat<16:
        if bmi_type=="underweight":
            predict_img="underweight"
            info="Make a Nutritious Food Diet"

        elif bmi_type=="normal":
            predict_img="underweight"
            info = "Please Be Aware Your Loosing"

        elif bmi_type=="overweight":
            predict_img="normal"
            info = "Good You are fit now carry on with this food diet"

        elif bmi_type=="obesity":
            predict_img="overweight"
            info = "Still more on your mile stone carry on your recommended food diet"
    else:
        if predict_fat >= 16:
            if bmi_type == "underweight":
                predict_img = "normal"
                info = "Correct and balanced diet achieved"

            elif bmi_type == "normal":
                predict_img = "overweight"
                info = "Its not good please be on the recommeded food diet"

            elif bmi_type == "overweight":
                predict_img = "obesity"
                info = "OOPS be aware your leading to high range please be on a normal stand"

            elif bmi_type == "obesity":
                predict_img = "obesity"
                info = "Kindly follow the footstep of nutritous food recommendation"

    print(predict_fat,bmi_type,predict_img)



    check_self_assessment=mm.select_direct_query("select * from user_self_assessment where username='"+str(user)+"'")
    check_len_self_assessment=len(check_self_assessment)
    # print(check_len_self_assessment)
    if int(check_len_self_assessment)<9:
        qstn_id=int(session['qid'])
        qstn=question[qstn_id]
        print(check_len_self_assessment,qstn_id,qstn)
        session["qid"]=qstn_id
        session["qstn"]=qstn
        return redirect(url_for('user_home_self_assessment'))
    return render_template('user_home.html',bmi=bmi,type=bmi_type,height=height,weight=weight,predict_fat=predict_fat,predict_img=predict_img,info=info)


@app.route("/user_home_self_assessment")
def user_home_self_assessment():
    # user = session['user']
    qstn_id=session["qid"]
    qstn=session["qstn"]
    # print( qstn_id, qstn)
    return render_template('user_home_self_assessment.html',qstn_id=qstn_id,qstn=qstn)




@app.route("/user_home_self_assessment1", methods = ['GET', 'POST'])
def user_home_self_assessment1():
    if request.method == 'POST':
        user = session['user']
        qstn_id = session["qid"]
        qstn = session["qstn"]
        answer = request.form['answer']
        maxin=mm.find_max_id("user_self_assessment")
        mm.insert_query("insert into user_self_assessment values('"+str(maxin)+"','"+str(user)+"','"+str(qstn_id)+"','"+str(qstn)+"','"+str(answer)+"','0','0')")
        tmp=int(qstn_id)
        tmp+=1
        session["qid"]=str(tmp)
    return redirect(url_for('user_home'))


@app.route("/user_bmi")
def user_bmi():
    return render_template('user_bmi.html')

@app.route("/user_bmi1", methods=['GET', 'POST'])
def user_bmi1():
    if request.method == 'POST':
        user=session['user']
        height = int(request.form['height'])
        weight = int(request.form['weight'])
        height_m = height / 100
        bmi = weight / (height_m ** 2)
        type='Normal'
        if bmi < 18.5:
            type="Underweight"
        elif bmi >= 18.5 and bmi < 25:
            type="Normal"
        elif bmi >= 25 and bmi < 30:
            type="Overweight"
        else:
            type="Obese"
        mm.insert_query("update   user_details set bmi='"+str(bmi)+"',bmi_type='"+str(type)+"',height='"+str(height)+"',weight='"+str(weight)+"' where name='"+str(user)+"'")
        session['bmi']=str(bmi)
        session['bmi_type']=str(type)
        session['height']=str(height)
        session['weight']=str(weight)
        return render_template('user_bmi.html',height=height,weight=weight,bmi=bmi,type=type)
    return render_template('user_bmi.html')


@app.route("/user_register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        maxin = mm.find_max_id("user_details")
        qq = "insert into user_details values('" + str(maxin) + "','" + str(name) + "','" + str(contact) + "','" + str(
            email) + "','" + str(address) + "','" + str(password) + "','-','-','-','-','-','0','0')"
        result = mm.insert_query(qq)
        if (result == 1):
            return render_template('user_login.html',flash_message=True,data="Success")
        else:
            return render_template('user_register.html')
    else:
        return render_template('user_register.html')
    return render_template('user_register.html')

def recomed_food_list(interval,food,quantity):


    file="nutrition.csv"
    caloties="0"
    cholesterol="0"
    protein=0
    carbohydrate="0"
    fat="0"
    water="0"
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            t1 = row['name']
            t2 = row['calories']
            t3 = row['cholesterol']
            t4 = row['protein']
            t5 = row['carbohydrate']
            t6 = row['fat']
            t7 = row['water']
            if food.lower() in t1.lower():
                caloties=t2
                cholesterol=t3
                protein=t4
                carbohydrate=t5
                fat=t6
                water=t7

                caloties=caloties.replace("mg","")
                cholesterol=cholesterol.replace("mg","")
                protein=protein.replace("mg","")
                carbohydrate=carbohydrate.replace("mg","")
                fat=fat.replace("mg","")
                water=water.replace("mg","")

                caloties=caloties.replace("g", "")
                cholesterol=cholesterol.replace("g", "")
                protein=protein.replace("g", "")
                carbohydrate=carbohydrate.replace("g", "")
                fat=fat.replace("g", "")
                water=water.replace("g", "")
                break
        if caloties!="0":
            data_quantity=100
            total_quantity=float(quantity)

            total_caloties = float(caloties)/data_quantity
            total_cholesterol = float(cholesterol)/data_quantity
            total_protein = float(protein)/data_quantity
            total_carbohydrate = float(carbohydrate)/data_quantity
            total_fat = float(fat)/data_quantity
            total_water = float(water)/data_quantity

            total_caloties=(total_caloties*total_quantity)/100
            total_cholesterol=(total_cholesterol*total_quantity)/100
            total_protein=(total_protein*total_quantity)/100
            total_carbohydrate=(total_carbohydrate*total_quantity)/100
            total_fat=(total_fat*total_quantity)/100
            total_water=(total_water*total_quantity)/100
        print(total_caloties,total_cholesterol,total_protein,total_carbohydrate,total_fat,total_water)
        return total_caloties,total_cholesterol,total_protein,total_carbohydrate,total_fat,total_water






def food_list(fat):
    file = "nutrition.csv"
    input=float(fat)
    type = "reduce"
    if input<=16:
        type = "increase"

    ar_list=[]

    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            t1 = row['name']
            t6 = row['fat']
            tmp = str(t6)
            tmp = tmp.replace("mg", "")
            tmp = tmp.replace("g", "")
            fat=float(tmp)


            if type=="increase":
                if fat>16:
                    ar_list.append(t1)
            else:
                if fat<=16:
                    ar_list.append(t1)

    return ar_list




@app.route("/user_food_analysis", methods=['GET', 'POST'])
def user_food_analysis():
    user = session['user']
    bmi=session['bmi']
    bmi_type=session['bmi_type']
    height=session['height']
    weight=session['weight']
    remove_food_list=[]
    qry="select * from user_self_assessment where username='"+str(user)+"' and qid IN('7','8')"
    data=mm.select_direct_query(qry)
    for x in data:
        d1=x[4]
        remove_food_list.append(d1)
    if request.method == 'POST':
        select = request.form['select']
        food_name = request.form['food_name']
        quantity = request.form['quantity']
        total_caloties,total_cholesterol,total_protein,total_carbohydrate,total_fat,total_water=recomed_food_list(select,food_name,quantity)

        update_data=mm.select_direct_query("select fat,fat_count from user_details where name='"+str(user)+"'")
        pre_fat=0
        pre_fat_count=0
        for y in update_data:
            pre_fat = float(y[0])
            pre_fat_count = y[1]
        pre_fat_count=int(pre_fat_count)
        pre_fat_count+=1
        predict_fat=(float(pre_fat)+float(total_fat))
        mm.insert_query("update user_details set fat='"+str(predict_fat)+"',fat_count='"+str(pre_fat_count)+"' where name='"+str(user)+"'")
        tmp=predict_fat/pre_fat_count
        result=food_list(tmp)
        random_result = random.choice(result)

        return render_template('user_food_analysis1.html',recommended=random_result,food_name=food_name,total_caloties=total_caloties,total_cholesterol=total_cholesterol
                               ,total_protein=total_protein,total_carbohydrate=total_carbohydrate,total_fat=total_fat,total_water=total_water)

    return render_template('user_food_analysis.html')



def generate_recommend_food_list(type):
    file = "recomendation_food.csv"
    breakfast=[]
    afternoon=[]
    night=[]

    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            t1 = row['interval']
            t2 = row['type']
            t3 = row['food_name']
            if type==t2:
                if t1=="breakfast":
                    breakfast.append(t3)
                elif t1=="afternoon":
                    afternoon.append(t3)
                elif t1=="night":
                    night.append(t3)
    return breakfast,afternoon,night





@app.route("/user_food_recommendation", methods = ['GET', 'POST'])
def user_food_recommendation():
    user = session['user']
    remove_food_list = []
    qry = "select * from user_self_assessment where username='" + str(user) + "' and qid IN('7','8')"
    data = mm.select_direct_query(qry)
    for x in data:
        d1 = str(x[4])
        d2=d1.split(",")
        for x in d2:
            remove_food_list.append(x)
    print(remove_food_list)
    day_order=["Monday", "Tuesday", "Wednesday", "Thursday",  "Friday","Saturday" , "Sunday"]
    if request.method == 'POST':
        select = request.form['select']
        breakfast,afternoon,night=generate_recommend_food_list(str(select))

        breakfast = [x for x in breakfast if (x not in remove_food_list)]
        afternoon = [x for x in afternoon if (x not in remove_food_list)]
        night = [x for x in night if (x not in remove_food_list)]

        count=7
        tmp_breakfast=random.sample(breakfast, count)
        tmp_afternoon=random.sample(afternoon, count)
        tmp_night=random.sample(night, count)
        i=0
        data=[]
        for x in range(7):
            a1=tmp_breakfast[x]
            a2=tmp_afternoon[x]
            a3=tmp_night[x]
            a0=day_order[x]
            tmp=[a0,a1,a2,a3]
            data.append(tmp)
        print(data)
        return render_template('user_food_recommendation.html',items=data)
    return render_template('user_food_recommendation.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True,port=4545)
