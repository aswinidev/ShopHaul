from django.http.response import HttpResponseRedirect
import mysql.connector
from operator import itemgetter
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from shophaul.models import UserRegistration
from django.contrib import messages
from django.contrib.auth import logout,authenticate, login

# Create your views here.
def userReg(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('Fname') and request.POST.get('Lname') and request.POST.get('address') and request.POST.get('contact_no') and request.POST.get('pswrd'):
            saverecord = UserRegistration()
            saverecord.username = request.POST.get('username')
            saverecord.Fname = request.POST.get('Fname')
            saverecord.Lname = request.POST.get('Lname')
            saverecord.address = request.POST.get('address')
            saverecord.contact_no = request.POST.get('contact_no')
            saverecord.pswrd = request.POST.get('pswrd')
            saverecord.save()
            messages.success(request,"User Registered Successfully..!!")
            return render(request,'register.html')
    else :
        return render(request,'register.html')

def index(request):
    if request.user.is_anonymous:
        return redirect("/login")

    return HttpResponse('This is Homepage')

def login(request):
    con = mysql.connector.connect(host="localhost",user="shophaul",password="shophaul",database="shophaul")
    cursor = con.cursor()
    con2 = mysql.connector.connect(host="localhost",user="shophaul",password="shophaul",database="shophaul")
    cursor2 = con2.cursor()
    sqlcommand = "select username from Seller_info"
    sqlcommand2 = "select pswrd from Seller_info"
    cursor.execute(sqlcommand)
    cursor2.execute(sqlcommand2)
    e=[]
    p=[]
    for i in cursor:
        e.append(i)
    for j in cursor2:
        p.append(j)
    res = list(map(itemgetter(0),e))
    res2 = list(map(itemgetter(0),e))
    
    if request.method=="POST":
        username = request.POST['username']
        pswrd = request.POST['pswrd']
        i=1
        k=len(res)
        while i<k:
            if res[i]==username and res2[i]==pswrd:
                messages.info(request,"Hello..{username} u r logged in!!")
                return render(request,'home.html',{'username':username})
                break
            i+=1
        else:
            messages.info(request,"Check username or password")
            return redirect('login')
    return render(request,"login.html")


    