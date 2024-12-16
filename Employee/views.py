from django.shortcuts import render
from ClientManager.models import Notifications,Ratings,Tasks,TasksChats,TasksLogs,TaskCrew ,PhaseVersion,TaskFiles,Versions
from Employee.models import Empdata,EmpLeaves,Activities
from HR.models import LeaveDetails
from mainlogin.models import Login
from datetime import datetime, timedelta,date
from datetime import datetime as dateTime
from django.http import HttpResponseRedirect,JsonResponse
from HR.models import ProjectDetails,Manager,Project_team,EmpDesk,LeaveDetails
import smtplib
from email.message import EmailMessage
from django.db.models import DateField, CharField,IntegerField,Subquery, OuterRef
import ssl
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear, Cast
from django.db.models import DateTimeField,FloatField,DateField,Sum
import time
from collections import defaultdict
from datetime import date
from datetime import timedelta
from cryptography.fernet import Fernet
from django.db.models import IntegerField
# Create your views here.


start_dates=datetime.now().date()
end_dates=datetime.now().date()
for i in range(8):
    if start_dates.weekday()==0:
        starts=start_dates
    else:
        start_dates=start_dates- timedelta(days=1, hours=0)
    if end_dates.weekday()==6:
        end_dts=end_dates
    else:
            end_dates=end_dates + timedelta(days=1, hours=0)
start_dates=starts
end_dates=end_dts

def weekdates():
    start_date=datetime.now().date()
    end_date=datetime.now().date()
    for i in range(8):
        if start_date.weekday()==0:
            starts=start_date
        else:
            start_date=start_date- timedelta(days=1, hours=0)
        if end_date.weekday()==6:
            end_dts=end_date
        else:
                end_date=end_date + timedelta(days=1, hours=0)
    start_date=starts
    end_date=end_dts
    # request.session['prev_date']=str(starts)
    # request.session['last_date']=str(end_dts)
    return(start_date,end_date)
def weekdates_2(request):
    start_date=datetime.now().date()
    end_date=datetime.now().date()
    for i in range(8):
        if start_date.weekday()==0:
            starts=start_date
        else:
            start_date=start_date- timedelta(days=1, hours=0)
        if end_date.weekday()==6:
            end_dts=end_date
        else:
                end_date=end_date + timedelta(days=1, hours=0)
    request.session['start_date']=str(starts)
    request.session['end_date']=str(end_dts)
    return(request.session['start_date'],request.session['end_date'])


def home(request):
    try:
        if request.session['user']=="3":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    

 
    if request.session['user']=="3":
        weekdates_2(request)
        global start_dates
        global end_dates
        
        
        notify = Notifications.objects.filter(emp='1',date=start_dates,emp_id=request.session['id'])
        notify = len(notify)

        start_dates=datetime.now().date()
        end_dates=datetime.now().date()
        for i in range(8):
            if start_dates.weekday()==0:
                starts=start_dates
            else:
                start_dates=start_dates- timedelta(days=1, hours=0)
            if end_dates.weekday()==6:
                end_dts=end_dates
            else:
                end_dates=end_dates + timedelta(days=1, hours=0)
                
        start_dates=starts
        end_dates=end_dts 
        # request.session['start_dates']=start_dates
        # request.session['end_dates']=end_dates
        
        login=Login.objects.filter(id=request.session['id'])
        login=login[0]
        passwordstatus=login.passwordstatus
        if request.method=='POST':
            pass
            
            
        if start_dates.weekday()==5:
            
            emp = Login.objects.filter(id=request.session['id'])
            email=emp[0].email
            sender = 'ats.ariespro@gmail.com'
            receivers = email
            password = 'ahbfhcshjujvkgge'
            Subject= 'Submit weekly timesheet'
            message = f"""
            Hi {request.session['name']},
            Please Submit Your TimeSheet by End of This Week.
                
            Note: DO NOT REPLY TO THIS EMAIL. If you did not request this change, or if youbelieve you have received this email in error, please email at it.support@ariespro.com.
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
            
        
        
        employee=EmpLeaves.objects.filter(emp_id=str(request.session['id']))
        notifs = []
        noti = []
        notif = Notifications.objects.filter(emp_id=str(request.session['id']),emp='1',date=start_dates)
        for i in notif:
            notifs.append(i)
        try:
            noti.append(notifs[-1])
        except:
            pass
        try:
            noti.append(notifs[-2])
        except:
            pass
        try:
            noti.append(notifs[-3])
        except:
            pass
        
        emp_id = [i.emp_id for i in noti]
        images_data = Login.objects.filter(id__in=emp_id).values('image')
        image = [i['image'] for i in images_data]
        noti = zip(noti,image)
        
        diff = []
        activity = Activities.objects.filter(emp_id = request.session['id'], date=start_dates)
        for i in activity:
            time = i.currentdate
            
            diff.append(time)
        activities = zip(activity,diff)    
        emp_id=request.session['id']
        bar=[]
        dash_data=Empdata.objects.filter(emp_id=emp_id,start=start_dates)
        
        for dash in dash_data:
            bar.append({'project':dash.project_name,'mon':dash.mon,'tue':dash.tue,'wed':dash.wed,'thu':dash.thu,'fri':dash.fri,'sat':dash.sat,'sun':dash.sun})
        leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
        print(bar,'bar')
        for i in bar:
            i
        remaining=leave_details[0].days_allowed
        taken=leave_details[0].taken
        name=request.session['name']
        current_month=date.today().month
        print(current_month,'current_month')
        emp_dash_data=Empdata.objects.annotate(start_month=Cast('start', output_field=DateTimeField())).filter(emp_id=request.session['id'],start_month__month=current_month,status='1' ,statushr=1)
        # emp_dash_data = Empdata.objects.annotate(start_month=Cast('start', output_field=DateTimeField())).filter(emp_id=request.session['id'], start_month__month=current_month).values('project_name').annotate(total_hours=Sum('mon') + Sum('tue') + Sum('wed') + Sum('thu') + Sum('fri') + Sum('sat'))
        emp_dash_=[]
        for i in emp_dash_data:
            data1=[]
            project=i.project_name
            hours_worked=i.total
            data1=[project,hours_worked]
            emp_dash_.append(data1)
        print(emp_dash_)
        project_hours = defaultdict(int)

        for project, hours in emp_dash_:
            project_hours[project] += int(hours)

        emp_dash_aggregated = [[project, hours] for project, hours in project_hours.items()]
        print(emp_dash_aggregated)
        emp_dash_=[]
        lef=[]
        rig=[]
        for i in emp_dash_aggregated:
            if i[0]=='0' or i[1]=='0' or i[1]==0 or i[0]==0:
                pass
            else:
                lef.append(i[0])
                rig.append(i[1])
                emp_dash_.append(i)
        emp_dash=zip(lef,rig)        
        print(emp_dash_,'emp_dash_')
        
        
        datas={'emp_dash_':emp_dash_,"name":name,'notify':notify,'passwordstatus':passwordstatus, 'taken':taken,'remaining':remaining,'leave':employee,"bar":bar,'noti':noti,'activity':activities,'project0': '', 'mon0': 0, 'tue0': 0, 'wed0': 0, 'thu0': 0, 'fri0': 0, 'sat0': 0, 'sun0': 0, 'project1': '', 'mon1': 0, 'tue1': 0, 'wed1': 0, 'thu1': 0, 'fri1': 0, 'sat1': 0, 'sun1': 0, 'project2': '', 'mon2': 0, 'tue1': 0, 'wed2': 0, 'thu2': 0, 'fri2': 0, 'sat2': 0, 'sun2': 0, 'project3': '', 'mon3': 0, 'tue3': 0, 'wed3': 0, 'thu3': 0, 'fri3': 0, 'sat3': 0, 'sun3': 0}
        for i in range(len(bar)):
            for keys,values in bar[i].items():
                if keys=="project":
                    datas[f"{keys}{i}"]=values 
                else:
                    try:
                        datas[f"{keys}{i}"]=int(values )
                    except:
                        datas[f"{keys}{i}"]=0
        verify=LeaveDetails.objects.filter(emp_id=request.session['id'])
        verify=verify[0]
        reset_date=verify.reset_date
        reset_date = datetime.strptime(reset_date, "%Y-%m-%d %H:%M:%S")
        today = datetime.now()
        print(today,reset_date)
        print(str(today-reset_date).split(' ')[0])
        try:
            deltas=int(str(today-reset_date).split(' ')[0] )  
        except:
              deltas=0   
        print(deltas)
        projectdetails=Project_team.objects.filter(employee_id=request.session['id'])
        hr_id=EmpDesk.objects.get(login_id=request.session['id']).hr_id
        manager_id=EmpDesk.objects.get(login_id=request.session['id']).manager_id
        # print(projectdetails)
        for i in projectdetails:
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=i.project,start=start_dates)
            if len(projectdata)>0:
                pass #print('projects alreaddy present in database')
            else:
                employeedata=Empdata(emp_id=request.session['id'],status=0,mon=0,tue=0,wed=0,thu=0,fri=0,sat=0,sun=0,total=0,totals=0,hr_id=hr_id, manager_id=manager_id, start=start_dates,end=end_dates,project_name=i.project,
                                     name=i.employee_name,statushr=0,date_created=datetime.now(),assigned='*')
                employeedata.save()
                # print('projects added to database')
        start_date,end_date=weekdates()
        # print(start_date,end_date,weekdates(),'weeklydatetimes')
        
        if deltas>=0:
            verify.reset_date=reset_date+timedelta(days=365)
            verify.save(update_fields=['reset_date'])
            verify.days_allowed=10
            verify.save(update_fields=['days_allowed'])
            verify.sick_day=3
            verify.save(update_fields=['sick_day'])
            
            verify.taken=0
            verify.save(update_fields=['taken'])
            verify.remaining=13
            verify.save(update_fields=['remaining'])
            
        return render(request,'Emp_dashboard.html',datas)
    
    else:
        s='enter credentials for Employee login'
        response=HttpResponseRedirect('../../')

        return response
# except:
#     s='enter credentials for Employee login '
#     response=HttpResponseRedirect('../../')
#     return response
        
def Emp_tracker(request):
    if True:
        if request.session['user']=="3":
            if request.method=='GET':
                weekdates_2(request)
            dates_for_filter = weekdates()
            manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
            hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
            print(manager_id,hr_id)
            # request.session['prev_date'] = 

            start_dates=request.session['start_date']
            end_dates=request.session['end_date']
            daystr=[]
            print(start_dates,'start_dates', end_dates,'end_dates')
            daystrr=[]
            sickleaves=[]
            otherleaves=[]
            sun,tue,mond,wed,thu,fri,sat=0,0,0,0,0,0,0
            weektotal=0
            projectname,days=[],[]
            messages=''
            
            employee_data=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates)
            print(employee_data,'-------------------------------------')
            try:
                hr_status = employee_data[0].status
            except:
                hr_status='0'
            for data in employee_data:
                if data.project_name=='0' or data.project_name==0:
                    continue
                else:
                    projectname.append(data.project_name)
                    if data.mon==None or data.mon=='None' or int(data.mon)>8:
                        days.append(0)
                    else:    
                        days.append(data.mon)
                    if data.tue==None or data.tue=='None' or int(data.tue)>8:
                        days.append(0)
                    else:    
                        days.append(data.tue)
                    if data.wed==None or data.wed=='None' or int(data.wed)>8:
                        days.append(0)
                    else:    
                        days.append(data.wed)
                    if data.thu==None or data.thu=='None' or int(data.thu)>8:
                        days.append(0)
                    else:    
                        days.append(data.thu)
                    if data.fri==None or data.fri=='None' or int(data.fri)>8:
                        days.append(0)
                    else:    
                        days.append(data.fri)
                    if data.sat==None or data.sat=='None' or int(data.sat)>8:
                        days.append(0)
                    else:    
                        days.append(data.sat)
                    if data.sun==None or data.sun=='None' or int(data.sun)>8:
                        days.append(0)
                    else:    
                        days.append(data.sun)
                   
                    # weektotal=data.totals
                    # weektotal.append(data.total)
                    print(data.total,'////////////////////////weektotal')
                    mond=mond+int(data.mon)
                    tue=tue+int(data.tue)
                    wed=wed+int(data.wed)
                    thu=thu+int(data.thu)
                    weektotal = data.totals
                    fri=fri+int(data.fri)
                    sat=sat+int(data.sat)
                    sun=sun+int(data.sun)
                    # weektotal = data.totals
            # weektotal = [int(i) for i in weektotal]
            # weektotal = sum(weektotal)
                    
            print(weektotal)       
            dats={}
            c=0
            
            
            for pro in projectname:
                c+=1
                p='project'+str(c)
                
                dats[f"{p}"]=pro
                for i in range(0,len(days)):
                    day='day'+str(i)
                    dats[f"{day}"]=days[i]
            emp=Empdata.objects.all()
            total_hour=0
            for i in emp:
                if str(request.session['id'])==str(i.emp_id):
                    total_hour=total_hour+int(i.total)
            tt=total_hour 
            name=request.session['name']
            id=request.session['id']
            # print(name,id)
            lists=[]
            i=0
            rows=0
            count=0
            total=0
            start=0
            end_dt=0
            x=datetime.now().date()
            y=datetime.now().date()
            for i in range(8):
                if x.weekday()==0:
                    start=x
                else:
                    x=x- timedelta(days=1, hours=0)
                if y.weekday()==6:
                    end_dt=y
                else:
                    y=y - timedelta(days=1, hours=0)
            start_date=start
            end_date=end_dt
            tracker_leaves=EmpLeaves.objects.filter(emp_id=request.session['id'],status='Approved')
            # tracker_leaves=tracker_leaves[0]
            # print(tracker_leaves)
            for i in tracker_leaves:
                tracker_leaves_start=i.from_dt
                tracker_leaves_end=i.to_dt
                tracker_leaves_start=datetime.strptime(tracker_leaves_start, '%Y-%m-%d')
                x=tracker_leaves_start
                
                tracker_leaves_end=datetime.strptime(tracker_leaves_end, '%Y-%m-%d')
                y=tracker_leaves_end
                
                for j in range(8):
                    if x.weekday()==0:

                        start=x
                    else:
                        x=x- timedelta(days=1, hours=0)
                    if y.weekday()==6:
                        end_dt=y
                    else:
                        y=y - timedelta(days=1, hours=0)
                start_date_track=start
                start_datetrack=start_date
                start_datetrack=str(start_datetrack)
                start_datetrack=datetime.strptime(start_datetrack, '%Y-%m-%d')
                end_date_track=end_dt
                trackerleavedate=datetime.strptime(i.from_dt, '%Y-%m-%d')
                # print(start_date_track,'start')
                # print(end_date_track,'end')
                # print(start_datetrack,'middle')
                if start_date_track==start_datetrack:
                    try:
                        range_no=i.no_of_days
                        if '.' in range_no:
                            range_no=float(i.no_of_days)
                            range_no=range_no-0.5
                            range_no=int(range_no)
                        else:
                            range_no=int(range_no)
                            
                    except:
                        range_no=0
                        pass
                    for k in range(range_no):
                        trackerleavedate=trackerleavedate+ timedelta(days=1,hours=0)
                        # print(trackerleavedate,'this')
                        day=trackerleavedate.strftime('%A')
                        daystr.append(day)
                        # print(k)
                    daystr.append(i.leave_type)
                # daystrr.append(daystr)
            flag=0  
            flag2=0 
            # print(daystr,'helloworld')
            for i in daystr:
                flag+=1
                text=i.split(" ")
                if len(text)>1:
                    leave_type = text[0]+text[1]
                    
                    if  text[0]=='Sick':
                        sickleaves=daystr[flag2:flag]
                        flag2+=1
                        # # print(flag2,flag)
                        # # print(sickleaves,'helga')
                    else:
                        otherleaves=daystr[flag2:flag]
                        flag3=flag
                
            leave_day =EmpLeaves.objects.filter(emp_id=request.session['id'],status='Approved')
            # print(sickleaves,otherleaves)
            if request.method=="POST" and ('prev' in request.POST or 'next' in request.POST):
                
                if 'prev' in request.POST:
                    start_dates=request.session['start_date']
                    end_dates=request.session['end_date']
                    start_dates=datetime.strptime(start_dates, "%Y-%m-%d")
                    end_dates=datetime.strptime(end_dates, "%Y-%m-%d")
                    start_dates=start_dates- timedelta(days=7, hours=0)
                    end_dates=end_dates- timedelta(days=7, hours=0)
                    start_dates=start_dates.date()
                    end_dates=end_dates.date()
                    request.session['start_date']=str(start_dates)
                    request.session['end_date']=str(end_dates)
            
                elif 'next' in request.POST:
                    start_dates=request.session['start_date']
                    end_dates=request.session['end_date']
                    start_dates=datetime.strptime(start_dates, "%Y-%m-%d")
                    end_dates=datetime.strptime(end_dates, "%Y-%m-%d")
                    start_dates=start_dates+ timedelta(days=7, hours=0)
                    end_dates=end_dates+ timedelta(days=7, hours=0)
                    start_dates=start_dates.date()
                    end_dates=end_dates.date()
                    request.session['start_date']=str(start_dates)
                    request.session['end_date']=str(end_dates)
                sun,tue,mond,wed,thu,fri,sat=0,0,0,0,0,0,0
                projectname,days=[],[]
                
                weektotal=0
                employee_data=Empdata.objects.annotate(totals_as_integer=Cast('totals', IntegerField())).filter(emp_id=request.session['id'],start=start_dates).order_by('totals_as_integer')
                print(employee_data,'-------------------------------------')
                try:
                    hr_status = employee_data[0].status
                except:
                    hr_status='0'
                for data in employee_data:
                    
                    days.append(data.mon)
                    days.append(data.tue)
                    days.append(data.wed)
                    days.append(data.thu)
                    days.append(data.fri)
                    days.append(data.sat)
                    days.append(data.sun)
                    
                    projectname.append(data.project_name)
                    weektotal=data.totals
                    
                    mond=mond+int(data.mon)
                    tue=tue+int(data.tue)
                    wed=wed+int(data.wed)
                    thu=thu+int(data.thu)
                    fri=fri+int(data.fri)
                    sat=sat+int(data.sat)
                    sun=sun+int(data.sun)
                # weektotal = sum([int(i) for i in weektotal ])
                dats={}
                for pro in projectname:
                    for i in range(0,len(days)):
                        
                        dats[f"{pro}"]=pro
                        day='day'+str(i)
                        dats[f"{day}"]=days[i]
                if manager_id == Login.objects.get(id=request.session['id']).office_manager:
                    managersall=Login.objects.filter(user_type=3,office_manager=Login.objects.get(id=request.session['id']).office_manager)
                    managersall=[x.id for x in managersall]
                    projectss=ProjectDetails.objects.filter(manager_id__in=managersall)
                    print(managersall,';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;',projectss)
                else:
                    projectss=ProjectDetails.objects.filter(manager_id=manager_id)        
                    
                try :
                    print(start_dates,'|||||||||||||||||||------start_dates-----------||||||||||||||||')
                    comments=Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).employee_comment
                    tue_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_tue
                    wed_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_wed
                    thu_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_thu
                    fri_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_fri
                    sat_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_sat
                    print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'try')
                except :
                    comments = ''
                    tue_comm = ''
                    wed_comm = ''
                    thu_comm = ''
                    fri_comm = ''
                    sat_comm = ''
                    print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'except')
                date_format = "%Y-%m-%d"
                start_dates_dt = datetime.strptime(request.session['start_date'], date_format)
                end_dates_dt = datetime.strptime(request.session['end_date'], date_format)
                print(start_dates_dt,end_dates_dt,'//////////////////')
                current_date = datetime.now()
                day_names = []

                
                while start_dates_dt <= current_date:
                    # Get the day name for the current date in the loop
                    day = start_dates_dt.strftime("%A")
                    # Append the day name to the list
                    day_names.append(day)
                    # Move to the next day
                    start_dates_dt += timedelta(days=1)
                
                datas={'comments':comments,'tue_comm':tue_comm,'wed_comm':wed_comm,'thu_comm':thu_comm,'fri_comm':fri_comm,'sat_comm':sat_comm,
                'projectss':projectss,'day':day_names,'messages':messages,'sickleaves':sickleaves,'otherleaves':otherleaves,'hr_status':hr_status,'emp_data':employee_data,'list': lists,'total':total,'rows':rows,'days':days,'name':name,'start_date':start_dates,'end_date':end_dates,'totals':total_hour,'gtotal':weektotal,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun}
                for keys,values in dats.items():
                    datas[f"{keys}"]=values  
                name=request.session['name']  
                return render(request,'Emp_tracker.html',datas)
            
            elif request.method=="POST":
                
                if 'submit' in request.POST:
                    obj=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates,status='4')
                    print(obj,'----------------',len(obj))
                    if len(obj)==0:
                        # messages="This Week's Timesheet Already Submitted..!"
                        # print(messages)
                        name=request.session['name']
                        # print(name) 
                        projects=Project_team.objects.filter(employee_name=name)
                        totala,totalb,totalc,totals,i,dts=0,0,0,0,0,1
                        rows=int(request.POST.get('rows'))
                        print(rows,'rows---------------')
                        lists=[]
                        extra=0
                        obj=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates)
                        extra=(len(obj)-len(projects))
                        noof=extra+len(projects)
                        print(noof)
                        for i in range(noof):
                            if True:
                                assigned1=request.POST.get(f'assigned{i+1}')
                                if assigned1 == '' or assigned1 == 'None' or assigned1 == None:
                                    assigned1 = ' ' 
                                a1=request.POST.get(f'a1{i+1}')
                                print(a1,'-----------------')
                                if a1 == '' or a1 == 'None' or a1 == None or int(a1) > 8:
                                    a1 = 0 
                                a2=request.POST.get(f'a2{i+1}')
                                if a2 == '' or a2 == 'None' or a2 == None or int(a2) > 8:
                                    a2 = 0 
                                a3=request.POST.get(f'a3{i+1}')
                                if a3 == '' or a3 == 'None' or a3 == None or int(a3) > 8:
                                    a3 = 0 
                                a4=request.POST.get(f'a4{i+1}')
                                if a4 == '' or a4 == 'None' or a4 == None or int(a4) > 8:
                                    a4 = 0 
                                a5=request.POST.get(f'a5{i+1}')
                                if a5 == '' or a5 == 'None' or a5 == None or int(a5) > 8:
                                    a5 = 0 
                                a6=request.POST.get(f'a6{i+1}')
                                if a6 == '' or a6 == 'None' or a6 == None or int(a6) > 8:
                                    a6 = 0 
                                a7=request.POST.get(f'a7{i+1}')
                                if a7 == '' or a7 == 'None' or a7 == None or int(a7) > 8:
                                    a7 = 0 
                                a0=request.POST.get(f'a0{i+1}')
                                # print(a0)
                                print(assigned1,a1,a2,a3,a4,a5,a6,a7,'///////hours')
                            else:
                                pass
                            
                            try:
                                if a0 !='0' and a0!= None :
                                    totala=int(a1)+int(a2)+int(a3)+int(a4)+int(a5)+int(a6)+int(a7)
                                    totals=totals+totala
                                    a={"b0":a0,"b1":a1,"b2":a2,"b3":a3,"b4":a4,"b5":a5,"b6":a6,"b7":a7,"total":totala,'totals':totals,'assigned1':assigned1}
                                    lists.append(a)
                                    # print(lists)
                                    
                            except:
                                pass
                        if rows >0:
                            for i in range(0,rows*8,8):

                                assigned1=request.POST.get("assigned"+str(i))
                                if assigned1=='None' or assigned1==None or assigned1=='' or assigned1==' ':
                                    assigned1=''
                                b0=request.POST.get("Name"+str(i))
                                if b0=='None' or b0==None or b0=='' or b0==' ':
                                    b0=0
                                b1=request.POST.get("Name"+str(i+1))
                                if b1=='None' or b1==None or b1=='' or b1==' ' or int(b1) > 8:
                                    b1=0
                                b2=request.POST.get("Name"+str(i+2))
                                if b2=='None' or b2==None or b2=='' or b2==' ' or int(b2) > 8:
                                    b2=0
                                b3=request.POST.get("Name"+str(i+3))
                                if b3=='None' or b3==None or b3=='' or b3==' ' or int(b3) > 8:
                                    b3=0
                                b4=request.POST.get("Name"+str(i+4))
                                if b4=='None' or b4==None or b4=='' or b4==' ' or int(b4) > 8:
                                    b4=0
                                b5=request.POST.get("Name"+str(i+5))
                                if b5=='None' or b5==None or b5=='' or b5==' ' or int(b5) > 8:
                                    b5=0
                                b6=request.POST.get("Name"+str(i+6))
                                if b6=='None' or b6==None or b6=='' or b6==' ' or int(b6) > 8:
                                    b6=0
                                b7=request.POST.get("Name"+str(i+7))
                                if b7=='None' or b7==None or b7=='' or b7==' ' or int(b7) > 8:
                                    b7=0
                                try:
                                    total=int(b1)+int(b2)+int(b3)+int(b4)+int(b5)+int(b6)+int(b7)
                                    totals=totals+int(b1)+int(b2)+int(b3)+int(b4)+int(b5)+int(b6)+int(b7)
                                    print(total,totals,'total_Totals---------------')
                                except:
                                    pass
                                i=0
                                
                                b={"b"+str(i):b0,"b"+str(i+1):b1,"b"+str(i+2):b2,"b"+str(i+3):b3,"b"+str(i+4):b4,"b"+str(i+5):b5,"b"+str(i+6):b6,"b"+str(i+7):b7,"total":total,'totals':totals,'assigned1':assigned1}
                                lists.append(b)
                        # For saving in database 
                        manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
                        hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
                        
                        emp_id=request.session['id']
                        
                        createdate=date.today()
                       
                        employee_comment=request.POST.get('comment')
                        # print(comment)
                        emp_comm_tue=request.POST.get('tue_comment')
                        print(emp_comm_tue)
                        emp_comm_wed=request.POST.get('wed_comment')
                        emp_comm_thu=request.POST.get('thu_comment')
                        emp_comm_fri=request.POST.get('fri_comment')
                        emp_comm_sat=request.POST.get('sat_comment')
                      
                        print(createdate,'createdate')
                        print(hr_id,'hr_id')
                        print(manager_id,'manager_id')
                        print(employee_comment,'manager_comment')
                        
                        try:
                            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
                            existing_rating.enddates = end_dates  # Update the fields you want to change
                            existing_rating.createdate = createdate  # Update the fields you want to change
                            existing_rating.hr_id = hr_id  # Update the fields you want to change
                            existing_rating.manager_id = manager_id  # Update the fields you want to change
                            if employee_comment != None:
                                existing_rating.employee_comment = employee_comment  # Update the fields you want to change
                            if emp_comm_tue != None:
                                existing_rating.emp_comm_tue = emp_comm_tue 
                            if emp_comm_wed != None:
                                existing_rating.emp_comm_wed = emp_comm_wed
                            if emp_comm_thu != None:
                                existing_rating.emp_comm_thu = emp_comm_thu
                            if emp_comm_fri != None:
                                existing_rating.emp_comm_fri = emp_comm_fri
                            if emp_comm_sat != None:
                                existing_rating.emp_comm_sat = emp_comm_sat
                            existing_rating.save()
                        except Ratings.DoesNotExist:
                            # If a row with the specified emp_id and startdate does not exist, create a new one
                            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
                            # Set other fields of the new_rating as needed
                            # Set other fields here
                            new_rating.enddates = end_dates  # Set other fields here
                            new_rating.createdate = createdate  # Set other fields here
                            new_rating.hr_id = hr_id  # Set other fields here
                            new_rating.manager_id = manager_id  # Set other fields here
                            if employee_comment != None:
                                new_rating.employee_comment = employee_comment  # Update the fields you want to change
                            if emp_comm_tue != None:
                                new_rating.emp_comm_tue = emp_comm_tue 
                            if emp_comm_wed != None:
                                new_rating.emp_comm_wed = emp_comm_wed
                            if emp_comm_thu != None:
                                new_rating.emp_comm_thu = emp_comm_thu
                            if emp_comm_fri != None:
                                new_rating.emp_comm_fri = emp_comm_fri
                            if emp_comm_sat != None:
                                new_rating.emp_comm_sat = emp_comm_sat
                            new_rating.save()
                        print(lists,'lists***********************')
                        for i in lists:
                            try:
                                obj=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates,project_name=i['b0'])
                                obj.delete()
                            except:
                                pass
                            statushr=0
                            if Login.objects.get(id=id).work_location == 'US':
                                statushr=0
                            
                            work_location=Login.objects.get(id=request.session['id']).work_location
                            office_manager=Login.objects.get(id=request.session['id']).office_manager
                            stat=str(4)
                            status_om=0
                            if work_location== 'IN':
                                status_om=1

                            if office_manager == manager_id:
                                
                                stat=1
                                pass
                            a = Empdata(emp_id=id,mon= i['b1'] ,tue=str(i['b2']) ,wed=i['b3'] ,thu=str(i['b4']) ,fri=str(i['b5']) ,sat=str(i['b6']) ,sun=str(i['b7']),status=stat,project_name=str(i['b0']),start=str(start_dates),end=str(end_dates),name=name, total=i['total'],totals=i['totals'],statushr=statushr,date_created=datetime.now().date(), hr_id=hr_id, manager_id=manager_id,assigned=i['assigned1'],work_location=work_location,status_om=status_om,office_manager=office_manager)
                            
                            if i['b1']==0 and i['b2']==0 and i['b3']==0 and i['b4']==0 and i['b5']==0 and i['b6']==0 and i['b7'] == 0:
                                pass
                            else:
                                a.save()

                            # b= Empdata.objects.filter(emp_id=id,status=str(0),project_name=str(i['b0']),start=str(start_dates),end=str(end_dates),statushr=0)
                            # b.save()
                        
                        x = dateTime.now()
                        x=time.ctime(time.time())
                        current_date = datetime.now()
                        
                        formatted_date = current_date.strftime("%A, %B. %d, %Y")
                        next_formatted_date=datetime.strptime(start_dates,'%Y-%m-%d')
                        next_formatted_date=next_formatted_date+timedelta(days=7)
                        next_formatted_date = next_formatted_date.strftime("%A, %B. %d, %Y")
                        data={"list": lists,'total':total,'rows':rows,'name':name,'start_date':start_dates,'end_date':end_dates,'totals':total_hour,'gtotal':weektotal,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun}
                        for keys,values in dats.items():
                            data[f"{keys}"]=values
                        name=request.session['name']
                        #return render(request,'Emp_tracker.html',data)
                        status=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates)
                        # for statuss in status:
                        #     statuss.status=0
                        #     statuss.save(update_fields=['status'])
                        notify = Notifications(emp_id=request.session['id'],message=f'{request.session["name"]} has submitted their weekly task for approval', date=start_dates,current_date=datetime.now().date(), emp=0,hr=1,manager=1,hr_id=hr_id,manager_id=manager_id) 
                        notify.save()                 
                        x = datetime.now()
                        x = x=time.ctime(time.time())
                        activity = Activities(emp_id=request.session['id'],message=f'Your timesheet is submitted',date=start_dates,currentdate=x)
                        activity.save()
                        email = Login.objects.get(id=hr_id).email
                        # email='karan.rana@ariespro.com'
                        name=request.session['name']
                        sender = 'ats.ariespro@gmail.com'
                        receivers = email
                        password = 'ahbfhcshjujvkgge'
                        Subject= 'Pending Timesheet Approval'
                        gender=EmpDesk.objects.get(login_id=request.session['id']).gender
                        if gender=='Male' or gender=='male':
                            gender='his'
                        elif gender=='Female' or gender=='female':
                            gender='her'
                        else:
                            gender='their'
                        message = f"""

                        Hi,
                        
                        {request.session['name']}  Submited {gender} Timesheet for {start_dates} to {end_dates} on {formatted_date}.
                        Please approve or reject timesheet by {next_formatted_date}.
                        
                        To access the portal, please click on the following link: "https://hcm.ariespro.com/".

                        Note: DO NOT REPLY TO THIS EMAIL. If you did not request this change, or if you believe you have 
                        received this email in error, please email at it.support@ariespro.com.

                        Thank you,
                        AriesPro Utilities
                        """

                        server=EmailMessage()

                        server['From']='Ariespro'
                        server['To']=receivers
                        server['Subject']=Subject
                        server.set_content(message)
                        if True:
                            context=ssl.create_default_context()
                            with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                                smtp.login(sender,password)
                                smtp.sendmail(sender,receivers,server.as_string())
                        else:
                            pass
                        messages='Timesheet Submitted..!'
                        # print(messages)
           
            sun,tue,mond,wed,thu,fri,sat=0,0,0,0,0,0,0
            print(start_dates ,type(start_dates),'start_dates',end_dates,type(end_dates),'end_dates',)
            projectname,days=[],[]
            try:
                print(start_dates,'start_dates')
                start_dates = datetime.strptime(start_dates, "%Y-%m-%d")
            except:
                pass
            try:
                end_dates = datetime.strptime(end_dates, "%Y-%m-%d")
            
            except:
                pass
            if True:
                start_dts=start_dates.strftime("%Y-%m-%d ")
                start_dates=start_dates.strftime("%Y-%m-%d ")

            else:
                pass
            if True:
                end_dates=end_dates.strftime("%Y-%m-%d ")
            else:
                pass
            
            weektotal=0
            employee_data=Empdata.objects.annotate(totals_as_integer=Cast('totals', IntegerField())).filter(emp_id=request.session['id'],start=start_dts).order_by('totals_as_integer')
            try:
                hr_status = employee_data[0].status
            except:
                hr_status=0
            for data in employee_data:
                   
                if data.mon==None or data.mon=='None':
                    days.append(0)
                else:
                    days.append(data.mon)
                if data.tue==None or data.tue=='None':
                    days.append(0)
                else:
                    days.append(data.tue)
                if data.wed==None or data.wed=='None':
                    days.append(0)
                else:
                    days.append(data.wed)
                if data.thu==None or data.thu=='None':
                    days.append(0)
                else:
                    days.append(data.thu)
                if data.fri==None or data.fri=='None':
                    days.append(0)
                else:
                    days.append(data.fri)
                if data.sat==None or data.sat=='None':
                    days.append(0)
                else:
                    days.append(data.sat)
                if data.sun==None or data.sun=='None':
                    days.append(0)
                else:
                    days.append(data.sun)
                    
                projectname.append(data.project_name)
                # weektotal.append(data.total)
                weektotal=data.totals
                print(weektotal,'weektotal')   
                mond=mond+int(data.mon)
                tue=tue+int(data.tue)
                wed=wed+int(data.wed)
                thu=thu+int(data.thu)
                fri=fri+int(data.fri)
                sat=sat+int(data.sat)
                sun=sun+int(data.sun)

            # weektotal = sum([int(i) for i in weektotal ])    
            print(weektotal,'weektotal2-------------')   
            pp=0
             
            dats={'day0':0,'day1':0,'day2':0,'day3':0,'day4':0,'day5':0,'day6':0,'day7':0,'day8':0,'day9':0,'day10':0,'day11':0,'day12':0,'day13':0,'day14':0,'day15':0,'day16':0,'day17':0,'day18':0,'day19':0,'day20':0,"project1":"--Select--","project2":"--Select--","project3":"--Select--"}
                
            for pro in projectname:
                pp+=1
                p='project'+str(pp)
                for i in range(0,len(days)):
                        
                    dats[f"{p}"]="--"+pro+"--"
                    day='day'+str(i)
                    dats[f"{day}"]=days[i]
            projects=Project_team.objects.filter(employee_name=name)
            hr_id=EmpDesk.objects.get(login_id=request.session['id']).hr_id
            manager_id=EmpDesk.objects.get(login_id=request.session['id']).manager_id
            
            for i in projects:
                emp=Empdata.objects.filter(emp_id=request.session['id'],project_name=i.project,start=start_dates,)
                # print(emp,'this is the list of Projects i am in')
                if len(emp)>0:
                    pass
                else:
                    # print(i,'this is the list of Projects on my time sheet')
                    a = Empdata(emp_id=request.session['id'],mon='0' ,tue='0', wed='0',thu='0' ,fri='0' ,sat='0' ,sun='0',project_name=i.project,start=str(start_dates),end=str(end_dates),name=name,hr_id=hr_id,manager_id=manager_id, status=4,total=0,totals=0,statushr=0,date_created=datetime.now().date(),assigned='*')
                    a.save()
            obj=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates)
            email_data=EmpDesk.objects.filter(login_id=request.session['id'])
            email_data=email_data[0].email
            name=request.session['name'] 
            projects=Project_team.objects.filter(employee_name=email_data)
            if manager_id == Login.objects.get(id=request.session['id']).office_manager:
                managersall=Login.objects.filter(user_type=3,office_manager=Login.objects.get(id=request.session['id']).office_manager)
                managersall=[x.id for x in managersall]
                projectss=ProjectDetails.objects.filter(manager_id__in=managersall)
                print(managersall,';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;',projectss)
            else:
                projectss=ProjectDetails.objects.filter(manager_id=manager_id)
            

            try :
                print(start_dates,'|||||||||||||||||||------start_dates-----------||||||||||||||||')
                comments=Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).employee_comment
                tue_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_tue
                wed_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_wed
                thu_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_thu
                fri_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_fri
                sat_comm = Ratings.objects.get(emp_id=request.session['id'],startdate=start_dates).emp_comm_sat
                print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'try')
            except :
                comments = ''
                tue_comm = ''
                wed_comm = ''
                thu_comm = ''
                fri_comm = ''
                sat_comm = ''
                print(tue_comm,wed_comm,thu_comm,fri_comm,sat_comm,'except')
            print(start_dates,end_dates)
            date_format = "%Y-%m-%d"
            start_dates = start_dates.strip()
            end_dates = end_dates.strip()
            # Convert the string dates to datetime objects
            start_dates_dt = datetime.strptime(start_dates, date_format)
            end_dates_dt = datetime.strptime(end_dates, date_format)

            # Get the current date and time
            current_date = datetime.now()
            
            # Check if the current date is within the range
            day_names = []

            # Loop through each day from start_date to current_date
            while start_dates_dt <= current_date:
                # Get the day name for the current date in the loop
                day = start_dates_dt.strftime("%A")
                # Append the day name to the list
                day_names.append(day)
                # Move to the next day
                start_dates_dt += timedelta(days=1)

            # Print the list of day names
            print(day_names)
            datas={'comments':comments,'tue_comm':tue_comm,'wed_comm':wed_comm,'thu_comm':thu_comm,'fri_comm':fri_comm,'sat_comm':sat_comm,
            "list": lists,'day':day_names,'total':total,'daystr':daystr,'hr_status':hr_status,'sickleaves':sickleaves,'messages':messages,'otherleaves':otherleaves,'emp_data':obj,'rows':rows,'name':name,'projects':projects,'projectss':projectss,'start_date':start_dates,'end_date':end_dates,'totals':total_hour,'gtotal':weektotal,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun,"project1":"--Select--","project2":"--Select--","project3":"--Select--"}
            for keys,values in dats.items():
                datas[f"{keys}"]=values  
            name=request.session['name'] 
            return render(request,'Emp_tracker.html',datas)
            #return render(request,'Emp_tracker.html',data)
        else:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response
    else:
        
        response=HttpResponseRedirect('../../')
        return response


def Emp_EditProfile(request):
    try:
        if request.session['user']=="3":

            message1 = ''
            message = ''
            empl = EmpDesk.objects.filter(login_id=request.session['id'])
            empl = empl[0]
            if request.method == 'POST':
                if 'editProfile' in request.POST:
                    data = EmpDesk.objects.filter(login_id=request.session['id'])
                    data = data[0]
                    data.f_name=request.POST.get('fname') 
                    data.save(update_fields=['f_name'])
                    data.l_name=request.POST.get('lname')
                    data.save(update_fields=['l_name'])
                    data.email=request.POST.get('email')
                    data.save(update_fields=['email'])
                    data.mobile=request.POST.get('mobileNo')
                    data.save(update_fields=['mobile'])
                    data.address=request.POST.get('addr')
                    data.save(update_fields=['address'])
                    
                    data = Login.objects.filter(id=request.session['id'])
                    data = data[0]
                    data.f_name=request.POST.get('fname')
                    data.save(update_fields=['f_name'])
                    data.l_name=request.POST.get('lname')
                    data.save(update_fields=['l_name'])
                    data.email=request.POST.get('email')
                    data.save(update_fields=['email'])
                    data.mobile=request.POST.get('mobileNo')
                    data.save(update_fields=['mobile'])
                    data.address=request.POST.get('addr')
                    data.save(update_fields=['address']) 
                    
                    # print(request.FILES,'hello world')
                    if len(request.FILES) != 0:
                        data.image = request.FILES['profile_pic']
                        data.save(update_fields=['image'])
                        task=Login.objects.filter(id=request.session['id'])
                        request.session['profile_pic']=str(task[0].image)
                    

                elif 'changePass' in request.POST:
                    data = Login.objects.filter(id=request.session['id'])
                    data = data[0]
                    pwd= data.password
                    try:
                        cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                        decryptedpassword = (cipher_suite.decrypt(pwd))
                        pwd=decryptedpassword.decode()
                    except:
                        pass
                    if data.password == request.POST.get('currPass'):
                        if request.POST.get('password') == request.POST.get('confirmPass'):
                            key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
                            cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                            ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                            # print(ciphered_text) 
                            pwd=ciphered_text.decode()
                            data.password=pwd
                            data.save(update_fields=['password'])

                        else:
                            message1 = 'password and confirm password must be same.'
                    elif pwd == request.POST.get('currPass'):
                        if request.POST.get('password') == request.POST.get('confirmPass'):
                            key = b'PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug='
                            cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                            ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                            # print(ciphered_text) 
                            pwd=ciphered_text.decode()
                            data.password=pwd
                            data.save(update_fields=['password'])

                        else:
                            message1 = 'password and confirm password must be same.'
                    
                    else:
                        message = 'current password is incorrect'

            name=request.session['name']
            empl = EmpDesk.objects.filter(login_id=request.session['id'])
            empl = empl[0]
            return render(request,'Emp_EditProfile.html',{"name":name,'employee':empl, 'message':message,'message1':message1})
        else:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response
    except:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response

def Emp_leave(request):
    try:
        if request.session['user']=="3":
            remaining_leaves=LeaveDetails.objects.filter(emp_id=request.session['id'])
            remaining_leaves=remaining_leaves[0]
            if request.method=="POST":
                manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
                hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
                leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
                empid=request.session['id']
                empname=request.session['name']
                leavetype=request.POST.get('leaveType')
                fromdt=request.POST.get('fromDate')
                todt=request.POST.get('toDate')
                daytype=request.POST.get('day')
                noofdays=request.POST.get('NumofDays')
                taken=leave_details[0].taken
                remaining=leave_details[0].days_allowed
                reason=request.POST.get('leaveReason')
                flagdata=EmpDesk.objects.filter(login_id = empid)
                dateofjoining=str(flagdata[0].doj)
                noofdays=float(noofdays)
                dateofjoining = datetime.strptime(dateofjoining, '%Y-%m-%d')
                todaydate=datetime.now()
                gap=(todaydate-dateofjoining)
                if gap.days > 150:
                    valid_leaves=1 
                else:
                    valid_leaves=0
                if leavetype=='Sick Leave':
                    sl=remaining_leaves.sick_day
                    sl=float(sl)
                    if sl>noofdays:
                        paid_leave=noofdays
                    else:
                        paid_leave=sl
                else:
                    rmn=remaining_leaves.days_allowed
                    print(rmn,'hello world ')
                    try:
                        rmn=float(rmn)
                    except:
                        rmn=0
                    if rmn>noofdays:
                        paid_leave=noofdays
                    else:
                        paid_leave=rmn        

                # if 'cancelLeave' in request.POST :
                #     name=request.session['name']
                #     return render(request,'Emp_leave.html',{"name":name})

                if 'applyLeave' in request.POST :
                    leave_details = EmpLeaves(emp_id=empid,emp_name=empname,leave_type=leavetype,from_dt=fromdt,to_dt=todt,day_type=daytype,no_of_days=noofdays,leave_taken=taken,remaining_leaves=remaining,reason=reason,status='Applied',date_applied=datetime.now().date(),user_type=3,valid_leaves=valid_leaves, paid_leaves=paid_leave, hr_id=hr_id, manager_id=manager_id)
                    leave_details.save()
                    
                    notify = Notifications(emp_id=request.session['id'],message=f'{request.session["name"]} has applied for leave', date=start_dates,current_date=datetime.now().date(), emp=0,hr=1,manager=0, hr_id=hr_id,manager_id=manager_id) 
                    notify.save()

                    x = datetime.now()
                    x=time.ctime(time.time())
                    activity = Activities(emp_id=request.session['id'],message=f'Leave applied successfully',date=start_dates,currentdate=x)
                    activity.save()
                    sender = 'ats.ariespro@gmail.com'
                    # receivers = "karan.rana@ariespro.com"
                    receivers = "karan.rana@ariespro.com"
                    password = 'ahbfhcshjujvkgge'
                    Subject= 'Leave Application'
                    message = f"""
                    Hi Ma'am,
                    - Leave Type: {leavetype}
                    - Number of Days: {noofdays}
                    - Date From: {fromdt}
                    - Date To: {todt}
                    - Note: {reason}.
                                        
                    Thank you,
                    {empname}
                            """
                    server=EmailMessage()
                    server['From']='Ariespro'
                    server['To']=receivers
                    server['Subject']=Subject
                    server.set_content(message)
                    context=ssl.create_default_context()
                    # with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                    #     smtp.login(sender,password)
                    #     smtp.sendmail(sender,receivers,server.as_string())
                    

                
            leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
            try:
                remaining=(float(leave_details[0].days_allowed)+float(leave_details[0].sick_day))
            except:
                remaining= leave_details[0].days_allowed
            taken=leave_details[0].taken
            name=request.session['name']
            emp_leaves=EmpLeaves.objects.filter(emp_id=request.session['id']).order_by('-id')
            return render(request,'Emp_leave.html',{'emp_leaves':emp_leaves,'remaining_leaves':remaining_leaves,"name":name,'remaining':remaining,'taken':taken})
        else:
            response=HttpResponseRedirect('../../')
            return response
            # return response
    except:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response
def Emp_notification(request):
    try:
        if request.session['user']=="3":
            notify = []
            if request.method == 'POST':
                if 'clear' in request.POST:
                    notify = Notifications.objects.filter(emp_id=request.session['id'])

                    # print(notify,"hello world")
                    for i in notify:
                        i.emp='2'
                        i.save(update_fields=['emp'])
                        # print(i,"hello")                

            notification=Notifications.objects.filter(emp_id=request.session['id'],emp='1')
            
                
            name=request.session['name']
            
            return render(request,'Emp_notification.html',{"name":name,'notify':notify,'notifications':notification})
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response
def Emp_profile(request):
    try:
        if request.session['user']=="3":
            name=request.session['name']

            profileData = EmpDesk.objects.filter(login_id=request.session['id'])
            profileData = profileData[0]
            
            return render(request,'Emp_profile.html',{"name":name, 'profile': profileData})
        else:
            response=HttpResponseRedirect('../../')
            return response
            return response
    except:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response
def Emp_report(request):
    try:
        if request.session['user']=="3":

            test = ProjectDetails.objects.all()
            projects = ProjectDetails.objects.all()
            dlist = {}
            label=[]
            data=[]
            labels=Empdata.objects.filter(emp_id=request.session['id'])
            for i in labels:
                d=0
                projectName=i.project_name
                datas=Empdata.objects.filter(project_name=projectName,emp_id=request.session['id'])
                for j in datas:
                    d=d+int(j.total)
                if projectName in label:
                    pass
                else:
                    dlist[f'{projectName}']=d
                    label.append(projectName)
                    data.append(d)
            dlist = zip(label, data)
                
                
            

            global start_dates
            global end_dates
            start_dates=datetime.now().date()
            end_dates=datetime.now().date()
            for i in range(8):
                if start_dates.weekday()==0:
                    starts=start_dates
                else:
                    start_dates=start_dates- timedelta(days=1, hours=0)
                if end_dates.weekday()==6:
                    end_dts=end_dates
                else:
                    end_dates=end_dates + timedelta(days=1, hours=0)
            start_dates=starts
            end_dates=end_dts   
            name=request.session['name']
            emp_id=request.session['id']
            bar=[]
            dash_data=Empdata.objects.filter(emp_id=emp_id,start=start_dates)
            current_month=date.today().month
            emp_dash_data=Empdata.objects.annotate(start_month=Cast('start', output_field=DateTimeField())).filter(emp_id=request.session['id'])
            # emp_dash_data = Empdata.objects.annotate(start_month=Cast('start', output_field=DateTimeField())).filter(emp_id=request.session['id'], start_month__month=current_month).values('project_name').annotate(total_hours=Sum('mon') + Sum('tue') + Sum('wed') + Sum('thu') + Sum('fri') + Sum('sat'))
            emp_dash_= []
            for i in emp_dash_data:
                data1= []
                project = i.project_name
                hours_worked = i.total
                data1 = [project,hours_worked]
                emp_dash_.append(data1)
            print(emp_dash_)
            project_hours = defaultdict(int)

            for project, hours in emp_dash_:
                project_hours[project] += int(hours)

            emp_dash_aggregated = [[project, hours] for project, hours in project_hours.items()]
            print(emp_dash_aggregated)
            emp_dash_=[]
            lef=[]
            rig=[]
            for i in emp_dash_aggregated:
                if i[0]=='0' or i[1]=='0' or i[1]==0 or i[0]==0:
                    pass
                else:
                    lef.append(i[0])
                    rig.append(i[1])
                    emp_dash_.append(i)
            emp_dash=zip(lef,rig)  

            print(emp_dash_)
            datas={'emp_dash_':emp_dash_,"name":request.session['name'],'test':test,'dlist':dlist,'label':label,'data':data,'project0': '', 'mon0': 0, 'tue0': 0, 'wed0': 0, 'thu0': 0, 'fri0': 0, 'sat0': 0, 'sun0': 0, 'project1': '', 'mon1': 0, 'tue1': 0, 'wed1': 0, 'thu1': 0, 'fri1': 0, 'sat1': 0, 'sun1': 0, 'project2': '', 'mon2': 0, 'tue1': 0, 'wed2': 0, 'thu2': 0, 'fri2': 0, 'sat2': 0, 'sun2': 0, 'project3': '', 'mon3': 0, 'tue3': 0, 'wed3': 0, 'thu3': 0, 'fri3': 0, 'sat3': 0, 'sun3': 0}
            
            for dash in dash_data:
                bar.append({'project':dash.project_name,'mon':dash.mon,'tue':dash.tue,'wed':dash.wed,'thu':dash.thu,'fri':dash.fri,'sat':dash.sat,'sun':dash.sun})

                
            employee=EmpLeaves.objects.filter(emp_id=str(request.session['id']))
            
            name=request.session['name']
            
            for i in range(len(bar)):
                for keys,values in bar[i].items():
                    if keys=="project":
                        datas[f"{keys}{i}"]=values 
                    else:
                        datas[f"{keys}{i}"]=int(values )
                    
            
            
            return render(request,'Emp_report.html',datas)
        else:
            response=HttpResponseRedirect('../../')
            return response
            return response
    except:
            s='enter credentials for Employee login '
            response=HttpResponseRedirect('../../')
            return response
def Emp_Project_List(request):
    try:
        if request.session['user']=="3":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for Employee login '
        response=HttpResponseRedirect('../../')
        return response
    if 'project_name' in request.POST:
        request.session['project_name']=request.POST.get('project_name')
        response=HttpResponseRedirect('/employee/Emp_Project_task')
        return response
    
    username=Login.objects.get(id=request.session['id']).user_name
    taskcrew=TaskCrew.objects.filter(employee_name=username)
    taskcrew=[x.task_id for x in taskcrew]
    
    projects_names=Tasks.objects.filter(id__in=taskcrew)
    projects_names=[x.project_id for x in projects_names]
    
    projects_names=set(projects_names)
    print(projects_names)
    
    project=[]
    assigned_date=[]
    pending=[]
    development=[]
    completed=[]
    for i in projects_names:
        try:
            assigned=Project_team.objects.get(employee_id=request.session['id'],project=i).crt_date
            assigned_date.append(assigned)
        except:
            assigned='Project Not Assigned.'
            assigned_date.append(assigned)
        project.append(i)
        projects_names=Tasks.objects.filter(project_id=i)
        task_ids=[x.id for x in projects_names]

        pending.append(len(TaskCrew.objects.filter(status='Task List',employee_name__contains=request.session['name'],task_id__in=task_ids)))
        development.append(len(TaskCrew.objects.filter(status='Development',employee_name__contains=request.session['name'],task_id__in=task_ids)))
        completed.append(len(TaskCrew.objects.filter(status='Completed',employee_name__contains=request.session['name'],task_id__in=task_ids)))
    projects=zip(project, pending, development,  completed,assigned_date)

    return render(request, "Emp_Project_List.html",{'projects':projects})

def Emp_Project_task(request):
    try:
        if request.session['user']=="3":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
                
    except:
        s='enter credentials for Employee login '
        response=HttpResponseRedirect('../../')
        return response
    task_id=request.session['project_name']
    print(task_id)
    project_team=Project_team.objects.filter(project=task_id)    
    task_ids=Tasks.objects.filter(project_id=request.session['project_name'])
    task_ids=[x.id for x in task_ids] 

    chats=TasksChats.objects.filter(task_id__in=task_ids).annotate(tasks_id=Cast('task_id', output_field=IntegerField())).exclude(description=None).order_by('id')
    last_id=[x.id for x in chats]
    try:
        last_id=last_id[-1]
    except:
        last_id=0
    request.session['last_id']=last_id
    print(request.session['last_id'],'last_id')
    print(request.session['id'],'id\\\\')
    print(request.session['user'])
    print(request.session['name'])
    # assigned_crew_task_id=TaskCrew.objects.filter(employee_name__contains=request.session['name']).values('task_id')
    # assigned_crew_task_id1 = list(assigned_crew_task_id)
    # assigned_task_ids=[]
   
    # for task in assigned_crew_task_id1:
    #     assigned_task_ids.append(task['task_id'])
    # print(assigned_task_ids)
    
    
    assigned_task_id_complted = TaskCrew.objects.filter(employee_name__contains=request.session['name'],status='Completed').values('task_id')
    assigned_task_id_task_list = TaskCrew.objects.filter(employee_name__contains=request.session['name'],status='Task List').values('task_id')
    assigned_task_id_develpoment = TaskCrew.objects.filter(employee_name__contains=request.session['name'],status='Development').values('task_id')
    
    
    assigned_complete = [task['task_id'] for task in assigned_task_id_complted]
    assigned_dev = [task['task_id'] for task in assigned_task_id_develpoment]
    assigned_task = [task['task_id'] for task in assigned_task_id_task_list]
    
    
    print(assigned_complete)
    print(assigned_dev)
    print(assigned_task)
    
    # tasks_list=Tasks.objects.filter(status='Task List',project_id=request.session['project_name'],id__in=assigned_task_ids).order_by('-id')
    tasks_list=Tasks.objects.filter(id__in=assigned_task,project_id=request.session['project_name']).order_by('-id')
    task_list=[]
    task_list_logs=[]
    logs=[]
    task_chat=[]
    task_crew=[]
    

    tasks=[]
    team=[]
    taskss=[]
    crew=[]
    task_chats=[]
    task_logs=[]
    attachments=[]

    print(request.session['project_name'],assigned_task,tasks_list,'tasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_listtasks_list')
    for i in tasks_list:
        tasks_list_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        tasks_list_log=len(tasks_list_logs)
        task_list.append(i)
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
        task_list_logs.append(tasks_list_log+1)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        logs.append(
            TasksLogs.objects
            .annotate(dates=Cast('crt_date', output_field=DateField()))
            .annotate(
                name=Subquery(
                    EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1]
                )
            )
            .filter(task_id=i.id)
            .order_by('id')
        )
        crews=TaskCrew.objects.filter(task_id=i.id)
        if len(crew)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        
    tasks_list=zip(task_list,task_list_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments)        

    # developments=Tasks.objects.filter(status='Development',project_id=request.session['project_name']).order_by('-id')
    developments=Tasks.objects.filter(id__in=assigned_dev,project_id=request.session['project_name']).order_by('-id')
    development=[]
    developments_logs=[]
    logs=[]
    task_chat=[]
    task_crew=[]
    tasks=[]
    team=[]

    
    tasks=[]
    team=[]
    taskss=[]
    crew=[]
    task_chats=[]
    task_logs=[]
    attachments=[]
    for i in developments:
        development_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        development_log=len(development_logs)
        development.append(i)
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
        developments_logs.append(development_log+1)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        logs.append(
            TasksLogs.objects
            .annotate(dates=Cast('crt_date', output_field=DateField()))
            .annotate(
                name=Subquery(
                    EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1]
                )
            )
            .filter(task_id=i.id)
            .order_by('id')
        )
        crews=TaskCrew.objects.filter(task_id=i.id)
        if len(crew)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
    development=zip(development,developments_logs,logs,task_chat,task_crew,tasks,crew ,task_chats ,task_logs ,attachments)  
    
    # completeds=Tasks.objects.filter(status='Completed',project_id=request.session['project_name']).order_by('-id')
    completeds=Tasks.objects.filter(id__in=assigned_complete,project_id=request.session['project_name']).order_by('-id')
    completed=[]
    completedt_logs=[]
    task_chat=[]
    task_crew=[]
    tasks=[]
    team=[]

    
    tasks=[]
    team=[]
    taskss=[]
    crew=[]
    task_chats=[]
    task_logs=[]
    attachments=[]
    
    print(task_chat)
    for i in completeds:
        completed_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        completed_log=len(completed_logs)
        completed.append(i)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
        completedt_logs.append(completed_log+1)
        logs.append(
            TasksLogs.objects
            .annotate(dates=Cast('crt_date', output_field=DateField()))
            .annotate(
                name=Subquery(
                    EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1]
                )
            )
            .filter(task_id=i.id)
            .order_by('id')
        )
        
        crews=TaskCrew.objects.filter(task_id=i.id)
        if len(crew)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        
    completed=zip(completed,completedt_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments)  
    print(task_chat)

    return render(request, "Emp_Project_task.html",{ 'project_team':project_team,'tasks_list':tasks_list, 'development':development, 'completed':completed,'chats':chats})

        




def mon_data(request):
    emp_id = request.session['id']
    start_dates=request.session['start_date']
    end_dates=request.session['end_date']
    hour_mon = request.GET.getlist('hoursList[]')
    project_mon = request.GET.getlist('projectList[]')
    employee_comment = request.GET.get('empComm')
    createdate = date.today()
    manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
    hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
    employee_name = request.session['name']
    work_location=Login.objects.get(id=request.session['id']).work_location
    office_manager=Login.objects.get(id=request.session['id']).office_manager
    stat=str(0)
    status_om=0
    if work_location== 'IN':
        status_om=1
    if office_manager == manager_id:
        stat=1
        pass
    # print( id,start_dates,end_dates,hour_mon,employee_comment,createdate,project_mon,manager_id,hr_id,employee_name)
    total_h = [int(i) for i in hour_mon]
    # print(hour_mon)
    # print(sum(hour_mon),'-------')
    weekly_hours=[]
    if sum(total_h)<9 and sum(total_h)>0:
        print('hello',total_h)
        try:
            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
            existing_rating.enddates = end_dates  
            existing_rating.createdate = createdate  
            existing_rating.hr_id = hr_id  
            existing_rating.manager_id = manager_id  
            existing_rating.employee_comment = employee_comment 
            existing_rating.save()
        except Ratings.DoesNotExist:
            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
            new_rating.enddates = end_dates  
            new_rating.hr_id = hr_id  
            new_rating.manager_id = manager_id  
            new_rating.createdate = createdate  
            new_rating.employee_comment = employee_comment 
            new_rating.save()


        for i in range(len(hour_mon)):
            hour_data = hour_mon[i]
            print(hour_data)
            priject_data = project_mon[i]
            print(priject_data)
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
            print(projectdata)
            if len(projectdata)>0:
                print('if====')
                old_data = Empdata.objects.get(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
                old_data.mon = hour_data
                old_data.office_manager = office_manager
                old_data.work_location = work_location
                old_data.status_om = status_om
                total = int(old_data.mon)+int(old_data.tue)+int(old_data.wed)+int(old_data.thu)+int(old_data.fri)+int(old_data.sat)+int(old_data.sun)
                old_data.total = total
                weekly_hours.append(total)
                old_data.totals = sum(weekly_hours)
                old_data.save()
            else:
                print('else============')
                employeedata=Empdata(emp_id=request.session['id'],status=stat,mon=hour_data,totals=0,hr_id=hr_id, manager_id=manager_id,
                        start=start_dates,end=end_dates,project_name=priject_data,work_location=work_location,office_manager=office_manager,
                        status_om=status_om,name=employee_name,statushr=0,date_created=datetime.now(),assigned='*',tue=0
                        ,wed=0,thu=0,fri=0,sat=0,sun=0)
                totL =  int(employeedata.mon)+int(employeedata.tue)+int(employeedata.wed)+int(employeedata.thu)+int(employeedata.fri)+int(employeedata.sat)+int(employeedata.sun)                
                weekly_hours.append(totL)
                employeedata.total = totL
                employeedata.totals = sum(weekly_hours)
                print(totL,'----------------TOTL')
                employeedata.save()
    else:
        pass   
    return JsonResponse({'message':'success'})


def tue_data(request):
    emp_id = request.session['id']
    start_dates=request.session['start_date']
    end_dates=request.session['end_date']
    hour_mon = request.GET.getlist('hoursList[]')
    project_mon = request.GET.getlist('projectList[]')
    employee_comment = request.GET.get('empComm')
    createdate = date.today()
    manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
    hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
    employee_name = request.session['name']
    work_location=Login.objects.get(id=request.session['id']).work_location
    office_manager=Login.objects.get(id=request.session['id']).office_manager
    stat=str(0)
    status_om=0
    if work_location== 'IN':
        status_om=1
    if office_manager == manager_id:
        stat=1
        pass

    total_h = [int(i) for i in hour_mon]
    weekly_hours=[]
    if sum(total_h)<9 and sum(total_h)>0:
        try:
            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
            existing_rating.enddates = end_dates  
            existing_rating.createdate = createdate  
            existing_rating.hr_id = hr_id  
            existing_rating.manager_id = manager_id  
            existing_rating.emp_comm_tue = employee_comment 
            existing_rating.save()
        except Ratings.DoesNotExist:
            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
            new_rating.enddates = end_dates  
            new_rating.hr_id = hr_id  
            new_rating.manager_id = manager_id  
            new_rating.createdate = createdate  
            new_rating.emp_comm_tue = employee_comment 
            new_rating.save()

        for i in range(0,len(hour_mon)):
            hour_data = hour_mon[i]
            priject_data = project_mon[i]
            print( hour_data, priject_data)
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
            print(projectdata.values)
            if len(projectdata)>0:
                print('if')
                old_data = Empdata.objects.get(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
                old_data.tue = hour_data
                old_data.office_manager = office_manager
                old_data.work_location = work_location
                old_data.status_om = status_om
                total = int(old_data.mon)+int(old_data.tue)+int(old_data.wed)+int(old_data.thu)+int(old_data.fri)+int(old_data.sat)+int(old_data.sun)
                weekly_hours.append(total)
                old_data.total = total
                old_data.totals = sum(weekly_hours)
                old_data.save()
            else:
                print('else_st')
                employeedata=Empdata(emp_id=request.session['id'],status=stat,tue=hour_data,totals=0,hr_id=hr_id, manager_id=manager_id,
                        start=start_dates,end=end_dates,project_name=priject_data,work_location=work_location,office_manager=office_manager,
                        status_om=status_om,name=employee_name,statushr=0,date_created=datetime.now(),assigned='*',mon=0
                        ,wed=0,thu=0,fri=0,sat=0,sun=0)
                totL =  int(employeedata.mon)+int(employeedata.tue)+int(employeedata.wed)+int(employeedata.thu)+int(employeedata.fri)+int(employeedata.sat)+int(employeedata.sun)
                print(totL)
                weekly_hours.append(totL)
                employeedata.total = totL
                employeedata.totals = sum(weekly_hours)
                employeedata.save()
    print(weekly_hours)
    return JsonResponse({'message':'success'})

def wed_data(request):
    emp_id = request.session['id']
    start_dates=request.session['start_date']
    end_dates=request.session['end_date']
    hour_mon = request.GET.getlist('hoursList[]')
    project_mon = request.GET.getlist('projectList[]')
    employee_comment = request.GET.get('empComm')
    createdate = date.today()
    manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
    hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
    employee_name = request.session['name']
    work_location=Login.objects.get(id=request.session['id']).work_location
    office_manager=Login.objects.get(id=request.session['id']).office_manager
    stat=str(0)
    status_om=0
    if work_location== 'IN':
        status_om=1
    if office_manager == manager_id:
        stat=1
        pass
    # print( id,start_dates,end_dates,hour_mon,employee_comment,createdate,project_mon,manager_id,hr_id,employee_name)
    total_h = [int(i) for i in hour_mon]
    weekly_hours=[]
    if sum(total_h)<9 and sum(total_h)>0:
        try:
            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
            existing_rating.enddates = end_dates  
            existing_rating.createdate = createdate 
            existing_rating.hr_id = hr_id  
            existing_rating.manager_id = manager_id  
            existing_rating.emp_comm_wed = employee_comment 
            existing_rating.save()
        except Ratings.DoesNotExist:
            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
            new_rating.enddates = end_dates  
            new_rating.hr_id = hr_id  
            new_rating.manager_id = manager_id  
            new_rating.createdate = createdate  
            new_rating.emp_comm_wed = employee_comment 
            new_rating.save()

        for i in range(0,len(hour_mon)):
            hour_data = hour_mon[i]
            priject_data = project_mon[i]
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=priject_data,start=start_dates,)
            if len(projectdata)>0:
                old_data = Empdata.objects.get(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
                old_data.wed = hour_data
                old_data.office_manager = office_manager
                old_data.work_location = work_location
                old_data.status_om = status_om
                total = int(old_data.mon)+int(old_data.tue)+int(old_data.wed)+int(old_data.thu)+int(old_data.fri)+int(old_data.sat)+int(old_data.sun)
                weekly_hours.append(total)
                old_data.totals = sum(weekly_hours)
                old_data.total = total
                
                old_data.save()
            else:
                employeedata=Empdata(emp_id=request.session['id'],status=stat,totals=0,hr_id=hr_id, manager_id=manager_id,
                        start=start_dates,end=end_dates,project_name=priject_data,work_location=work_location,office_manager=office_manager,
                        status_om=status_om,name=employee_name,statushr=0,date_created=datetime.now(),assigned='*',mon=0,tue=0
                        ,wed=hour_data,thu=0,fri=0,sat=0,sun=0)
                totL =  int(employeedata.mon)+int(employeedata.tue)+int(employeedata.wed)+int(employeedata.thu)+int(employeedata.fri)+int(employeedata.sat)+int(employeedata.sun)
                    
                weekly_hours.append(totL)
                employeedata.total = totL
                employeedata.totals = sum(weekly_hours)
                employeedata.save()
        
    return JsonResponse({'message':'success'})
def thu_data(request):
    emp_id = request.session['id']
    start_dates=request.session['start_date']
    end_dates=request.session['end_date']
    hour_mon = request.GET.getlist('hoursList[]')
    project_mon = request.GET.getlist('projectList[]')
    employee_comment = request.GET.get('empComm')
    createdate = date.today()
    manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
    hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
    employee_name = request.session['name']
    work_location=Login.objects.get(id=request.session['id']).work_location
    office_manager=Login.objects.get(id=request.session['id']).office_manager
    stat=str(0)
    status_om=0
    if work_location== 'IN':
        status_om=1
    if office_manager == manager_id:
        stat=1
        pass
    # print( id,start_dates,end_dates,hour_mon,employee_comment,createdate,project_mon,manager_id,hr_id,employee_name)
    print(hour_mon)
    total_h = [int(i) for i in hour_mon]
    print(total_h)
    weekly_hours=[]
    if sum(total_h)<9 and sum(total_h)>0:
        print('less_thna_9')
        try:
            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
            existing_rating.enddates = end_dates  
            existing_rating.createdate = createdate 
            existing_rating.hr_id = hr_id  
            existing_rating.manager_id = manager_id  
            existing_rating.emp_comm_thu = employee_comment 
            existing_rating.save()
        except Ratings.DoesNotExist:
            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
            new_rating.enddates = end_dates  
            new_rating.hr_id = hr_id  
            new_rating.manager_id = manager_id  
            new_rating.createdate = createdate  
            new_rating.emp_comm_thu = employee_comment 
            new_rating.save()

        for i in range(0,len(hour_mon)):
            hour_data = hour_mon[i]
            priject_data = project_mon[i]
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=priject_data,start=start_dates,)
            if len(projectdata)>0:
                old_data = Empdata.objects.get(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
                old_data.thu = hour_data
                old_data.office_manager = office_manager
                old_data.work_location = work_location
                old_data.status_om = status_om
                total = int(old_data.mon)+int(old_data.tue)+int(old_data.wed)+int(old_data.thu)+int(old_data.fri)+int(old_data.sat)+int(old_data.sun)
                old_data.total = total
                weekly_hours.append(total)
                old_data.totals = sum(weekly_hours)
                old_data.save()
            else:
                employeedata=Empdata(emp_id=request.session['id'],status=stat,totals=0,hr_id=hr_id, manager_id=manager_id,
                        start=start_dates,end=end_dates,project_name=priject_data,work_location=work_location,office_manager=office_manager,
                        status_om=status_om,name=employee_name,statushr=0,date_created=datetime.now(),assigned='*',mon=0,tue=0
                        ,wed=0,thu=hour_data,fri=0,sat=0,sun=0)
                totL =  int(employeedata.mon)+int(employeedata.tue)+int(employeedata.wed)+int(employeedata.thu)+int(employeedata.fri)+int(employeedata.sat)+int(employeedata.sun)
                    
                weekly_hours.append(totL)
                employeedata.total = totL
                employeedata.totals = sum(weekly_hours)
                employeedata.save()
    else:
        pass    
    return JsonResponse({'message':'success'})
def fri_data(request):
    emp_id = request.session['id']
    start_dates=request.session['start_date']
    end_dates=request.session['end_date']
    hour_mon = request.GET.getlist('hoursList[]')
    project_mon = request.GET.getlist('projectList[]')
    employee_comment = request.GET.get('empComm')
    createdate = date.today()
    manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
    hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
    employee_name = request.session['name']
    work_location=Login.objects.get(id=request.session['id']).work_location
    office_manager=Login.objects.get(id=request.session['id']).office_manager
    stat=str(0)
    status_om=0
    if work_location== 'IN':
        status_om=1
    if office_manager == manager_id:
        stat=1
        pass
    # print( id,start_dates,end_dates,hour_mon,employee_comment,createdate,project_mon,manager_id,hr_id,employee_name)
    print(hour_mon,project_mon)
    total_h = [int(i) for i in hour_mon]
    print(sum(total_h))
    weekly_hours=[]
    if sum(total_h)<9 and sum(total_h)>0:
        print('hello_8')
        try:
            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
            existing_rating.enddates = end_dates  
            existing_rating.createdate = createdate 
            existing_rating.hr_id = hr_id  
            existing_rating.manager_id = manager_id  
            existing_rating.emp_comm_fri = employee_comment 
            existing_rating.save()
        except Ratings.DoesNotExist:
            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
            new_rating.enddates = end_dates  
            new_rating.hr_id = hr_id  
            new_rating.manager_id = manager_id  
            new_rating.createdate = createdate  
            new_rating.emp_comm_fri = employee_comment 
            new_rating.save()

        for i in range(0,len(hour_mon)):
            hour_data = hour_mon[i]
            priject_data = project_mon[i]
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=priject_data,start=start_dates,)
            if len(projectdata)>0:
                old_data = Empdata.objects.get(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
                old_data.fri = hour_data
                old_data.office_manager = office_manager
                old_data.work_location = work_location
                old_data.status_om = status_om
                total = int(old_data.mon)+int(old_data.tue)+int(old_data.wed)+int(old_data.thu)+int(old_data.fri)+int(old_data.sat)+int(old_data.sun)
                old_data.total = total
                weekly_hours.append(total)
                old_data.totals = sum(weekly_hours)
                old_data.save()
            
            else:
                employeedata=Empdata(emp_id=request.session['id'],status=stat,totals=0,hr_id=hr_id, manager_id=manager_id,
                        start=start_dates,end=end_dates,project_name=priject_data,work_location=work_location,office_manager=office_manager,
                        status_om=status_om,name=employee_name,statushr=0,date_created=datetime.now(),assigned='*',mon=0,tue=0
                        ,wed=0,thu=0,fri=hour_data,sat=0,sun=0)
                totL =  int(employeedata.mon)+int(employeedata.tue)+int(employeedata.wed)+int(employeedata.thu)+int(employeedata.fri)+int(employeedata.sat)+int(employeedata.sun)
                            
                
                weekly_hours.append(totL)
                employeedata.total = totL
                employeedata.totals = sum(weekly_hours)
                employeedata.save()
    else:
        pass    
    return JsonResponse({'message':'success'})
def sat_data(request):
    emp_id = request.session['id']
    start_dates=request.session['start_date']
    end_dates=request.session['end_date']
    hour_mon = request.GET.getlist('hoursList[]')
    project_mon = request.GET.getlist('projectList[]')
    employee_comment = request.GET.get('empComm')
    createdate = date.today()
    manager_id = EmpDesk.objects.get(login_id=request.session['id']).manager_id
    hr_id = EmpDesk.objects.get(login_id=request.session['id']).hr_id
    employee_name = request.session['name']
    work_location=Login.objects.get(id=request.session['id']).work_location
    office_manager=Login.objects.get(id=request.session['id']).office_manager
    stat=str(0)
    status_om=0
    if work_location== 'IN':
        status_om=1
    if office_manager == manager_id:
        stat=1
        pass
    # print(start_dates,end_dates,hour_mon,employee_comment,createdate,project_mon,manager_id,hr_id,employee_name)
    total_h = [int(i) for i in hour_mon]
    weekly_hours=[]
    if sum(total_h)<9 and sum(total_h)>0:
        try:
            existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_dates)
            existing_rating.enddates = end_dates  
            existing_rating.createdate = createdate 
            existing_rating.hr_id = hr_id  
            existing_rating.manager_id = manager_id  
            existing_rating.emp_comm_sat = employee_comment 
            existing_rating.save()
        except Ratings.DoesNotExist:
            new_rating = Ratings(emp_id=emp_id, startdate=start_dates)
            new_rating.enddates = end_dates  
            new_rating.hr_id = hr_id  
            new_rating.manager_id = manager_id  
            new_rating.createdate = createdate  
            new_rating.emp_comm_sat = employee_comment 
            new_rating.save()

        for i in range(0,len(hour_mon)):
            hour_data = hour_mon[i]
            priject_data = project_mon[i]
            projectdata=Empdata.objects.filter(emp_id=request.session['id'],project_name=priject_data,start=start_dates,)
            if len(projectdata)>0:
                old_data = Empdata.objects.get(emp_id=request.session['id'],project_name=priject_data,start=start_dates)
                old_data.sat = hour_data
                old_data.office_manager = office_manager
                old_data.work_location = work_location
                old_data.status_om = status_om
                total = int(old_data.mon)+int(old_data.tue)+int(old_data.wed)+int(old_data.thu)+int(old_data.fri)+int(old_data.sat)+int(old_data.sun)
                old_data.total = total
                weekly_hours.append(total)
                old_data.totals = sum(weekly_hours)
                old_data.save()
            else:
                employeedata=Empdata(emp_id=request.session['id'],status=stat,totals=0,hr_id=hr_id, manager_id=manager_id,
                        start=start_dates,end=end_dates,project_name=priject_data,work_location=work_location,office_manager=office_manager,
                        status_om=status_om,name=employee_name,statushr=0,date_created=datetime.now(),assigned='*',mon=0,tue=0
                        ,wed=0,thu=0,fri=0,sat=hour_data,sun=0)
                totL =  int(employeedata.mon)+int(employeedata.tue)+int(employeedata.wed)+int(employeedata.thu)+int(employeedata.fri)+int(employeedata.sat)+int(employeedata.sun)
                
                weekly_hours.append(totL)
                employeedata.total = totL
                employeedata.totals = sum(weekly_hours)
                employeedata.save()
        
    return JsonResponse({'message':'success'})






