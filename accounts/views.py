from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import pickle
import numpy as np
from .models import Patient
import pandas as pd
def home(request):
    return render(request,'home.html')
def plogin(request):
    return render(request,'plogin.html')
def pcreate(request):
    return render(request,'pcreate.html')
@csrf_exempt
@login_required(login_url = '/')
def patient(request):
    list = Patient.objects.filter(payer=str(request.user.id))
    paginator = Paginator(list, 3)
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)
    return render(request,
                  'patient.html',
                  {
                      "list":list,
                      "paginator":paginator ,
                      "page_number":int(page_number),
                      "page_obj": page_obj,
                  })
def pcreatecheck(request):
    if request.method == 'POST':
        f_name = request.POST['f_name']
        s_name = request.POST['s_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "username taken")
                return redirect('pcreate')
            if User.objects.filter(email=email).exists():
                messages.info(request, "email taken")
                return redirect('dcreate')
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=f_name, last_name=s_name)
            user.save()
            print('user created')
            return redirect('home')
        else:
            messages.info(request, 'password not matching')
            return redirect('pcreate')
        return redirect("")
    return redirect('pcreate')
def plogincheck(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('patient')
        else:
            messages.info(request, "invalid credentials")
            return redirect('home')
    else:
        return redirect('home')
def plogout(request):
    auth.logout(request)
    return redirect('home')

def predict(request):
    if request.method=="POST":
        values = request.POST
        print(values)
        final=[]
        if values['a']=="Male":final.append(1)
        else:final.append(0)
        for ele in 'bcedfghijklmn':
            final.append(int(values[ele]))
        x=values['o']
        if x=="AfricanAmerican":
            final.extend([1,0,0,0])
        elif x=="Asian":
            final.extend([0,1,0,0])
        elif x=="Caucasian":
            final.extend([0,0,1,0])
        elif x=="Hispanic":
            final.extend([0,0,0,1])
        else:
            final.extend([0,0,0,0])
        final = [np.array(final)]
        print(final,len(final[0]))
        print("name of docter is :",request.user.username)
        model = pickle.load(open("accounts\\model.pkl", 'rb'))
        prediction = model.predict_proba(final)
        output = float("{0:.2f}".format(prediction[0][1]))
        print(output)
        if output>0.5:
            report="Your Adherence levels are GOOD \n LEVELS:{}".format(output)
        else:
            report = "Your Adherence levels are LOW \n LEVELS:{}".format(output)
        return render(request,"patient.html",{'report':report})

def createpatient(request):
    #print("1")
    if request.method=="POST":
        #print(2)
        f = request.POST["b"]
        l = request.POST["c"]
        email = request.POST["d"]
        contact = request.POST["e"]
        age = request.POST["f"]
        gender = request.POST["g"]
        blood = request.POST["h"]
        emergency = request.POST["i"]
        address = request.POST["j"]
        town = request.POST["k"]
        zip = request.POST["l"]

        patient = Patient(blood=blood,emergency=emergency,address=address,town=town,zipcode=zip,
                          first=f,last=l,email=email,contact=contact,age = age,gender = gender,payer=request.user.id,
                          medical=100,treatment=100,total=100)
        patient.save()
    context = Patient.objects.filter(payer=str(request.user.id))
    print(context)
    return render(request, "patient.html", {"list": context})

class Update:
    def __init__(self):

        #load model,dataset
        model = pickle.load(open("accounts/model.pkl", "rb"))
        df = pd.read_csv("accounts/iotDATA.csv", encoding='latin1')

        # for each patient
        for ID, frame in df.groupby(["patient_id"]):
            x = frame.iloc[:, 2:9].mean() # slice required cols
            treatment = model.predict_proba([x])[0][1] # prediction
            one = zero = 0

            # count zeros and ones
            for row in range(frame.shape[0]):
                for col in range(9,18):
                    val = frame.iloc[row, col]
                    if val == 0: zero += 1
                    if val == 1: one += 1

            #calculate final value
            medical = one/(one+zero)
            total = (medical+treatment)/2

            # update results
            pat_id = ID
            pat = Patient.objects.get(pk=ID)
            pat.medical = int(medical*100)
            pat.treatment = int(treatment*100)
            pat.total = int(total*100)
            pat.save()

def details(request,pat_id):
    pat = Patient.objects.get(pk=pat_id)
    df = pd.read_csv("accounts/iotDATA.csv",encoding='latin1')
    df = df[df["patient_id"]==pat_id]
    steps = []
    fast = list(df['fasting_blood sugar'])
    random = list(df.Random_blood_sugar)
    pulse = list(df.pulse_rate)
    Diastolic = list(df["Diastolic Pressure"])
    Systolic = list(df["Systolic Pressure"])
    df1 = df.iloc[:,9:18]
    rows = df.shape[0]
    med=[0]
    treatment = [0]
    model = pickle.load(open("accounts/ml_model.pkl", "rb"))
    for i in range(0,rows,7):
        j = min(rows, i+7)
        steps.append(df.step_count.iloc[i:j].mean())
        x = df.iloc[i:j,2:9].mean()
        #print(x)
        pred = model.predict_proba([x])
        #print(pred)
        treatment.append(int(pred[0][1]*100))
        ones=zeros=0
        for row in range(i,j):
            for col in range(9):
                val = df1.iloc[row,col]
                if val==0:zeros+=1
                if val==1:ones+=1
        med.append((100*ones)//(ones+zeros))
    meds = list(range(len(med)))
    steplabels = meds[1:]

    return render(request, "chart.html", {"labels":list(range(len(fast))), "Diastolic":Diastolic,"Systolic":Systolic,
                                          "pat":pat,"steps":steps,"fast":fast,"random":random,"pulse":pulse,
                                          "med":med, "meds":meds, 'steplabels':steplabels, 'treatment':treatment})

def search(request):
    if request.method=="POST":
        target = request.POST["target"]
        try:
            list=Patient.objects.filter(pk=target,payer=str(request.user.id))
        except:
            list=Patient.objects.filter(payer=str(request.user.id),first=str(target))
        print(list)
        paginator = Paginator(list, 3)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.page(page_number)
        return render(request,
                      'patient.html',
                      {
                          "list": list,
                          "paginator": paginator,
                          "page_number": int(page_number),
                          "page_obj": page_obj,
                      })






