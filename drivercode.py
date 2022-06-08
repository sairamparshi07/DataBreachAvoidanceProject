# MyBankCardManager , manage all your bank cards at one place :)
# Note : Before running this, make sure MongoDB Server is active

#--------------------------------------------------------------------------

DBACredentrials=["DBA707","Mercury80"]

MongoDB_Databasename="MyBankCardsManagerDB"
Original_database_name="Original"
Honeypot_database_name="SuperOriginal"
port=7000



#---------------------------------------------------------------------------

#- - - - - -
def install(package):
    # This function will install a package if it is not present
    from importlib import import_module
    try:
        import_module(package)
    except:
        from sys import executable as se
        from subprocess import check_call
        check_call([se,'-m','pip','-q','install',package])


for package in ['flask','pymongo','time','pathlib']:
    install(package)
#- - - - - -
    
from flask import *
import pymongo
import time
from pathlib import Path

# Global Variables

app=Flask(__name__) 

GenuineDBA=True
FailCount=0
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
dblist = myclient.list_database_names()
original=[]
superoriginal=[]
makeinaccessable=False
mystr=""

def ComputeOriginal():
    myworkingdatabase=0
    if MongoDB_Databasename in dblist:
        myworkingdatabase=myclient[MongoDB_Databasename]
        myoriginalcollection=myworkingdatabase[Original_database_name]
        for record in myoriginalcollection.find():
            record=str(record)
            x=record.split(',')
            x[-1]=x[-1].replace('}','')
            del x[0]
            z=""
            for i in x:
                z+=i
            original.append(z)
def ComputeSuperOriginal():
    myworkingdatabase=0
    if MongoDB_Databasename in dblist:
        myworkingdatabase=myclient[MongoDB_Databasename]
        mysuperoriginalcollection=myworkingdatabase[Honeypot_database_name]
        for record in mysuperoriginalcollection.find():
            record=str(record)
            x=record.split(',')
            x[-1]=x[-1].replace('}','')
            del x[0]
            z=""
            for i in x:
                z+=i
            superoriginal.append(z)

    
        
@app.route('/MyBankCardsManager') #ONE
def fun1():
    time.sleep(1)
    FailCount==0
    GenuineDBA=True
    return render_template("1.EntryPage.html")


@app.route('/MyBankCardsManager/ThisIsDBA') #TWO
def home():
    time.sleep(1)
    FailCount==0
    GenuineDBA=True
    return render_template("2.AuthenticateDBA.html")


@app.route('/MyBankCardsManager/AuthenticateAgain') #THREE
def home2():
    time.sleep(1)
    return render_template("3.AuthenticateAgain.html")


@app.route('/MyBankCardsManager/DBAMenu') #Four
def home3():
    time.sleep(1)
    return render_template("4.DBAMenu.html")

@app.route('/MyBankCardsManager/ProcessDBAdata',methods = ['GET'])
def processthedata():
    DBACode=request.args.get('DBACode')  
    Password=request.args.get('Password')
    global FailCount
    global GenuineDBA
    if str(DBACode)==DBACredentrials[0]:
        if str(Password)==DBACredentrials[1]:
            if FailCount==0 or FailCount==1:
                GenuineDBA=True
            return redirect("http://localhost:7000/MyBankCardsManager/DBAMenu")
        else:
            FailCount+=1
            
            if FailCount==3:
                GenuineDBA=False
                return redirect("http://localhost:7000/MyBankCardsManager/DBAMenu")
            
            return redirect("http://localhost:7000/MyBankCardsManager/AuthenticateAgain")
    else:
        FailCount+=1
        if FailCount==3:
            GenuineDBA=False
            return redirect("http://localhost:7000/MyBankCardsManager/DBAMenu")
        return redirect("http://localhost:7000/MyBankCardsManager/AuthenticateAgain")


@app.route('/MyBankCardsManager/DBAMenu/DropDB') # FIVE
def DropDB():
    global original
    global superoriginal
    time.sleep(2)
    original=['Database made inaccessible']
    superoriginal=['NULL, 0 records selected']
    return "<h1>Dropped the database</h1>"
@app.route('/MyBankCardsManager/DBAMenu/AddEntry') # SIX
def AddEntry():
    time.sleep(1)
    return render_template("6.AddEntry.html")

@app.route('/MyBankCardsManager/DBAMenu/ViewDatabase') # Seven
def ViewDatabase():
    time.sleep(1)
    global makeinaccessable
    global mystr
    mystr=''
    temp=''
    if GenuineDBA==True:
        
        mystr="<h1> ORIGINAL DATABASE </h1><br>"
        mystr+="<h5>"
        for i in original:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        if makeinaccessable:
            return "<h1> Database InAccessable!! </h1>"
        return temp
        
    else:
        mystr="<h1> HONEYPOT DATABASE </h1><br>"
        mystr+="<h5>"
        for i in superoriginal:
            mystr+=str(i)
            mystr+="<br>"
        mystr+="</h5>"
        temp=mystr
        mystr=""
        makeinaccessable=True
        return temp

@app.route('/MyBankCardsManager/DBAMenu/DownloadDB')
def DownloadDB():
    time.sleep(1)
    downloads_path = str(Path.home() / "Downloads")
    #return str(downloads_path)
    #return 'hello'
    p=downloads_path.replace('\\','/')
    print(p)
    p+='/MyBankCardsManagerDatabase.txt'
    d=open(p,'w')
    data=[]
    if GenuineDBA:
        data=original+[]
    else:
        data=superoriginal+[]
    for i in data:
        i=str(i)+'\n'
        d.write(i)

    d.close()
    
    
    if GenuineDBA:
        return "<h1>Database Downloaded</h1>"
    else:
        return "<h1>Database Downloaded</h1>"
@app.route('/MyBankCardsManager/DBAMenu/AddEntryData',methods=['GET'])
def AddEntryData():
    time.sleep(1)
    CName=request.args.get('CName')
    CNumber=request.args.get('CNum')
    CExpiry=request.args.get('CExpiry')
    CCVV=request.args.get('CCVV')
    record={'username':'DBA707', 'CardName':str(CName), 'CardNumber':str(CNumber), 'Expiry':str(CExpiry), 'CVV':str(CCVV)}
    record=str(record)
    x=record.split(',')
    x[-1]=x[-1].replace('}','')
    x[0]=x[0].replace('{','')
    z=""
    for i in x:
        z+=i    
    if GenuineDBA:
        original.append(z)
    else:
        superoriginal.append(z)
    return render_template("9.EntrySuccessful.html")
    
def DBADone():
    return render_template("DBADone.html")
if __name__ =='__main__':
    ComputeOriginal()
    ComputeSuperOriginal()
    print("To access application, go to:","http://127.0.0.1:"+str(port)+"/MyBankCardsManager\n\n\nServer Traffic and other details:\n")
    app.run(host="localhost", port=port,debug = True)

    
