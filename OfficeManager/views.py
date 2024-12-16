from django.db import connection
import json
from django.core.serializers import serialize
from django.shortcuts import render,redirect
from Employee.models import Empdata,EmpLeaves
from mainlogin.models import Login
from datetime import datetime, timedelta, date
from django.http import HttpResponseRedirect
from ClientManager.models import Notifications,Tasks,TasksChats,TasksLogs,TaskCrew ,PhaseVersion,TaskFiles,Versions,Ratings
from HR.models import LeaveDetails,EmpDesk,ProjectDetails,Manager,Project_team
from cryptography.fernet import Fernet
from django.db.models import DateField, CharField,IntegerField,FloatField,Subquery, OuterRef
from django.db.models.functions import Cast
from django.db.models import Count
# from .models import Ratings
import smtplib
from django.db.models import Q
from email.message import EmailMessage
import ssl
from django.http import JsonResponse
# Create your views here.
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
    

    return(start_date,end_date)

def home(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    print('**************---------------------*************************---------------------------**********************--------------------************')
    if request.session['user']=="5":
        
        request.session['work_location']='IN'
        if request.method=='POST':
           work_location= request.POST.get('work_location')
           request.session['work_location']=work_location
        work_location=request.session['work_location']
        start_date,end_date=weekdates()
        request.session['start_date']=str(start_date)
        request.session['end_date']=str(end_date)
        if request.method=='POST':
            if 'emp_details' in request.POST:
                request.session['emp_details']=request.POST.get('emp_details')
                return redirect('../officemanager/OM_Employee_Details')
        start_date=request.session['start_date']
        end_date=request.session['end_date']
        start_date=datetime.strptime(start_date,"%Y-%m-%d")
        start_date=start_date.date()
        end_date=datetime.strptime(end_date,"%Y-%m-%d")
        end_date=end_date.date()
        emp_ids=Login.objects.filter(work_location=work_location,activation='Active')
        emp_ids=[x.id for x in emp_ids]
        
        empl = EmpDesk.objects.filter(emp_type='3', login_id__in=emp_ids)
        print(empl,'[[[[[[[[[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]]]]]]]]]')
        projects = ProjectDetails.objects.filter(manager_id__in=emp_ids)
        notify = Notifications.objects.filter(manager='1',date=start_date, manager_id=request.session['id'])
        notify = len(notify)
        
        
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
        request.session['start_date']=str(start_date)
        request.session['end_date']=str(end_date)
        approved=Empdata.objects.filter(status=1, manager_id__in=emp_ids,work_location=work_location).values('emp_id', 'start').distinct()
        total_approved=len(approved)
        pending=Empdata.objects.filter(status=4, manager_id__in=emp_ids,work_location=work_location).values('emp_id', 'start').distinct()
        total_pending=len(pending)
        last_month=date.today().month
        last_month=last_month-1
        year=date.today().year
        if last_month == 0:
            last_month=12
            year=year-1

        approved_last = Empdata.objects.annotate(start_month=Cast('start', output_field=DateField())).filter(status=1,manager_id__in=emp_ids,start_month__year=year,start_month__month=last_month).values('emp_id', 'start').annotate(total_approved_last=Count('id')).distinct()

        pending_last = Empdata.objects.annotate(start_month=Cast('start', output_field=DateField())).filter(status=4,manager_id__in=emp_ids,start_month__year=year,start_month__month=last_month).values('emp_id', 'start').annotate(total_pending_last=Count('id')).distinct()
        
        # approved_last = Empdata.objects.annotate(start_month=Cast('start', output_field=DateField())).filter(status=1, manager_id=request.session['id'], start_month__year=year, start_month__month=last_month)
        total_approved_last=len(approved_last)
        # pending_last=Empdata.objects.annotate(start_month=Cast('start', output_field=DateField())).filter(status=4, manager_id=request.session['id'], start_month__year=year, start_month__month=last_month)
        total_pending_last=len(pending_last)

        name = request.session['name']
        
        notifs = []
        noti = []
        
        notif = Notifications.objects.filter(manager='1',date=start_date, manager_id=request.session['id'])
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
        return render(request, 'OM_dashboard.html', {'name': name,'noti':noti,'notify':notify,'total_approved_last':total_approved_last,'total_pending_last':total_pending_last, 'employee':empl,'project':projects,'total_pending':total_pending,'total_approved':total_approved})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_approvedTimesheet(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        # work_location=request.session[work_location]
        # if request.method == 'POST':
        #     work_location=request.POST.get('work_location')
        #     request.session[work_location]=work_location
        # emp_ids=Login.objects.filter(work_location=work_location,activation='Active')
        # emp_ids=[x.id for x in emp_ids]
        start_date=request.session['start_date']
        end_date=request.session['end_date']
        start_date=datetime.strptime(start_date,"%Y-%m-%d")
        end_date=datetime.strptime(end_date,"%Y-%m-%d")
        start_date=start_date.date()
        end_date=end_date.date()
        start = 0
        end_dt = 0
        x = datetime.now().date()
        y = datetime.now().date()
        for i in range(8):
            if x.weekday() == 0:

                start = x
            else:
                x = x - timedelta(days=1, hours=0)
            if y.weekday() == 6:
                end_dt = y
            else:
                y = y + timedelta(days=1, hours=0)
        obj = []
        Name = ''
        name = request.session['name']
        start_dts=start_date.strftime("%Y-%m-%d ")
            
        if request.method=="POST" :
            
            if 'prev' in request.POST:
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
                start_date=start_date.date()
                end_date=end_date.date()

                start_date=start_date- timedelta(days=7, hours=0)
                end_date=end_date- timedelta(days=7, hours=0)


                request.session['start_date']=str(start_date)
                request.session['end_date']=str(end_date)
        
            elif 'next' in request.POST:
                start_date=request.session['start_date']
                end_date=request.session['end_date']
                
                start_date=datetime.strptime(start_date,"%Y-%m-%d")
                end_date=datetime.strptime(end_date,"%Y-%m-%d")
                start_date=start_date+ timedelta(days=7, hours=0)
                end_date=end_date+ timedelta(days=7, hours=0)
                start_date=start_date.date()
                end_date=end_date.date()
                request.session['start_date']=str(start_date)
                request.session['end_date']=str(end_date)
           
            elif 'approve' in request.POST:
                approved=request.POST.get('approve')
                approved=approved.split('|')
                print(approved)
                
                request.session['approved_emp_id'] = approved[0]
                request.session['start_dt'] = approved[1]
                request.session['end_dt'] = approved[2]
                print('hello vlog welcome to my guys')
                return redirect('../officemanager/OM_empTracker_Details')
                
        try:
            hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
        except:
            hr_id=0
        start_dts=start_date.strftime("%Y-%m-%d ")        
        task = Empdata.objects.filter(start=start_date)
        cursor = connection.cursor()
        
        print(f" hr_pending_timesheet_om '{start_date}','1','1','{hr_id}','{request.session['id']}'")
        querry=f" hr_pending_timesheet_om '{start_date}','1','1','{hr_id}','{request.session['id']}'"
        cursor.execute(querry) 
          
        

        pending_timesheet = cursor.fetchall()   
        print(pending_timesheet,'[[[[[[[[[[[[[[[]]]]]]]]]]]]]]]') 
        data = Empdata.objects.all()
        name = request.session['name'] 
        pending=[]
        for i in pending_timesheet:
            designation=EmpDesk.objects.get(login_id=i[1]).designation
            pending.append({'name':i[13],'id':i[1],'designation':designation,'total':i[15],})
        start_date=str(start_date)
        end_date=str(end_date)
        
        return render(request, 'OM_approvedTimesheet.html', {'pending':pending,"task": task, "name": name, 'i': task, 'start': start_date, 'end': end_date})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_leave(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        # manager_id = EmpDesk.objects.get(id=request.session['id']).manager_id
        hr_id = Manager.objects.get(emp_id=request.session['id']).hr_id
        manager_id=request.session['id']
        if request.method=='POST':
            if 'applyLeave' in request.POST:
                print('leave sent-------------*******************---------------')
                leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
                empid=request.session['id']
                empname=request.session['name']
                leavetype=request.POST.get('leaveType')
                fromdt=request.POST.get('fromDate')
                todt=request.POST.get('toDate')
                daytype=request.POST.get('day')
                noofdays=request.POST.get('NumofDays')
                reason=request.POST.get('leaveReason')
                taken=leave_details[0].taken
                remaining=leave_details[0].remaining
                hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
                manager_id=request.session['id']
                
                # noofdays=request.POST.get('noofdays')
                # reason=request.POST.get('reason')
                # taken=leave_details[0].taken
                # remaining=leave_details[0].remaining
                
               
               
                leave_details = EmpLeaves(emp_id=empid,emp_name=empname,leave_type=leavetype,from_dt=fromdt,to_dt=todt,day_type=daytype,no_of_days=noofdays,leave_taken=taken,remaining_leaves=remaining,reason=reason,status='Applied',date_applied=datetime.now().date(),user_type=2,valid_leaves=0,hr_id=hr_id,manager_id=manager_id)
                leave_details.save()
                # hr_id=Manager.objects.filter(emp_id=)
                notify = Notifications(emp_id=request.session['id'],message=f'{request.session["name"]} has applied for leave', date=start_date,current_date=datetime.now().date(), emp=0,hr=1,manager=0,hr_id=hr_id) 
                notify.save()
                sender = 'ats.ariespro@gmail.com'
                # receivers = "karan.rana@ariespro.com"
                receivers = "neelam.vohra@ariespro.com"
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
                print('----------------mail-sent-----------------')
                # with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                #     smtp.login(sender,password)
                #     smtp.sendmail(sender,receivers,server.as_string())
            if 'approve' in request.POST:

                emp_id=int(request.POST.get('approve'))
                
                emp=EmpLeaves.objects.filter(id=emp_id)
                
                j=emp[0]
                leave_type=j.leave_type
                j.status = 'Approved'
                j.save(update_fields=['status'])
                
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your leave ({j.from_dt} - {j.to_dt}) is Approved ',date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                notify.save()
                mail_leave_start= j.from_dt
                mail_leave_end=j.to_dt
                emp_id=emp[0].emp_id
                typ=emp[0].day_type
                noofday=float(emp[0].no_of_days)
               
                leave_start=emp[0].from_dt
                leave_end=emp[0].to_dt
                leave_start= datetime.strptime(leave_start, '%Y-%m-%d')
                leave_end= datetime.strptime(leave_end, '%Y-%m-%d')
                leave_holiday=get_holiday_in_leaves(leave_start,leave_end)
                noofday=noofday-leave_holiday
                emp=LeaveDetails.objects.filter(emp_id=emp_id)
                i=emp[0]
                if leave_type=='Sick Leave':
                    if float(i.sick_day) <= 0:
                        i.sick_day=0
                        i.save(update_fields=['sick_day'])
                    else:
                    
                        sick_day=emp[0].sick_day
                        sick_day=float(sick_day)
                        new_sick_day=(float(sick_day)-noofday)
                        if new_sick_day<0:
                            new_sick_day=0
                        i.sick_day=new_sick_day
                        i.save(update_fields=['sick_day'])
                else:
                    try:
                        days_allowed=float(i.days_allowed)
                        
                    except:
                        days_allowed=0
                    if  days_allowed<= 0:
                        i.days_allowed=0
                        i.save(update_fields=['days_allowed'])
                    else:
                    
                        days_allowed=emp[0].days_allowed
                        days_allowed=float(days_allowed)
                        new_days_allowed=(float(days_allowed)-noofday)
                        if new_days_allowed<0:
                            new_days_allowed=0
                        i.days_allowed=new_days_allowed
                        i.save(update_fields=['days_allowed'])
                
                
                i.taken=(float(emp[0].taken)+noofday)
                i.save(update_fields=['taken'])

                remaning=i.remaining
                
                emp=EmpLeaves.objects.filter(emp_id=emp_id)

                j=emp[0]
                j.remaining_leaves = remaning
                j.save(update_fields=['remaining_leaves'])
                
                try:
                    leave = EmpDesk.objects.filter(login_id = emp_id)
                    l=leave[0]
                    
                    l.leave_taken = (float(leave[0].leave_taken) + noofday)
                    l.save(update_fields=['leave_taken'])
                    l.leave_remaining = (float(leave[0].leave_remaining) - noofday)
                    l.save(update_fields=['leave_remaining'])
                except:
                    pass

                # hr_mail=Login.objects.get(id=hr_id).email
                email=Login.objects.get(id=emp_id).email
                mail_name=Login.objects.get(id=request.session['id']).f_name
                l_name=Login.objects.get(id=request.session['id']).l_name
                mail_name=mail_name+' '+l_name
                sender = 'ats.ariespro@gmail.com'
                # receivers = email
                name_of_emp=Login.objects.get(id=emp_id).f_name
                receivers = email
                # receivers = 'karan.rana@ariespro.com'
                password = 'ahbfhcshjujvkgge'
                Subject= 'Leave Approved'
                
                message = f"""
                Hi {name_of_emp},   
                
                Your leave for ({mail_leave_start} to {mail_leave_end}) is Approved  by {mail_name} 
                
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
                # server['cc']=hr_mail #'neelam.vohra@ariespro.com'

                server.set_content(message)
                if True:
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass
            elif 'reject' in request.POST:
                emp_id=int(request.POST.get('reject'))
                print(emp_id)
                
                emp=EmpLeaves.objects.filter(id=emp_id)
                
                i=emp[0]
                if i.status=='Approved':
                    noofday=float(emp[0].no_of_days)
                    leave_start=emp[0].from_dt
                    leave_end=emp[0].to_dt
                    leave_start= datetime.strptime(leave_start, '%Y-%m-%d')
                    leave_end= datetime.strptime(leave_end, '%Y-%m-%d')
                    leave_holiday=get_holiday_in_leaves(leave_start,leave_end)
                    noofday=noofday-leave_holiday

                    if i.leave_type=='Sick Leave':
                        try:
                            paid_leave_revert=float(i.paid_leaves)
                        except:
                            paid_leave_revert=0
                        paid_leave_revert=paid_leave_revert-leave_holiday
                        leave_taken=float(EmpDesk.objects.get(login_id=i.emp_id).leave_taken)
                        leave_taken=leave_taken-paid_leave_revert
                        
                        if leave_taken<0:
                            leave_taken=0
                        leave_remaining=float(EmpDesk.objects.get(login_id=i.emp_id).leave_remaining)
                        leave_remaining=leave_remaining+paid_leave_revert
                        EmpDesk.objects.filter(login_id=i.emp_id).update(leave_taken=leave_taken,leave_remaining=leave_remaining)
                        try:
                            remaining=float(LeaveDetails.objects.get(emp_id=i.emp_id).remaining)
                        except:
                            remaining=0
                        remaining=remaining+paid_leave_revert
                        try:
                            sick_day=float(LeaveDetails.objects.get(emp_id=i.emp_id).sick_day)
                        except:
                            sick_day=0
                        sick_day=sick_day+paid_leave_revert
                        try:
                            taken=float(LeaveDetails.objects.get(emp_id=i.emp_id).taken)
                        except:
                            taken=0
                        taken=taken-paid_leave_revert
                        if taken<0:
                            taken=0
                        print( remaining,'remaining-------' ,sick_day,'sick_day-------' ,taken,'taken-------' ,noofday,"noofday--" ,leave_holiday,"leave_holiday--")
                        LeaveDetails.objects.filter(emp_id=i.emp_id).update(remaining=remaining,sick_day=sick_day,taken=taken)
                    else:
                        try:
                            paid_leave_revert=float(i.paid_leaves)
                        except:
                            paid_leave_revert=0
                        paid_leave_revert=paid_leave_revert-leave_holiday
                        try:
                            leave_taken=float(EmpDesk.objects.get(login_id=i.emp_id).leave_taken)
                        except:
                            leave_taken=0
                        leave_taken=leave_taken-paid_leave_revert
                        
                        if leave_taken<0:
                            leave_taken=0
                        try:
                            leave_remaining=float(EmpDesk.objects.get(login_id=i.emp_id).leave_remaining)
                        except:
                            leave_remaining=0
                        leave_remaining=leave_remaining+paid_leave_revert
                        EmpDesk.objects.filter(login_id=i.emp_id).update(leave_taken=leave_taken,leave_remaining=leave_remaining)
                        try:
                            remaining=float(LeaveDetails.objects.get(emp_id=i.emp_id).remaining)
                        except:
                            remaining=0
                        remaining=remaining+paid_leave_revert
                        try:
                            days_allowed=float(LeaveDetails.objects.get(emp_id=i.emp_id).days_allowed)
                        except:
                            days_allowed=0
                        days_allowed=days_allowed+paid_leave_revert
                        try:
                            taken=float(LeaveDetails.objects.get(emp_id=i.emp_id).taken)
                        except:
                            taken=0
                        taken=taken-paid_leave_revert
                        if taken<0:
                            taken=0
                        print( remaining,'remaining-------' ,days_allowed,'days_allowed-------', taken,'taken-------',noofday,"noofday--" ,leave_holiday,"leave_holiday--")
                        LeaveDetails.objects.filter(emp_id=i.emp_id).update(remaining=remaining,days_allowed=days_allowed,taken=taken)

             
                i.status='Rejected'
                i.save(update_fields=['status'])

                manage_attendance(request,i)
                j=emp[0]
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your leave ({j.from_dt} - {j.to_dt}) is Rejected',date=start_date,current_date=datetime.now().date(),hr_id=request.session['id'])
                notify.save()
                emp_id=j.emp_id

                #emp[0].note=request.POST.get('note')
                #emp[0].save(update_fields=['note'])
                
                email=Login.objects.get(id=emp_id).email
                mail_name=Login.objects.get(id=request.session['id']).f_name
                l_name=Login.objects.get(id=request.session['id']).l_name
                mail_name=mail_name+' '+l_name
                sender = 'ats.ariespro@gmail.com'
                # receivers = email
                name_of_emp=Login.objects.get(id=emp_id).f_name
                receivers = email
                # receivers = 'karan.rana@ariespro.com'
                password = 'ahbfhcshjujvkgge'
                Subject= 'Leave Rejected'
                
                message = f"""
                Hi {name_of_emp},   
                
                Your leave for ({j.from_dt} to {j.to_dt}) is Rejected  by {mail_name} 
                
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
                # server['cc']=hr_mail #'neelam.vohra@ariespro.com'

                server.set_content(message)
                try :
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                except:
                    pass
            
        # name = request.session['name']
        # leaves_detail=EmpLeaves.objects.all()
        leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
        sl=[]
        pl=[]
        leaves_detail=EmpLeaves.objects.filter(user_type='3').order_by('-id')
        if request.session['work_location']=='US':
            leaves_detail=EmpLeaves.objects.filter(user_type='3').order_by('-id')
            
        leave_details=LeaveDetails.objects.filter(emp_id=request.session['id'])
        for i in leaves_detail:
            detail=LeaveDetails.objects.filter(emp_id=i.emp_id)
            sl.append(detail[0].sick_day)
            pl.append(detail[0].days_allowed)
        # leaves_detail = zip(leaves_detail,leave_details)
        print(leaves_detail)
        if len(leave_details) == 0:
            # pass
            remaining = ''
            taken = ''
            name  = ''
            leaves = ''
            sick_leave=''
            
        else:
            remaining=leave_details[0].remaining
            taken=leave_details[0].taken
            sick_leave=leave_details[0].sick_day

        leaves=zip(sl,pl,leaves_detail)
        name=request.session['name']
        # if len(leave_details) == 0:
        #     remaining = 0
        #     taken = 0
        # else:
        #     remaining=leave_details[0].remaining
        #     taken=leave_details[0].taken
        manager_sl=sick_leave
        manager_pl=remaining
        try:
            manager_sl=LeaveDetails.objects.get(emp_id=request.session['id']).sick_day

        except:
            manager_sl=0
        try:
            manager_pl=LeaveDetails.objects.get(emp_id=request.session['id']).days_allowed
        except:
            manager_pl=0
        emp_leaves=EmpLeaves.objects.filter(emp_id=request.session['id']).order_by('-id')
        print(manager_sl,manager_pl)
        return render(request, 'OM_leave.html', {'emp_leaves':emp_leaves,'manager_sl':manager_sl, 'manager_pl':manager_pl,'name': name,'leaves_detail':leaves,'remaining':leaves,'taken':leaves})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_EditProfile(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":

        message1 = ''
        message = ''
        cmPro = Login.objects.filter(id=request.session['id'])
        try:
            cmPro = cmPro[0]
        except:
            pass

        if request.method == 'POST':
            if 'editProfile' in request.POST:

                data = Login.objects.filter(id=request.session['id'])
                
                data = data[0]                    
                data.email=request.POST.get('email')
                data.save(update_fields=['email'])
                data.mobile=request.POST.get('mobileNo')
                data.save(update_fields=['mobile'])
                data.address=request.POST.get('addr')
                data.save(update_fields=['address'])
                
                data = Login.objects.filter(id=request.session['id'])
                data = data[0]
            
                data.email=request.POST.get('email')
                data.save(update_fields=['email'])
                data.mobile=request.POST.get('mobileNo')
                data.save(update_fields=['mobile'])
                data.address=request.POST.get('addr')
                data.save(update_fields=['address'])
                print(len(request.FILES))
                print(request.FILES,'hello world')
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
                        cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                        ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                        print(ciphered_text) 
                        pwd=ciphered_text.decode()
                        data.password=pwd
                        data.save(update_fields=['password'])

                    else:
                        message1 = 'password and confirm password must be same.'
                elif pwd == request.POST.get('currPass'):
                    if request.POST.get('password') == request.POST.get('confirmPass'):

                        cipher_suite = Fernet('PCHl_MjGyEyBxLYha3S-cWg_SDDmjT4YYaKYh4Z7Yug=')
                        ciphered_text = cipher_suite.encrypt(bytes(request.POST.get('password') ,encoding='utf8')) 
                        print(ciphered_text) 
                        pwd=ciphered_text.decode()
                        data.password=pwd
                        data.save(update_fields=['password'])

                    else:
                        message1 = 'password and confirm password must be same.'

                else:
                    message = 'current password is incorrect'

        message1 = ''
        message = ''
        cmPro = Login.objects.filter(id=request.session['id'])
        try:
            cmPro = cmPro[0]
        except:
            pass
        
        name = request.session['name']
        return render(request, 'OM_EditProfile.html', {'name': name,'cm':cmPro, 'message':message,'message1':message1})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_notification(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        if request.method=='POST':
            if 'clear' in request.POST:
                notif = Notifications.objects.filter(manager='1',date=start_date,manager_id=request.session['id'])
                for i in notif:
                    i.manager='2'
                    i.save(update_fields=['manager'])
                    print(i)
        leave_details = EmpLeaves.objects.filter(from_dt=datetime.now().date(),status='Approved',manager_id=request.session['id'])
        for leaves in leave_details:
            obj=Notifications.objects.filter(message=f'{leaves.emp_name} is on leave today ({datetime.now().date()}) for {leaves.no_of_days} days',manager_id=request.session['id'])  
            if len(obj)>0:
                obj.delete()
            notify = Notifications(emp_id=leaves.emp_id,message=f'{leaves.emp_name} is on leave today ({datetime.now().date()}) for {leaves.no_of_days} days',emp=0,hr=0,manager=1,date=start_date,current_date=datetime.now().date(),manager_id=request.session['id'])
            notify.save()
        notif = Notifications.objects.filter(manager='1',date=start_date,manager_id=request.session['id'])
        name = request.session['name']
        return render(request, 'OM_notification.html', {'name': name,'notif':notif})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_pendingTimesheet(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        start_date=request.session['start_date']
        end_date=request.session['end_date']
        start_date=datetime.strptime(start_date,"%Y-%m-%d")
        end_date=datetime.strptime(end_date,"%Y-%m-%d")
        start_date=start_date.date()
        end_date=end_date.date()


        # global start_date
        # global end_date
        start = 0
        end_dt = 0
        x = datetime.now().date()
        y = datetime.now().date()
        for i in range(8):
            if x.weekday() == 0:

                start = x
            else:
                x = x - timedelta(days=1, hours=0)
            if y.weekday() == 6:
                end_dt = y
            else:
                y = y + timedelta(days=1, hours=0)
        name = request.session['name']
        obj = []
        totals = 0
        Name = ''
        ns=[]
        count = 0
        task = Empdata.objects.filter(start=start_date,status='1')
        for i in task:
            if i.name == Name:
                totals = totals+i.total
                continue
            else:
                ns.append(i.project_name)
                obj.append(i)
                Name = i.name
                totals = i.total
        
        if request.method=="POST" and ('prev' in request.POST or 'next' in request.POST):
            
                if 'prev' in request.POST:
                    start_date=request.session['start_date']
                    end_date=request.session['end_date']
                    
                    start_date=datetime.strptime(start_date,"%Y-%m-%d")
                    end_date=datetime.strptime(end_date,"%Y-%m-%d")
                    start_date=start_date.date()
                    end_date=end_date.date()

                    start_date=start_date- timedelta(days=7, hours=0)
                    end_date=end_date- timedelta(days=7, hours=0)


                    request.session['start_date']=str(start_date)
                    request.session['end_date']=str(end_date)
            # do subscribe
                elif 'next' in request.POST:
                    start_date=request.session['start_date']
                    end_date=request.session['end_date']
                    
                    start_date=datetime.strptime(start_date,"%Y-%m-%d")
                    end_date=datetime.strptime(end_date,"%Y-%m-%d")
                    start_date=start_date+ timedelta(days=7, hours=0)
                    end_date=end_date+ timedelta(days=7, hours=0)
                    start_date=start_date.date()
                    end_date=end_date.date()
                    request.session['start_date']=str(start_date)
                    request.session['end_date']=str(end_date)
                Name = ''
                obj = []
                for i in task:
                    if i.name == Name:
                        totals = totals+i.total
                        continue
                    else:
                
                        obj.append(i)
                        Name = i.name
                        totals = i.total
        elif request.method == "POST":
            
            e_id = 0
            names=''
            if 'pending' in request.POST:
                
                emp_id=request.POST.get('pending')
                data=Empdata.objects.filter(emp_id=emp_id,start=start_date)
                try:
                    start=data[0].start
                    end=data[0].end
                    end= datetime.strptime(end, "%Y-%m-%d")
                    start= datetime.strptime(start, "%Y-%m-%d")
                    projects=Project_team.objects.filter(employee_id=request.session['approved_emp_id'])
                    projects=[x.project for x in projects]
                    task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
                except:
                    task=[]
                try:
                    starts=data[0].start
                except:
                    starts=start_date
                name = request.session['name']
                try:
                    emp_name=data[0].name
                except:
                    emp_name=''
                try:
                    employee_id=data[0].emp_id
                except:
                    employee_id=emp_id
                try:
                    employee_start=data[0].start
                except:
                    employee_start=start_date
                try:
                    employee_end=data[0].end
                except:
                    employee_end=''
                des=EmpDesk.objects.filter(login_id=emp_id)
                try:
                    designation=des[0].designations
                except:
                    designation=''
                
                try:
                    img=Login.objects.filter(id=emp_id)
                    img=img[0].image
                    print(img)
                except:
                    img='static/uploads/images.jpg'
                    print(img,'except')
                try :
                   
                    comments=Ratings.objects.get(emp_id=emp_id,startdate=start_date).employee_comment
                except :
                    comments=''

                return render(request, 'OM_empTracker.html',{'comments':comments,'img':img,'name': name,'designation':designation,'data':data,'date':starts,'emp_id':emp_id,'count': count, 'start_date': start_date, 'end_date': end_date ,'emp_name':emp_name ,"employee_id":employee_id, 'employee_start':employee_start,'employee_end':employee_end,'tasks':task })

            elif 'denied' in request.POST:
                
                emp_id=request.POST.get('denied')
                date_start=request.POST.get('date_start')
                
                
                data=Empdata.objects.filter(emp_id=emp_id,start=start_date)
                if len(data)>0:
                    starts=data[0].start
                    name = request.session['name']
                    emp_name=data[0].name
                    employee_id=data[0].emp_id
                    employee_start=data[0].start
                    employee_end=data[0].end

            elif 'Deny' in request.POST:
                
                emp_id=request.POST.get('empid')
                names=''
                hr_id=EmpDesk.objects.get(login_id=emp_id).hr_id
                e_id = request.POST.get('Deny')
                
                t = Empdata.objects.filter(emp_id=emp_id,start=start_date)
                j = t[0]
                for i in t:
                    if i.status=="2":
                        pass #i.delete()
                    else:
                        names=i.name
                        i.status = '2'
                        
                        i.save(update_fields=['status'])
                        i.status_om = '2'

                        i.save(update_fields=['status_om'])
                        
                    task = Empdata.objects.all()
                obj=Notifications.objects.filter(emp_id=j.emp_id,message=f'Your Timesheet for Week ({j.start} - {j.end}) is Rejected by the Office Manager Today ({datetime.now().date()}) ',manager_id=request.session['id'])  
                if len(obj)>0:
                    obj.delete()
                notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your Timesheet for Week ({j.start} - {j.end}) is Rejected by the Office Manager Today ({datetime.now().date()}) ',emp_name=j.name,date=start_date,current_date=datetime.now().date(),manager_id=request.session['id'])
                notify.save()
                hr_mail=Login.objects.get(id=hr_id).email
                email=Login.objects.filter(id=emp_id)
                email=[x.email for x in email]

                email.append(hr_id)
                name=Login.objects.get(id=request.session['id']).f_name
                l_name=Login.objects.get(id=request.session['id']).l_name
                name=name+' '+l_name
                sender = 'ats.ariespro@gmail.com'
                # receivers = email

                name_of_emp=Login.objects.get(id=emp_id).f_name
                receivers = email
                receivers = 'karan.rana@ariespro.com'
                password = 'ahbfhcshjujvkgge'
                Subject= 'Timesheet Rejected'
                
                message = f"""
                Hi {name_of_emp},   
                
                Your Timesheet for period {start_date} to {end_date}  is Rejected by {name} 
                
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
                # server['cc']=hr_mail #'neelam.vohra@ariespro.com'

                server.set_content(message)
                if True:
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass

            elif 'Approve' in request.POST:
                emp_id=request.POST.get('empid')
                rating=request.POST.get('rating')
                createdate=date.today()
                hr_id=EmpDesk.objects.get(login_id=emp_id).hr_id
                manager_id=EmpDesk.objects.get(login_id=emp_id).manager_id
                manager_comment=request.POST.get('comment')
                print(rating,'rating')
                print(createdate,'createdate')
                print(hr_id,'hr_id')
                print(manager_id,'manager_id')
                print(manager_comment,'manager_comment')

                
                
                print(emp_id)
                e_date= request.POST.get('Approve')
                print(emp_id,e_date)
                # Ratings.objects.create(emp_id=emp_id,startdate=start_date,)
                try:
                    existing_rating = Ratings.objects.get(emp_id=emp_id, startdate=start_date)
                    # If a row with the same emp_id and startdate exists, update it
                    existing_rating.rating = rating  # Update the fields you want to change
                    existing_rating.createdate = createdate  # Update the fields you want to change
                    existing_rating.hr_id = hr_id  # Update the fields you want to change
                    existing_rating.manager_id = manager_id  # Update the fields you want to change
                    existing_rating.manager_comment = manager_comment  # Update the fields you want to change
                    existing_rating.save()
                except Ratings.DoesNotExist:
                    # If a row with the specified emp_id and startdate does not exist, create a new one
                    new_rating = Ratings(emp_id=emp_id, startdate=start_date)
                    # Set other fields of the new_rating as needed
                    new_rating.rating = rating  # Set other fields here
                    new_rating.createdate = createdate  # Set other fields here
                    new_rating.hr_id = hr_id  # Set other fields here
                    new_rating.manager_id = manager_id  # Set other fields here
                    new_rating.manager_comment = manager_comment  # Set other fields here
                    new_rating.save()
                Empdata.objects.filter(emp_id=emp_id,start=str(start_date)).update(status_om=1)

                t = Empdata.objects.filter(emp_id=emp_id,start=str(start_date))
                j = t[0]
                name_of_emp=Login.objects.get(id=emp_id).f_name
                email=Login.objects.filter(id=emp_id)
                email=[x.email for x in email]
                hr_mail=Login.objects.get(id=hr_id).email
                email.append(hr_mail)
                email='karan.rana@ariespro.com'
                # for i in t:
                                    
                #     i.status = '1'
                    
                #     i.save(update_fields=['status'])
                obj=Notifications.objects.filter(emp_id=j.emp_id,message=f'Your Timesheet for Week ({j.start} - {j.end}) is Approved by the Office Manager Today ({datetime.now().date()}) ',manager_id=request.session['id'])  
                # if len(obj)>0:
                #     obj.delete()
                # notify=Notifications(emp_id=j.emp_id,emp=1,hr=0,manager=0, message=f'Your Timesheet for Week ({j.start} - {j.end}) is Approved by the Manager Today ({datetime.now().date()}) ',emp_name=j.name,date=start_date,current_date=datetime.now().date(),manager_id=request.session['id'])
                # notify.save()
                sender = 'ats.ariespro@gmail.com'
                receivers = email
                
                receivers = email
                password = 'ahbfhcshjujvkgge'
                Subject= 'Timesheet Approved'
                
                message = f"""

                Hi {name_of_emp},   
                
                Your Timesheet for period {start_date} to {end_date}  is Approved by Office Manager 
                
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
                # server['cc']=hr_mail #'neelam.vohra@ariespro.com'

                server.set_content(message)
                if True:
                    context=ssl.create_default_context()
                    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
                        smtp.login(sender,password)
                        smtp.sendmail(sender,receivers,server.as_string())
                else:
                    pass


                task = Empdata.objects.all()

            Name = []
        
            task= Empdata.objects.filter(start=start_date,status='2')
            print(start_date)
            obj = []
            designations=[]
            for i in task:
                if i.name in Name:
                    totals = totals+i.total
                    continue
                else:
                    eid=i.emp_id
                    
                    des=EmpDesk.objects.filter(login_id=eid)
                    designation=des[0].designations
                    
                    designations.append(designation)               
                    obj.append(i)
                    Name.append(i.name)
                    totals = i.total
            rtask= Empdata.objects.filter(start=start_date,status='2')
            print(start_date,obj)
            robj = []
            rName=[]
            print(rtask)
            rdesignations=[]
            totalls=[]
            for i in rtask:
                if i.name in rName:
                    totals = totals+i.total
                    continue
                else:
                    eid=i.emp_id
                    
                    rdes=EmpDesk.objects.filter(login_id=eid)
                    rdesignation=rdes[0].designations
                    
                    rdesignations.append(rdesignation)               
                    robj.append(i)
                    rName.append(i.name)
                    totals = i.total
                totalls.append(totals)
            # robj = zip(robj,rdesignations) 
            obj = zip(obj,designations,totalls) 
            name = request.session['name']
            task = Empdata.objects.all()
            print('yessssss',robj)
        try:
            hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
        except:
            hr_id=0
            
        cursor = connection.cursor()
        print(f"-------------------------------  hr_pending_timesheet_om '{start_date}','1','0','{hr_id}','{request.session['id']}'----------------------------------")
        
        cursor.execute(f" hr_pending_timesheet_om '{start_date}','1','0','{hr_id}','{request.session['id']}'") 
        print(f"-------------------------------  hr_pending_timesheet_om '{start_date}','1','0','{hr_id}','{request.session['id']}'----------------------------------")
        
        pending_timesheet = cursor.fetchall()  
        print(cursor) 
        print(pending_timesheet)    
        data = Empdata.objects.all()
        name = request.session['name'] 
        pending=[]
        for i in pending_timesheet:
            designation=EmpDesk.objects.get(login_id=i[1]).designations
            pending.append({'name':i[13],'id':i[1],'designation':designation,'total':i[15]})
        start_date=str(start_date)
        end_date=str(end_date)
        return render(request, 'OM_pendingTimesheet.html', {'pending':pending,"task": task, "name": name, 'obj': obj, 'count': count, 'start_date': start_date, 'end_date': end_date})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_profile(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        name = request.session['name']

        profileData = Login.objects.filter(id=request.session['id'])
        try:
            profileData = profileData[0]
        except:
            pass
        return render(request, 'OM_profile.html', {'name': name,'profile':profileData})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_empTracker(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        if 'pending' in request.POST:
            pass
        
        name = request.session['name']
        return render(request, 'OM_empTracker.html', {'name': name})
    else:
        response=HttpResponseRedirect('../../')
        return response
    
def OM_empTracker_Details(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        start_date_str = request.session['start_dt']
        print(start_date_str)
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
        empdesk=EmpDesk.objects.filter(login_id=request.session['approved_emp_id'])
        try:
            empdesk=empdesk[0]
        except:
            pass
        try:
            img=Login.objects.get(id=request.session['approved_emp_id']).image
            
        except:
            img=''
        data=Empdata.objects.filter(emp_id=request.session['approved_emp_id'],start=start_date)
        try:
            start=data[0].start
            end=data[0].end
            end= datetime.strptime(end, "%Y-%m-%d")
            start= datetime.strptime(start, "%Y-%m-%d")
            projects=Project_team.objects.filter(employee_id=request.session['approved_emp_id'])
            projects=[x.project for x in projects]
            task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        except:
            task=[]
        try :
            comments=Ratings.objects.get(emp_id=request.session['approved_emp_id'],startdate=start_date).employee_comment
        except :
            comments=''
        return render(request, 'OM_empTracker_Details.html',{'comments':comments,'data':data,'empdesk':empdesk,'img':img,'tasks':task})   
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_team(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
    
        if request.method=='POST':
            
            if 'addEmp' in request.POST:
                project=request.POST.get('project')
                employee_name=request.POST.get('employee')
                # employee_name=employee_name.split(' ')

                print(project,'vlogs')
                manager_selected=request.POST.get('manager')
                teams=ProjectDetails.objects.filter(project_name=project)
                team='Team'+str(teams[0].id)

                emp_id=employee_name
                


                designation=EmpDesk.objects.filter(login_id=emp_id)
                managers=ProjectDetails.objects.filter(project_name=project)
                designations=designation[0].designations
                
                manager=managers[0].manager
                employee_name=Login.objects.get(id=emp_id).user_name
                employee_f_name=Login.objects.get(id=emp_id).f_name
                
                manager_id=EmpDesk.objects.get(login_id=emp_id).manager_id
                hr_id=EmpDesk.objects.get(login_id=emp_id).hr_id


                
                obj=Project_team.objects.filter(project=project,employee_name=employee_name,designation=designations)
                
                if len(obj)>0:
                    pass
    
                else:
                    teams=ProjectDetails.objects.filter(project_name=project)
                    
                    team=teams[0].team
                    print(team)
                    
                    a=Project_team(project=project,team=team,employee_id=emp_id,employee_name=employee_name,manager=manager_selected,designation=designations,crt_date=datetime.now().date(),hr_id=hr_id)
                    a.save()
                    start_date,end_date=weekdates()
                    employeedata=Empdata.objects.filter(emp_id=emp_id,  start=start_date,end=end_date,project_name=project,
                                        )
                    if len(employeedata) >0:
                        Empdata.objects.filter(emp_id=emp_id,  start=start_date,end=end_date,project_name=project,
                                         ).update(assigned='*')
                    else:
                        employeedata=Empdata(emp_id=emp_id,status=0,mon=0,tue=0,wed=0,thu=0,fri=0,sat=0,sun=0,total=0,totals=0,  start=start_date,end=end_date,project_name=project,
                                         name=employee_f_name,statushr=0,date_created=datetime.now(),assigned='*',hr_id=hr_id,manager_id=manager_id)
                        employeedata.save()
            elif 'remove' in request.POST:
                remove_id=request.POST.get('remove')
                remove=Project_team.objects.filter(id=remove_id)
                remove.delete()
            elif 'project_name' in request.POST:
                request.session['project_name']=request.POST.get('project_name')
                response=HttpResponseRedirect('/officemanager/OM_phase')
                return response
                  
        managers=Manager.objects.all()
        projects=ProjectDetails.objects.filter(manager_id=request.session['id'])
        manager_name= Manager.objects.get(emp_id=request.session['id']).name  
        team=Project_team.objects.filter(manager=manager_name)
        name=request.session['name']
        employees=EmpDesk.objects.filter(emp_type='3',activation='Active')
        project=[]
        pending=[]
        development=[]
        completed=[]
        for i in projects:
            project.append(i)
            pending.append(len(Tasks.objects.filter(status='Task List',project_id=i.project_name)))
            development.append(len(Tasks.objects.filter(status='Development',project_id=i.project_name)))
            completed.append(len(Tasks.objects.filter(status='Completed',project_id=i.project_name)))
        projects=zip(project, pending, development,  completed)
        return render(request,'OM_team.html',{'name':name,'team':team,'employees':employees,'managers':managers,"projects":projects})
    else:
        response=HttpResponseRedirect('../../')
        return response
    
def OM_projects(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        
        managers=Manager.objects.all()
        if 'project_id' in request.POST:
            request.session['project_name']=str(request.POST.get('project_id'))
            print(request.POST.get('project_id'),'-----------------------',request.session['project_name'])
            response=HttpResponseRedirect('/officemanager/OM_phase')
            return response    
        elif request.method=='POST':
            project=request.POST.get('project')
            client=request.POST.get('client')
            
            if 'add' in request.POST:
                date=request.POST.get('date')
                manager=request.POST.get('manager')
                
                managerss=Manager.objects.get(emp_id=manager).name
                hr_id=Manager.objects.get(emp_id=manager).hr_id
                a=ProjectDetails(project_name=project,client_name=client,manager_id=manager,start_date=date,status='PENDING',manager=managerss,crt_date=datetime.now().date(),hr_id=hr_id)
                a.save()
            if 'edit' in request.POST:
                edit=request.POST.get('edit')
                project_edit=request.POST.get(f'project_edit{edit}')
                client_edit=request.POST.get(f'client_edit{edit}')
                Project_team.objects.filter(project=ProjectDetails.objects.filter(id = edit).first().project_name).update(project = project_edit)
                Tasks.objects.filter(project_id=ProjectDetails.objects.filter(id = edit).first().project_name).update(project_id = project_edit)
                TasksLogs.objects.filter(project_id=ProjectDetails.objects.filter(id = edit).first().project_name).update(project_id = project_edit)
                Empdata.objects.filter(project_name=ProjectDetails.objects.filter(id = edit).first().project_name).update(project_name = project_edit)
                PhaseVersion.objects.filter(project=ProjectDetails.objects.filter(id = edit).first().project_name).update( project = project_edit) 
                ProjectDetails.objects.filter(id=edit).update( project_name= project_edit, client_name= client_edit)                                                  
                                                                    
            

        project=ProjectDetails.objects.all()   
        name=request.session['name']
        return render(request,'OM_projects.html',{'name':name,'project':project,'managers':managers})
    else:
        response=HttpResponseRedirect('../../')
        return response

def OM_Project_task(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        response=HttpResponseRedirect('../../')
        return response
    if request.session['user']=="5":
        pass
    else:
        response=HttpResponseRedirect('../../')
        return response
    task_id=request.session['project_name']
    if 'add_Task' in request.POST:

        project_name=request.session['project_name']
        project_id=project_name
        print(project_name)
        try:
            team_id=Project_team.objects.filter(project=project_name).first().team
        except:
            team_id=''
        task_heading=request.POST.get('task_heading')
        description=request.POST.get('task')

        assigning_date=date.today()
        target_date=request.POST.get('date')
        task_crew=request.POST.getlist('task_crew')
        task_type=request.POST.get('type')
        priority=request.POST.get('priority')


        description = description.split('\n')

        # Add <br> at the end of each line
        description = [line + '<br>' for line in description]

        # Join the lines back together with <br>
        description = ''.join(description)









        print(description,'-----------------------')
        complete_date=''
        manager_id=request.session['id']
        hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
        status='Task List'
        crt_date=datetime.now()
        projec_task_id=Tasks.objects.filter(project_id=project_id)
        projec_task_id=len(projec_task_id)
        projec_task_id=projec_task_id+1

        phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project_name)
        phase=[x.phase_float for x in phase_value]
        phase=max(phase)
        phase=int(phase)
        version=[x.version_float for x in phase_value]
        version=max(version)
    
        Tasks.objects.create(project_id=project_id,team_id=team_id,description=description,assigning_date=assigning_date,
            target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date,
            ui=' '  ,database=' ' ,backend=' ',projec_task_id=projec_task_id,phase=phase,project_version=version,task_heading=task_heading,
            task_type=task_type, priority=priority)

        task_id=Tasks.objects.filter(project_id=project_id,description=description,assigning_date=assigning_date,
            target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date).first()
        task_id=task_id.id
        
        for employee in task_crew:
            obj=TaskCrew.objects.filter(task_id=task_id,employee_name=employee)
            if len(obj)>0:
                pass
            else:
                TaskCrew.objects.create(task_id=task_id,employee_name=employee,create_date=datetime.now(),status='Task List')
        if True:
            print(request.FILES)
            uploaded_files = request.FILES.getlist('attachments')
            image_name=[]
            print(uploaded_files)
            for uploaded_file in uploaded_files:
                if uploaded_file is not None:
                    id_gen=str(task_id)
                    image=id_gen+uploaded_file.name
                    image=image.replace(' ','')
                    file_path = fr'static/uploads/task_files/{image}'
                    with open(file_path, 'wb') as file:
                        for chunk in uploaded_file.chunks():
                            file.write(chunk)
                    TaskFiles.objects.create(task_id=task_id,file_name=image,create_date=datetime.now())
        else:
            pass
        
        TasksLogs.objects.create(project_id=project_id, task_id=task_id, from_status='Task List', to_status='Task List', 
            assigning_date=assigning_date, target_date=target_date, complte_date=complete_date, manager_id=manager_id, user_id=request.session['id'], crt_date=crt_date,)
    
    task_ids=Tasks.objects.filter(project_id=request.session['project_name'])
    task_ids=[x.id for x in task_ids] 
    project_team=Project_team.objects.filter(project=request.session['project_name']) 
    chats=TasksChats.objects.filter(task_id__in=task_ids).annotate(tasks_id=Cast('task_id', output_field=IntegerField())).exclude(description=None).order_by('id')
    last_id=[x.id for x in chats]
    try:
        last_id=last_id[-1]
    except:
        last_id=0
    request.session['last_id']=last_id

    tasks_list=Tasks.objects.filter(status='Task List',project_id=request.session['project_name'])
    development=Tasks.objects.filter(status='Development',project_id=request.session['project_name'])
    completed=Tasks.objects.filter(status='Completed',project_id=request.session['project_name'])
    # print(chats)

    tasks_list=Tasks.objects.filter(status='Task List',project_id=request.session['project_name']).order_by('-id')
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
    all_crew=[]
    employees=EmpDesk.objects.filter(manager_id=request.session['id'],activation='Active')
    for i in tasks_list:
        all_crews=[]
        tasks_list_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        tasks_list_log=len(tasks_list_logs)
        task_list.append(i)
        task_list_logs.append(tasks_list_log+1)
        chat=TasksChats.objects.filter(task_id=i.id)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
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
        if len(crews)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)

        for cr in crews:
            if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                all_crews.append(cr.employee_name)
        for em in employees:
            if em.email in all_crews:
                pass
            else:
                all_crews.append(em.email)
        all_crew.append(all_crews)
   
    tasks_list=zip(task_list,task_list_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments,all_crew)        

    developments=Tasks.objects.filter(status='Development',project_id=request.session['project_name']).order_by('-id')
    development=[]
    developments_logs=[]
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
    all_crew=[]
    for i in developments:
        all_crews=[]
        development_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed')
        development_log=len(development_logs)
        development.append(i)
        developments_logs.append(development_log+1)
        task_chat.append(TasksChats.objects.filter(task_id=i.id))
        task_crew.append(TaskCrew.objects.filter(task_id=i.id))
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
        if len(crews)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        
        for cr in crews:
            if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                all_crews.append(cr.employee_name)
        for em in employees:
            if em.email in all_crews:
                pass
            else:
                all_crews.append(em.email)
        all_crew.append(all_crews)
    development=zip(development,developments_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments,all_crew)  
    
    completeds=Tasks.objects.filter(status='Completed',project_id=request.session['project_name']).order_by('-id')
    completed=[]
    completedt_logs=[]
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
    all_crew=[]
    for i in completeds:
        all_crews=[]
        completed_logs=TasksLogs.objects.filter(task_id=i.id,from_status='Completed').order_by('id')
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
        if len(crews)==0:
            crew.append(Project_team.objects.filter(project=i.project_id))
        else:
            crew.append(TaskCrew.objects.filter(task_id=i.id))

        task_chats.append(TasksChats.objects.filter(task_id=i.id))
        task_logs.append(TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=i.id))
        attachments.append(TaskFiles.objects.filter(task_id=i.id))
        tasks.append(i)
        
        for cr in crews:
            if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                all_crews.append(cr.employee_name)
        for em in employees:
            if em.email in all_crews:
                pass
            else:
                all_crews.append(em.email)
        all_crew.append(all_crews)
    completed=zip(completed,completedt_logs,logs,task_chat,task_crew,tasks ,crew ,task_chats ,task_logs ,attachments,all_crew)
    
    project_team_task=[x.employee_name for x in project_team]

    return render(request, "OM_Project_task.html" ,{'project_team_task':project_team_task,'employees':employees,'project_team':project_team, 'tasks_list':tasks_list, 'development':development, 'completed':completed,'chats':chats})

def task_chat(request):
   
    try:
        pass
    except:
        pass
    chat=request.POST.get('chat')
    task_id=request.POST.get('task_id')
    print(chat)
    if chat != '':
        team_id=''
        description=chat
        status='pending'
        crt_date=datetime.now()
        user_name= request.session['name']
        user_id=request.session['id']
        TasksChats.objects.create(task_id=task_id,team_id=team_id,description=description,status=status,crt_date=crt_date,user_name=user_name,user_id=user_id)


        tasks_chats=TasksChats.objects.filter(task_id=task_id).order_by('-id')
        request.session['last_id']=str(tasks_chats[0].id)
        serialized_data = serialize('json', tasks_chats)
        print('------------------------last -----')
        # Convert the serialized data to a Python object
        data = json.loads(serialized_data)
        
        return JsonResponse({'data':chat}) 
    else :
        pass

def task_chat_refresh(request):
    task_id = request.POST.get('task_id')
    flag=request.POST.get('flag')
    request.session['flag']=flag

    # flag=int(flag)
    last_id = request.session.get('last_id', 0)

    tasks_chats = TasksChats.objects.filter(task_id=task_id, id__gt=last_id).exclude(user_id=request.session['id']).order_by('id')
    
    if tasks_chats != None and len(tasks_chats)>0:
        tasks_chat=[x.description for x in tasks_chats]
        name=[x.user_name for x in tasks_chats]
        last_id=[x.id for x in tasks_chats]
        # serialized_data = serialize('json', tasks_chat)
        # data = json.loads(serialized_data)
        

        request.session['last_id'] = last_id[-1]
        
        return JsonResponse({'data': tasks_chat,'name':name,'flag':flag})
    else:
        # time.sleep(4)
        # return task_chat_refresh(request)
        tasks_chat=[]
        name=[]
        
        return JsonResponse({'data': tasks_chat,'name':name,'flag':flag})

def status_change(request):
    print('helllass')
    task_id=request.POST.get('task_id')
    print(task_id)
    Fromvalues=request.POST.get('Fromvalues')
    Tovalues=request.POST.get('Tovalues')
    print(Fromvalues ,Tovalues)
    tasks=Tasks.objects.filter(id=task_id).first()
    if Tovalues=='right1':
        Tovalues='Development'
    elif Tovalues=='left1':
        Tovalues='Task List'
    elif Tovalues=='last1':
        Tovalues='Completed'
    if Fromvalues=='right1':
        Fromvalues='Development'
    elif Fromvalues=='left1':
        Fromvalues='Task List'
    elif Fromvalues=='last1':
        Fromvalues='Completed'
    if Tovalues=='Completed':
        TaskCrew.objects.filter(task_id=task_id,employee_name__contains=request.session['name']).update(status=Tovalues,)
    else:
        TaskCrew.objects.filter(task_id=task_id,employee_name__contains=request.session['name']).update(status=Tovalues)
    
    urlName =request.POST.get('urlName')
    print(urlName,)
    try:
        urlName =request.POST.get('urlName')
        if 'clientmanager'  in urlName or  'admin'  in urlName:
            print('inner----------------------')
            Tasks.objects.filter(id=task_id).update(status=Tovalues,complete_date=date.today())
    except:
        pass
        
    
    status_for_all = TaskCrew.objects.filter(task_id=task_id).values_list('status')
    status_for_all = list(status_for_all)
    status_list = [status[0] for status in status_for_all]
    
    print(status_list)
  
    if all(status == 'Completed' for status in status_list):
    # All values are 'completed'
        Tasks.objects.filter(id=task_id).update(status=Tovalues,crt_date=date.today())
        check=Tasks.objects.filter(id=task_id).first()
        print(f'--{check.ui}---{check.database}----{check.backend}--')
        if check.ui == 'None' or check.ui == None or  check.ui == ' ' or  check.ui == '':
            Tasks.objects.filter(id=task_id).update(ui=date.today())
        if check.ui == 'None' or check.database == None or check.database == ' ' or  check.database == '':
            Tasks.objects.filter(id=task_id).update(database=date.today())
        if check.ui == 'None' or check.backend == None or check.backend == ' ' or  check.backend == '':
            Tasks.objects.filter(id=task_id).update(backend=date.today())
        print("All values are 'completed'")
        
        
    # # print(status_for_all,'dfhs') 
    tasks=Tasks.objects.filter(id=task_id).first()
    # if Tovalues=='right1':
    project_id=tasks.project_id  
    task_id=task_id
    from_status=Fromvalues
    to_status=Tovalues   
    assigning_date=tasks.assigning_date
    target_date=tasks.target_date
    complte_date=tasks.complete_date
    manager_id=''
    user_id=request.session['id']
    crt_date=datetime.now()

   
    TasksLogs.objects.create( project_id=project_id, task_id=task_id, from_status=from_status, to_status=to_status, assigning_date=assigning_date, target_date=target_date, complte_date=complte_date, manager_id=manager_id, user_id=user_id, crt_date=crt_date,)
  
    tasks_chat=[]
    name=[]
    # print('status changed',task_id,status)
    return JsonResponse({'success': 'success'})

def task_work(request):
    return JsonResponse()  

def task_status_mark(request):
    print('hii')
    task_id=request.POST.get('task_id')
    work=request.POST.get('chat')
    if work == 'ui':
        Tasks.objects.filter(id=task_id).update(ui=date.today())
    elif work == 'bc':
        Tasks.objects.filter(id=task_id).update( backend=date.today())
    elif work == 'db':
        Tasks.objects.filter(id=task_id).update( database=date.today())
    
    return JsonResponse({'data': 'success'})  

def Admin_Employee_Details(request):
    try:
        if request.session['user']=="5":
            pass
        else:
            response=HttpResponseRedirect('../../')
            return response
    except:
        s='enter credentials for  login '
        response=HttpResponseRedirect('../../')
        return response
    if request.method=='GET':
        current_date=datetime.now().date()
        month=current_date.month
        year=current_date.year
        day=current_date.day
        print(current_date,year)
        request.session['emp_detail_date']=str(current_date)
    empdetails=EmpDesk.objects.filter(login_id=request.session['emp_details']).first
    if 'prev' in request.POST:
        current_date=request.session['emp_detail_date']
        print(current_date)
        current_date=datetime.strptime(current_date, '%Y-%m-%d')
        year = current_date.year - (current_date.month == 1)
        month = current_date.month - 1 if current_date.month > 1 else 12
        day = current_date.day

        # Adjust for months with fewer days
        while True:
            try:
                current_date = datetime(year, month, day)
                break
            except ValueError:
                day -= 1
        print(year,month,current_date)
        current_date=current_date.strftime('%Y-%m-%d')
        request.session['emp_detail_date']=str(current_date)
    elif 'next' in request.POST:
        current_date=request.session['emp_detail_date']
        print(current_date)
        current_date=datetime.strptime(current_date, '%Y-%m-%d')
        year = current_date.year + (current_date.month == 12)
        month = current_date.month + 1 if current_date.month < 12 else 1
        day = current_date.day
        while True:
            print(year, month, day)
            try:
                current_date = datetime(year, month, day)
                break
            except ValueError:
                day -= 1
        print(year,month,current_date)
        current_date=current_date.strftime('%Y-%m-%d')
        request.session['emp_detail_date']=str(current_date)
    print(request.session['emp_details'],'---------------------')
    report_data=Empdata.objects.annotate(start_datetime=Cast('start', DateField()),end_datetime=Cast('end', DateField())).filter(Q(emp_id=request.session['emp_details'],start_datetime__month=month,start_datetime__year=year,statushr='1')|Q(emp_id=request.session['emp_details'],end_datetime__month=month,end_datetime__year=year,statushr='1'))
    week1=[]
    week2=[]
    week3=[]
    week4=[]
    week5=[]
    week6=[]
    for i in report_data:
        first_day_of_month = (i.start_datetime).replace(day=1)
        week_number_of_first_day = first_day_of_month.isocalendar()[1]
        current_week_within_month = i.start_datetime.isocalendar()[1] - week_number_of_first_day +1
        if current_week_within_month==1:
            week1.append(i)
            week1_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==2:
            week2.append(i)
            week2_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==3:
            week3.append(i)
            week3_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==4:
            week4.append(i)
            week4_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==5:
            week5.append(i)
            week5_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
        elif current_week_within_month==6:
            week6.append(i)
            week6_comment_performance=Ratings.objects.filter(emp_id=i.emp_id,startdate=i.start).first
    weekly_data=[]
    weekly_performance=[]
    weekly_tasks=[]
    if len(week1)>0:
        start=week1[0].start
        end=week1[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week1)
        weekly_performance.append(week1_comment_performance)
    if len(week2)>0:
        start=week2[0].start
        end=week2[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week2)
        weekly_performance.append(week2_comment_performance)
    if len(week3)>0:
        start=week3[0].start
        end=week3[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week3)
        weekly_performance.append(week3_comment_performance)
    if len(week4)>0:
        start=week4[0].start
        end=week4[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week4)
        weekly_performance.append(week4_comment_performance)
    if len(week5)>0:
        start=week5[0].start
        end=week5[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week5)
        weekly_performance.append(week5_comment_performance)
    if len(week6)>0:
        start=week6[0].start
        end=week6[0].end
        end= datetime.strptime(end, "%Y-%m-%d")
        start= datetime.strptime(start, "%Y-%m-%d")
        projects=Project_team.objects.filter(employee_id=request.session['emp_details'])
        projects=[x.project for x in projects]
        task=Tasks.objects.annotate(complete_dates=Cast('complete_date', DateField())).filter(project_id__in=projects,complete_dates__gte=start,complete_dates__lte=end)
        

        weekly_tasks.append(task)
        weekly_data.append(week6)
        weekly_performance.append(week6_comment_performance)    
   
    print(len(weekly_data),'weekly_data')
    weekly_data=zip(weekly_data,weekly_performance,weekly_tasks)
    return render(request, 'OM_EmpDetails.html',{'month':month,'year':year,'empdetails':empdetails,'weekly_data':weekly_data})

def OM_phase(request):
    message=''
    project=request.session['project_name']
    projectdetails=ProjectDetails.objects.filter(project_name=project)
    phaseversion=PhaseVersion.objects.filter(project=project)
    if len(phaseversion)==0:
        pass
        # PhaseVersion.objects.create(project=project, phase='1', version='1.0', start_date=datetime.now(), create_date=datetime.now(),time_period='2')
        # Versions.objects.create(project=project,version='1.0',create_date=datetime.now()) 
    version=Versions.objects.filter(project=project)
    if len(version)==0:
        Versions.objects.create(project=project,version='1.0',create_date=datetime.now()) 
    if request.method=='POST':
        if 'phase' in request.POST:
            time_period=request.POST.get('time_period')
            start_period=datetime.now()
            end_period=(start_period+timedelta(days=int(time_period)*7)).date()
            
            try:
                phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project)
                phase=[x.phase_float for x in phase_value]
                phase=max(phase)
                version_value=Versions.objects.annotate(version_float=Cast('version', output_field=FloatField())).filter(project=project)
                version=[x.version_float for x in version_value]
                version=max(version)
            except:
                phase=0
                version=1.0

            
            try:
                phase_data=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project,version_float=version,phase_float=phase).order_by('-phase_float').first()
                end_date=phase_data.start_date
                end_date=datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S.%f')
                end_date=(end_date+timedelta(days=int(phase_data.time_period)*7)).date()
                
                end_date=(end_date-datetime.now().date()).days
                
            except:
                end_date=0
            
            # phase=[x.phase_float for x in phase_value]
            # phase=max(phase)
            new_phase=phase+1
            new_phase=int(new_phase)




            if end_date<3:
                message=''
                PhaseVersion.objects.create(project=project,version=version,phase=new_phase,start_date=datetime.now()  ,create_date=datetime.now(),time_period=time_period,end_date=end_period)  
            else:
                message='You can not create a new phase until two days before the end date of the current phase.'

        elif 'add_Task' in request.POST:

            project_name=request.session['project_name']
            project_id=project_name
            print(project_name)
            try:
                team_id=Project_team.objects.filter(project=project_name).first().team
            except:
                team_id=''
            task_heading=request.POST.get('task_heading')
            description=request.POST.get('task')
            description = description.split('\n')

            description = [line + '<br>' for line in description]

            description = ''.join(description)
            assigning_date=date.today()
            target_date=request.POST.get('date')
            task_crew=request.POST.getlist('task_crew')
            task_type=request.POST.get('type')
            priority=request.POST.get('priority')
            print(task_type,task_crew)
            complete_date=''
            manager_id=request.session['id']
            assignee=str(Login.objects.get(id=request.session['id']).f_name)+str(Login.objects.get(id=request.session['id']).l_name)
            hr_id=Manager.objects.get(emp_id=request.session['id']).hr_id
            status='Task List'
            crt_date=datetime.now()
            projec_task_id=Tasks.objects.filter(project_id=project_id)
            projec_task_id=len(projec_task_id)
            projec_task_id=projec_task_id+1

            try:
                phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project_name)
                phase=[x.phase_float for x in phase_value]
                phase=max(phase)
                phase=int(phase)
                version=[x.version_float for x in phase_value]
                version=max(version)
            except:
                phase=1
                version=1.0
        
            Tasks.objects.create(project_id=project_id,team_id=team_id,description=description,assigning_date=assigning_date,
                target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date,
                ui=' '  ,database=' ' ,backend=' ',projec_task_id=projec_task_id,phase=phase,project_version=version,task_heading=task_heading,
                task_type=task_type, priority=priority,assignee=assignee)

            task_id=Tasks.objects.filter(project_id=project_id,description=description,assigning_date=assigning_date,
                target_date=target_date,complete_date=complete_date,manager_id=manager_id,hr_id=hr_id,status=status,crt_date=crt_date).first()
            task_id=task_id.id
            
            for employee in task_crew:
                obj=TaskCrew.objects.filter(task_id=task_id,employee_name=employee)
                if len(obj)>0:
                    pass
                else:
                    TaskCrew.objects.create(task_id=task_id,employee_name=employee,create_date=datetime.now(),status='Task List')
            if True:
                print(request.FILES)
                uploaded_files = request.FILES.getlist('attachments')
                image_name=[]
                print(uploaded_files)
                for uploaded_file in uploaded_files:
                    if uploaded_file is not None:
                        id_gen=str(task_id)
                        image=id_gen+uploaded_file.name
                        image=image.replace(' ','')
                        file_path = fr'static/uploads/task_files/{image}'
                        with open(file_path, 'wb') as file:
                            for chunk in uploaded_file.chunks():
                                file.write(chunk)
                        TaskFiles.objects.create(task_id=task_id,file_name=image,create_date=datetime.now())
            else:
                pass
            
            TasksLogs.objects.create(project_id=project_id, task_id=task_id, from_status='Task List', to_status='Task List', 
                assigning_date=assigning_date, target_date=target_date, complte_date=complete_date, manager_id=manager_id, user_id=request.session['id'], crt_date=crt_date,)
            

        elif 'version' in request.POST:
            try:
                phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project)
                phase=[x.phase_float for x in phase_value]
                phase=max(phase)
                version=[x.version_float for x in phase_value]
                version=max(version)
                version=version+0.1
                version = round(version, 1)
                # phase=1.0
                Versions.objects.create(project=project,version=version,create_date=datetime.now())
            except:
                pass  



            # phaseversion=PhaseVersion.objects.filter(project=project)
    phases=[]
    tasks=[]
    team=[]
    versions  = PhaseVersion.objects.filter(project=project)
    versions=[x.version for x in versions]
    versions = [float(version) for version in versions]
    versions = sorted(set(versions))
    # print(versions,'-----------------')
    versions = [str(version) for version in versions]
    versions.reverse()
    version=[]
    crews=[]
    employees=EmpDesk.objects.filter(manager_id=request.session['id'],activation='Active')

    for h in versions:

        phase= PhaseVersion.objects.filter(project=project,version=h).order_by('-id')
        phases=[]
        for i in  phase:
            start_period=str(i.start_date)
            print(start_period)
            try:
                start_period=datetime.strptime(start_period,'%Y-%m-%d')
            except:
                start_period=datetime.strptime(start_period,'%Y-%m-%d %H:%M:%S.%f')

            end_period=(start_period+timedelta(days=int(i.time_period)*7)).date()
            start_period=start_period.date()

            print(end_period,'-------------------------------------')

            task=Tasks.objects.filter(project_id=project,phase=i.phase,project_version=h).order_by('-id')
            tasks=[]
            for j in task:
                crews=[]
                crew=TaskCrew.objects.filter(task_id=j.id)

                if len(crew)==0:
                    crew=Project_team.objects.filter(project=project)
                task_chat=TasksChats.objects.filter(task_id=j.id)
                task_logs=TasksLogs.objects.annotate(dates=Cast('crt_date', output_field=DateField())).annotate(name=Subquery(EmpDesk.objects.filter(login_id=OuterRef('user_id')).values('f_name')[:1])).filter(task_id=j.id)
                attachments=TaskFiles.objects.filter(task_id=j.id)
                for cr in crew:
                    if EmpDesk.objects.get(email=cr.employee_name ).activation=='Active':
                        crews.append(cr.employee_name)
                for em in employees:
                    if em.email in crews:
                        pass
                    else:
                        crews.append(em.email)

                l=[j,crew,task_chat,task_logs,attachments,crews]
                tasks.append(l)
                l=team
            phases.append([i,tasks,str(end_period),str(start_period)])
        version.append(phases)
    
    project_team=Project_team.objects.filter(project=request.session['project_name']) 
    project_team_task=[x.employee_name for x in project_team]
    current_version_value=Versions.objects.annotate(version_float=Cast('version', output_field=FloatField())).filter(project=project)
    current_version=[x.version_float for x in current_version_value]
    current_version=max(current_version)
    current_phase_value=PhaseVersion.objects.annotate(phase_float=Cast('phase', output_field=FloatField()),version_float=Cast('version', output_field=FloatField())).filter(project=project)
    current_phase=[x.phase_float for x in current_phase_value]
    current_phase=int(max(current_phase)+1)
    
    return render(request,"OM_phase.html",{'current_phase':current_phase,'message':message,'version':version,'employees':employees,'project_team_task':project_team_task,'current_version':current_version})

def change_task_status(request):
    status=request.POST.get('task')
    urlName=request.POST.get('urlName')
    status=status.split('/')
    task_id=status[0]
    status=status[1]
    if 'employee' in urlName:
        TaskCrew.objects.filter(task_id=task_id).update(status=status)
    else:
        Tasks.objects.filter(id=task_id).update(status=status)
    return JsonResponse({'data': 'success'})

def change_task_crew(request):
    crew=request.POST.getlist('selectedNames[]')
    task_id=request.POST.get('task_id')
    task_crew=TaskCrew.objects.filter(task_id=task_id).exclude(employee_name__in=crew)
    task_crew.delete()
    for i in crew:
        task_data=TaskCrew.objects.filter(task_id=task_id,employee_name=i)
        if len(task_data)>0:
            pass
        else:
            TaskCrew.objects.create(task_id=task_id,employee_name=i,create_date=datetime.now(),status='Development')



    print(task_crew,'--task_crew-task_crew-task_crew-task_crew')

    
    print(crew,task_id)
    return JsonResponse({'data': 'success'})






















