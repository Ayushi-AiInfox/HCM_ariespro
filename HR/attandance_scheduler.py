import pyodbc
from datetime import date
sql_conn = pyodbc.connect('DRIVER={SQL server}; SERVER=apdevsys; DATABASE=global_work_force; UID=atsutilityariespro; PWD=ut!l!ty@t$@2019;') 
cursor=sql_conn.cursor()
today= date.today()
day=today.day
month=today.month
year=today.year
querry=f'''   update attendance  set day{day}='P' 
          from attendance  a       
          join login l on l.USER_NAME=a.[USER]  
          where month = {month}
          and year = {year} 
          and day{day} is NULL
          and l.activation = 'Active'
            '''

print(querry)
# cursor.execute(querry)
# cursor.commit()

cursor.close()
sql_conn.close()
x='success'
print(x)