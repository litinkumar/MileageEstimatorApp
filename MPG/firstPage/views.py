from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.
import joblib

loadmodel = joblib.load('./Models/ModelRF.pkl')

from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client['mpgDatabase']
collectionD=db['mpgTable']

def index(request):
    temp={}
    temp['Cylinders']=8
    temp['Displacement']=307
    temp['Horsepower']=130
    temp['Weight']=3504
    temp['Accelration']=12
    temp['Model']=70
    temp['Origin']=1
    context={'temp':temp}
    return render(request,'index.html',context)
    #return HttpResponse({'a':1})

def predictMPG(request):
    if request.method == 'POST':
        temp={}
        temp['Cylinders']=request.POST.get('cylinderVal')
        temp['Displacement']=request.POST.get('dispVal')
        temp['Horsepower']=request.POST.get('hrsPwrVal')
        temp['Weight']=request.POST.get('weightVal')
        temp['Accelration']=request.POST.get('accVal')
        temp['Model']=request.POST.get('modelVal')
        temp['Origin']=request.POST.get('originVal')

    testData=pd.DataFrame({'x':temp}).transpose()
    scoreVal=loadmodel.predict(testData)[0]
    context = {'scoreVal':scoreVal,'temp':temp}
    return render(request,'index.html',context)

def viewDatabase(request):
    countRow=collectionD.find().count()
    context={'countRow':countRow}
    return render(request,'viewDB.html',context)

def updateDatabase(request):
    temp={}
    temp['Cylinders']=request.POST.get('cylinderVal')
    temp['Displacement']=request.POST.get('dispVal')
    temp['Horsepower']=request.POST.get('hrsPwrVal')
    temp['Weight']=request.POST.get('weightVal')
    temp['Accelration']=request.POST.get('accVal')
    temp['Model']=request.POST.get('modelVal')
    temp['Origin']=request.POST.get('originVal')
    temp['mpg']=request.POST.get('mpgVal')
    collectionD.insert_one(temp)
    countRow=collectionD.find().count()
    context={'countRow':countRow}
    return render(request,'viewDB.html',context)