from django.shortcuts import render,redirect
from .models import Login,UserType
import smtplib
from email.message import EmailMessage
import ssl
from datetime import timedelta
from cryptography.fernet import Fernet

# Create your views here.

def home(request):
    try:
        request.session['id']=''
        request.session['user']=''
        request.session['name']=''
    except:
        pass
    if request.method == "POST":
        if 'EmployeeLogout' in request.POST:
            
            del request.session['id']
            del request.session['user']
            del request.session['name']
            return redirect('../')

        if 'login' in request.POST:
            typ=0
            
            user=request.POST.get('username')
            password=request.POST.get('password')
            print(user,password)
            task=Login.objects.filter(user_name=user,password=password,activation='Active')
            print(task,'task----------------------')
            if len(task)>0:
                

        
                
                usr=task[0].f_name
                typ=task[0].user_type
                id=task[0].id
                work_location=task[0].work_location
                request.session['id'] = id
                request.session['name'] = usr
                request.session['user'] = typ
                request.session['profile_pic']=str(task[0].image)
                print(work_location,'--------------------------------33333333333333333333333333333------------------------')
                request.session['work_location']=work_location

            else:
                try:
                    task=Login.objects.filter(user_name=user,activation='Active')
                    task=task[0]
                    encryptedpassword=task.password
                    
                    print(encryptedpassword)

                    key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
                    cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                    
                    decryptedpassword = (cipher_suite.decrypt(encryptedpassword))
                    print(decryptedpassword.decode())
                    if decryptedpassword.decode() == password:
                        usr=task.f_name
                        typ=task.user_type
                        id=task.id
                        work_location=task.work_location
                        request.session['id'] = id
                        request.session['name'] = usr
                        request.session['user'] = typ
                        request.session['profile_pic']=str(task.image)
                        request.session['work_location']=work_location
                except:
                    pass
                        
            if typ=='1':
                return redirect("hr/",{"id":id})
            elif typ=='2':
                return redirect("clientmanager/")
            elif typ=='3':
                return redirect("employee/")
            elif typ=='4':
                print('---------------',request.session['id'])
                return redirect("superadmin/")
            elif typ=='5':
                print('---------------',request.session['id'])
                return redirect("officemanager/")
            else:
                access=Login.objects.filter(user_name=user,activation='Deactive')
                if len(access )>0:
                    s='Access Denied !'
                else:
                    s='Enter Correct Username and Password'
                return render(request,'Login.html',{'s':s})
        if 'reset' in request.POST:
            email = request.POST.get('mail')
            email = request.POST.get('mail')
            reset = Login.objects.filter(email = email)
            if len(reset) > 0:
                name = reset[0].f_name
                user = reset[0].user_name
                pwd = reset[0].password
                try:
                    cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                    pwd = (cipher_suite.decrypt(pwd))
                    pwd=pwd.decode()
                except:
                    pass
                sender = 'ats.ariespro@gmail.com'
                receivers = email
                password = 'ahbfhcshjujvkgge'
                Subject= 'Reset Password'

                message = f"""
                Hi {name},

                

                Please Do Not Share:
                USER NAME: {user}
                PASSWORD: {pwd}
                
                "Please update your password after logging in with this password."

                Note: DO NOT REPLY TO THIS EMAIL. If you did not request this change, or if you believe you have received this email in error, please email at it.support@ariespro.com.

                Thank you,
                AriesPro Utilities
                """

                server=EmailMessage()

                server['From']='Ariespro'
                server['To']=receivers
                server['Subject']=Subject
                server.set_content(message)

                context=ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                    smtp.login(sender,password)
                    smtp.sendmail(sender,receivers,server.as_string())

              
                return render(request,'Login.html',{'message':'Check your mail'})
            else:
                return render(request,'Login.html',{'message':'Enter a valid Email Address'})
        else:
            return render(request,'Login.html')
    else:
        return render(request,'Login.html')

def test(request):
    return render(request,'test.html')
def logout(request):
    del request.session['id']
    del request.session['user']
    del request.session['name']
    return redirect('../')












    
        






    