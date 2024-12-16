def Emp_tracker(request):
    if request.session['user']=="3":
        global start_dates
        global end_dates
        sun,tue,mond,wed,thu,fri,sat=0,0,0,0,0,0,0
        weektotal=0
        projectname,days=[],[]
        print("!!!!!!!!!!")
        employee_data=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates)
        
        
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
        lists=[]
        i=0
        rows=0
        count=0
        total=0
        start=0
        end_dt=0
        day01,day2,day3,day4,day5,day6,day7,day8,day9,day10,day11,day12,day13,day14,day15,day16,day17,day18,day19,day20=0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
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
        if request.method=="POST" and ('prev' in request.POST or 'next' in request.POST):
            
            if 'prev' in request.POST:
                start_dates=start_dates- timedelta(days=7, hours=0)
                end_dates=end_dates- timedelta(days=7, hours=0)
        # do subscribe
            elif 'next' in request.POST:
                start_dates=start_dates+ timedelta(days=7, hours=0)
                end_dates=end_dates+ timedelta(days=7, hours=0)
            sun,tue,mond,wed,thu,fri,sat=0,0,0,0,0,0,0
            projectname,days=[],[]
            
            weektotal=0
            employee_data=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates)
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
            dats={}
            for pro in projectname:
                for i in range(0,len(days)):
                    
                    dats[f"{pro}"]=pro
                    day='day'+str(i)
                    dats[f"{day}"]=days[i]
            datas={"list": lists,'total':total,'rows':rows,'name':name,'start_date':start_dates,'end_date':end_dates,'totals':total_hour,'gtotal':weektotal,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun}
            for keys,values in dats.items():
                datas[f"{keys}"]=values  
            name=request.session['name']  
            return render(request,'Emp_tracker.html',datas)
        
        
        elif request.method=="POST":
            
            totala,totalb,totalc,totals,i,dt=0,0,0,0,0,1
            rows=int(request.POST.get('rows'))
            try:
                a1=request.POST.get('a1')
                a2=request.POST.get('a2')
                a3=request.POST.get('a3')
                a4=request.POST.get('a4')
                a5=request.POST.get('a5')
                a6=request.POST.get('a6')
                a7=request.POST.get('a7')
                a0=request.POST.get('a0')
                print('this is passed the condition where data is collected for ist row')
            except:
                pass
            try:
                b1=request.POST.get('b1')
                b2=request.POST.get('b2')
                b3=request.POST.get('b3')
                b4=request.POST.get('b4')
                b5=request.POST.get('b5')
                b6=request.POST.get('b6')
                b7=request.POST.get('b7')
                b0=request.POST.get('b0')
                print('thi is passed the condition 2nd row')
            except:
                pass
            try:
                c1=request.POST.get('c1')
                c2=request.POST.get('c2')
                c3=request.POST.get('c3')
                c4=request.POST.get('c4')
                c5=request.POST.get('c5')
                c6=request.POST.get('c6')
                c7=request.POST.get('c7')
                c0=request.POST.get('c0')
                print('thi is passed the condition 3rd row')
            except:
                pass
            try:
                if a0!='0' and a0!='--Select--' :
                    totala=int(a1)+int(a2)+int(a3)+int(a4)+int(a5)+int(a6)+int(a7)
                    totals=totals+totala
                    a={"b0":a0,"b1":a1,"b2":a2,"b3":a3,"b4":a4,"b5":a5,"b6":a6,"b7":a7,"total":totala,'totals':totals}
                    lists.append(a)
                    print('thi is passed the condition first entry')
            except:
                pass
            try:
                if b0 !='0' and b0!='--Select--' :
                    totalb=int(b1)+int(b2)+int(b3)+int(b4)+int(b5)+int(b6)+int(b7)
                    totals=totals+totalb
                    b={"b"+str(i):b0,"b"+str(i+1):b1,"b"+str(i+2):b2,"b"+str(i+3):b3,"b"+str(i+4):b4,"b"+str(i+5):b5,"b"+str(i+6):b6,"b"+str(i+7):b7,"total":totalb,'totals':totals}
                    lists.append(b)
                else:
                    print('thi is passed the conditionsecond enterty')
            except:
                pass
            try:
                if (c0 !='0'  and c0!='--Select--'):
                    totalc=int(c1)+int(c2)+int(c3)+int(c4)+int(c5)+int(c6)+int(c7)
                    totals=totals+totalc
                    c={"b"+str(i):c0,"b"+str(i+1):c1,"b"+str(i+2):c2,"b"+str(i+3):c3,"b"+str(i+4):c4,"b"+str(i+5):c5,"b"+str(i+6):c6,"b"+str(i+7):c7,"total":totalc,'totals':totals}
                    lists.append(c)
            except:
                pass
            if rows >0:
                for i in range(0,rows*8,8):
                    b0=request.POST.get("Name"+str(i))
                    b1=request.POST.get("Name"+str(i+1))
                    b2=request.POST.get("Name"+str(i+2))
                    b3=request.POST.get("Name"+str(i+3))
                    b4=request.POST.get("Name"+str(i+4))
                    b5=request.POST.get("Name"+str(i+5))
                    b6=request.POST.get("Name"+str(i+6))
                    b7=request.POST.get("Name"+str(i+7))
                    try:
                        total=int(b1)+int(b2)+int(b3)+int(b4)+int(b5)+int(b6)+int(b7)
                        totals=totals+int(b1)+int(b2)+int(b3)+int(b4)+int(b5)+int(b6)+int(b7)
                    except:
                        pass
                    i=0
                    b={"b"+str(i):b0,"b"+str(i+1):b1,"b"+str(i+2):b2,"b"+str(i+3):b3,"b"+str(i+4):b4,"b"+str(i+5):b5,"b"+str(i+6):b6,"b"+str(i+7):b7,"total":total,'totals':totals}
                    lists.append(b)

            # For saving in database 
            print(lists)   
            for i in lists:
                try:
                    obj=Empdata.objects.filter(emp_id=request.session['id'],start=start_dates,project_name=i['b0'])
                    obj.delete()
                except:
                    pass
                a = Empdata(emp_id=str(id),mon=str(i['b1']) ,tue=str(i['b2']) ,wed=str(i['b3']) ,thu=str(i['b4']) ,fri=str(i['b5']) ,sat=str(i['b6']) ,sun=str(i['b7']),project_name=str(i['b0']),start=str(start_dates),end=str(end_dates),name=name, status=0,total=i['total'],totals=i['totals'],statushr=0,date_created=datetime.now().date())
                a.save()
            
            
            data={"list": lists,'total':total,'rows':rows,'name':name,'start_date':start_dates,'end_date':end_dates,'totals':total_hour,'gtotal':weektotal,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun}
            for keys,values in dats.items():
                data[f"{keys}"]=values
            name=request.session['name']
            #return render(request,'Emp_tracker.html',data)
        
        sun,tue,mond,wed,thu,fri,sat=0,0,0,0,0,0,0

        projectname,days=[],[]
        start_dts=start_dates.strftime("%Y-%m-%d ")
        print(start_dts)
        weektotal=0
        employee_data=Empdata.objects.filter(emp_id=request.session['id'],start=start_dts)
        for data in employee_data:
            print(data.start)
                
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
            
        pp=0
            
        dats={'day0':0,'day1':0,'day2':0,'day3':0,'day4':0,'day5':0,'day6':0,'day7':0,'day8':0,'day9':0,'day10':0,'day11':0,'day12':0,'day13':0,'day14':0,'day15':0,'day16':0,'day17':0,'day18':0,'day19':0,'day20':0,"project1":"--Select--","project2":"--Select--","project3":"--Select--"}
            
        for pro in projectname:
            pp+=1
            p='project'+str(pp)
            for i in range(0,len(days)):
                    
                dats[f"{p}"]="--"+pro+"--"
                day='day'+str(i)
                dats[f"{day}"]=days[i]
        name=request.session['name'] 
        projects=Project_team.objects.filter(employee_name=name)
        datas={"list": lists,'total':total,'rows':rows,'name':name,'projects':projects,'start_date':start_dates,'end_date':end_dates,'totals':total_hour,'gtotal':weektotal,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun,"project1":"--Select--","project2":"--Select--","project3":"--Select--"}
        for keys,values in dats.items():
            datas[f"{keys}"]=values  
        name=request.session['name'] 

            
        #data={'name':name,'start_date':start_dates,'end_date':end_dates,'totals':tt,'mond':mond,'tue':tue,'wed':wed,'thu':thu,'fri':fri,'sat':sat,'sun':sun,'gtotal':weektotal,'project1':'--Select--','project2':'--Select--','project3':'--Select--'}
        
            
        return render(request,'Emp_tracker.html',datas)
        #return render(request,'Emp_tracker.html',data)
    else:
        response=HttpResponseRedirect('../../')
        return response
