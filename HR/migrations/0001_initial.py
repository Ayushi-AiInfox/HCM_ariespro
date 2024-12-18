# Generated by Django 5.1.3 on 2024-11-30 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="HrDesk",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "emp_name",
                    models.CharField(
                        blank=True, db_column="EMP_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "project",
                    models.CharField(
                        blank=True, db_column="PROJECT", max_length=50, null=True
                    ),
                ),
                (
                    "description_field",
                    models.CharField(
                        blank=True, db_column="DESCRIPTION_", max_length=50, null=True
                    ),
                ),
                (
                    "date_field",
                    models.DateField(blank=True, db_column="DATE_", null=True),
                ),
                (
                    "total_hours",
                    models.CharField(
                        blank=True, db_column="TOTAL_HOURS", max_length=50, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True, db_column="STATUS", max_length=50, null=True
                    ),
                ),
            ],
            options={
                "db_table": "HR_DESK",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Attendance",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.CharField(
                        blank=True, db_column="USER", max_length=50, null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, db_column="NAME", max_length=50, null=True
                    ),
                ),
                (
                    "month",
                    models.CharField(
                        blank=True, db_column="MONTH", max_length=50, null=True
                    ),
                ),
                (
                    "year",
                    models.CharField(
                        blank=True, db_column="YEAR", max_length=50, null=True
                    ),
                ),
                (
                    "day1",
                    models.CharField(
                        blank=True, db_column="DAY1", max_length=50, null=True
                    ),
                ),
                (
                    "day2",
                    models.CharField(
                        blank=True, db_column="DAY2", max_length=50, null=True
                    ),
                ),
                (
                    "day3",
                    models.CharField(
                        blank=True, db_column="DAY3", max_length=50, null=True
                    ),
                ),
                (
                    "day4",
                    models.CharField(
                        blank=True, db_column="DAY4", max_length=50, null=True
                    ),
                ),
                (
                    "day5",
                    models.CharField(
                        blank=True, db_column="DAY5", max_length=50, null=True
                    ),
                ),
                (
                    "day6",
                    models.CharField(
                        blank=True, db_column="DAY6", max_length=50, null=True
                    ),
                ),
                (
                    "day7",
                    models.CharField(
                        blank=True, db_column="DAY7", max_length=50, null=True
                    ),
                ),
                (
                    "day8",
                    models.CharField(
                        blank=True, db_column="DAY8", max_length=50, null=True
                    ),
                ),
                (
                    "day9",
                    models.CharField(
                        blank=True, db_column="DAY9", max_length=50, null=True
                    ),
                ),
                (
                    "day10",
                    models.CharField(
                        blank=True, db_column="DAY10", max_length=50, null=True
                    ),
                ),
                (
                    "day11",
                    models.CharField(
                        blank=True, db_column="DAY11", max_length=50, null=True
                    ),
                ),
                (
                    "day12",
                    models.CharField(
                        blank=True, db_column="DAY12", max_length=50, null=True
                    ),
                ),
                (
                    "day13",
                    models.CharField(
                        blank=True, db_column="DAY13", max_length=50, null=True
                    ),
                ),
                (
                    "day14",
                    models.CharField(
                        blank=True, db_column="DAY14", max_length=50, null=True
                    ),
                ),
                (
                    "day15",
                    models.CharField(
                        blank=True, db_column="DAY15", max_length=50, null=True
                    ),
                ),
                (
                    "day16",
                    models.CharField(
                        blank=True, db_column="DAY16", max_length=50, null=True
                    ),
                ),
                (
                    "day17",
                    models.CharField(
                        blank=True, db_column="DAY17", max_length=50, null=True
                    ),
                ),
                (
                    "day18",
                    models.CharField(
                        blank=True, db_column="DAY18", max_length=50, null=True
                    ),
                ),
                (
                    "day19",
                    models.CharField(
                        blank=True, db_column="DAY19", max_length=50, null=True
                    ),
                ),
                (
                    "day20",
                    models.CharField(
                        blank=True, db_column="DAY20", max_length=50, null=True
                    ),
                ),
                (
                    "day21",
                    models.CharField(
                        blank=True, db_column="DAY21", max_length=50, null=True
                    ),
                ),
                (
                    "day22",
                    models.CharField(
                        blank=True, db_column="DAY22", max_length=50, null=True
                    ),
                ),
                (
                    "day23",
                    models.CharField(
                        blank=True, db_column="DAY23", max_length=50, null=True
                    ),
                ),
                (
                    "day24",
                    models.CharField(
                        blank=True, db_column="DAY24", max_length=50, null=True
                    ),
                ),
                (
                    "day25",
                    models.CharField(
                        blank=True, db_column="DAY25", max_length=50, null=True
                    ),
                ),
                (
                    "day26",
                    models.CharField(
                        blank=True, db_column="DAY26", max_length=50, null=True
                    ),
                ),
                (
                    "day27",
                    models.CharField(
                        blank=True, db_column="DAY27", max_length=50, null=True
                    ),
                ),
                (
                    "day28",
                    models.CharField(
                        blank=True, db_column="DAY28", max_length=50, null=True
                    ),
                ),
                (
                    "day29",
                    models.CharField(
                        blank=True, db_column="DAY29", max_length=50, null=True
                    ),
                ),
                (
                    "day30",
                    models.CharField(
                        blank=True, db_column="DAY30", max_length=50, null=True
                    ),
                ),
                (
                    "day31",
                    models.CharField(
                        blank=True, db_column="DAY31", max_length=50, null=True
                    ),
                ),
                (
                    "hr_id",
                    models.CharField(
                        blank=True, db_column="hr_id", max_length=50, null=True
                    ),
                ),
            ],
            options={
                "db_table": "attendance",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="DesignationMaster",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "designation",
                    models.CharField(
                        blank=True, db_column="DESIGNATION", max_length=150, null=True
                    ),
                ),
            ],
            options={
                "db_table": "DESIGNATION_MASTER",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="EmpDesk",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "login_id",
                    models.IntegerField(blank=True, db_column="LOGIN_ID", null=True),
                ),
                (
                    "f_name",
                    models.CharField(
                        blank=True, db_column="F_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "l_name",
                    models.CharField(
                        blank=True, db_column="L_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "emp_type",
                    models.CharField(
                        blank=True, db_column="EMP_TYPE", max_length=50, null=True
                    ),
                ),
                (
                    "designation",
                    models.CharField(
                        blank=True, db_column="DESIGNATION", max_length=50, null=True
                    ),
                ),
                (
                    "manager_id",
                    models.CharField(
                        blank=True, db_column="MANAGER_ID", max_length=50, null=True
                    ),
                ),
                (
                    "hr_id",
                    models.CharField(
                        blank=True, db_column="HR_ID", max_length=50, null=True
                    ),
                ),
                (
                    "employment",
                    models.CharField(
                        blank=True, db_column="EMPLOYMENT", max_length=50, null=True
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True, db_column="GENDER", max_length=50, null=True
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        blank=True, db_column="EMAIL", max_length=50, null=True
                    ),
                ),
                ("doj", models.DateField(blank=True, db_column="DOJ", null=True)),
                ("dob", models.DateField(blank=True, db_column="DOB", null=True)),
                (
                    "mobile",
                    models.CharField(
                        blank=True, db_column="MOBILE", max_length=50, null=True
                    ),
                ),
                (
                    "mobile_alt",
                    models.CharField(
                        blank=True, db_column="MOBILE_ALT", max_length=50, null=True
                    ),
                ),
                (
                    "address",
                    models.CharField(
                        blank=True, db_column="ADDRESS", max_length=50, null=True
                    ),
                ),
                (
                    "salary",
                    models.CharField(
                        blank=True, db_column="SALARY", max_length=50, null=True
                    ),
                ),
                (
                    "bank_name",
                    models.CharField(
                        blank=True, db_column="BANK_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "account_number",
                    models.CharField(
                        blank=True, db_column="ACCOUNT_NUMBER", max_length=50, null=True
                    ),
                ),
                (
                    "ifsc",
                    models.CharField(
                        blank=True, db_column="IFSC", max_length=50, null=True
                    ),
                ),
                (
                    "branch",
                    models.CharField(
                        blank=True, db_column="BRANCH", max_length=50, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True, db_column="STATUS", max_length=50, null=True
                    ),
                ),
                (
                    "crt_date",
                    models.CharField(
                        blank=True, db_column="CRT_DATE", max_length=50, null=True
                    ),
                ),
                (
                    "current_project",
                    models.CharField(
                        blank=True,
                        db_column="CURRENT_PROJECT",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "team_name",
                    models.CharField(
                        blank=True, db_column="TEAM_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "leave_taken",
                    models.CharField(
                        blank=True, db_column="LEAVE_TAKEN", max_length=50, null=True
                    ),
                ),
                (
                    "leave_remaining",
                    models.CharField(
                        blank=True,
                        db_column="LEAVE_REMAINING",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "designations",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("managers", models.CharField(blank=True, max_length=50, null=True)),
                ("activation", models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                "db_table": "EMP_DESK",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="hrteam",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "emp_id",
                    models.CharField(
                        blank=True, db_column="emp_id", max_length=150, null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, db_column="name", max_length=150, null=True
                    ),
                ),
                (
                    "project",
                    models.CharField(
                        blank=True, db_column="project", max_length=150, null=True
                    ),
                ),
                (
                    "user_typ",
                    models.CharField(
                        blank=True, db_column="user_type", max_length=150, null=True
                    ),
                ),
                (
                    "team",
                    models.CharField(
                        blank=True, db_column="team", max_length=150, null=True
                    ),
                ),
                (
                    "manager",
                    models.CharField(
                        blank=True, db_column="manager", max_length=150, null=True
                    ),
                ),
            ],
            options={
                "db_table": "hrteam",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="LeaveDetails",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "emp_id",
                    models.CharField(
                        blank=True, db_column="EMP_ID", max_length=150, null=True
                    ),
                ),
                (
                    "remaining",
                    models.CharField(
                        blank=True, db_column="REMAINING", max_length=150, null=True
                    ),
                ),
                (
                    "taken",
                    models.CharField(
                        blank=True, db_column="TAKEN", max_length=150, null=True
                    ),
                ),
                (
                    "note",
                    models.CharField(
                        blank=True, db_column="note", max_length=250, null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, db_column="NAME", max_length=150, null=True
                    ),
                ),
                (
                    "sick_day",
                    models.CharField(
                        blank=True, db_column="SICK_DAY", max_length=150, null=True
                    ),
                ),
                (
                    "work_from_home",
                    models.CharField(
                        blank=True,
                        db_column="WORK_FROM_HOME",
                        max_length=150,
                        null=True,
                    ),
                ),
                (
                    "days_allowed",
                    models.CharField(
                        blank=True, db_column="DAYS_ALLOWED", max_length=150, null=True
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        blank=True, db_column="User_Type", max_length=150, null=True
                    ),
                ),
                (
                    "reset_date",
                    models.CharField(
                        blank=True, db_column="reset_date", max_length=150, null=True
                    ),
                ),
                (
                    "hr_id",
                    models.CharField(
                        blank=True, db_column="hr_id", max_length=150, null=True
                    ),
                ),
            ],
            options={
                "db_table": "LEAVE_DETAILS",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Manager",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "emp_id",
                    models.CharField(
                        blank=True, db_column="emp_id", max_length=150, null=True
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, db_column="NAME", max_length=150, null=True
                    ),
                ),
                (
                    "hr_id",
                    models.CharField(
                        blank=True, db_column="HR_ID", max_length=150, null=True
                    ),
                ),
                (
                    "client",
                    models.CharField(
                        blank=True, db_column="CLIENT", max_length=150, null=True
                    ),
                ),
                (
                    "office_manager",
                    models.CharField(
                        blank=True,
                        db_column="OFFICE_MANAGER",
                        max_length=150,
                        null=True,
                    ),
                ),
            ],
            options={
                "db_table": "MANAGERS",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Payroll",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "employee",
                    models.CharField(
                        blank=True, db_column="Employee", max_length=50, null=True
                    ),
                ),
                (
                    "salary_per_month",
                    models.CharField(
                        blank=True,
                        db_column="Salary_per_month",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "paid_sick_leave",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "paid_sick_leave_rs",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "paid_holiday",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "paid_holiday_rs",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "paid_vacation_day",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "paid_vacation_day_rs",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "unpaid_vacation",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "unpaid_vacation_rs",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "internet_charges_rs",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "salary_and_other_charges_rs",
                    models.CharField(
                        blank=True,
                        db_column="salary_and_other_harges_rs",
                        max_length=50,
                        null=True,
                    ),
                ),
                (
                    "paid_to_employee",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("user_name", models.CharField(blank=True, max_length=50, null=True)),
                ("month", models.CharField(blank=True, max_length=50, null=True)),
                ("year", models.CharField(blank=True, max_length=50, null=True)),
                ("paid", models.CharField(blank=True, max_length=50, null=True)),
                ("hr_id", models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                "db_table": "payroll",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Project_team",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "project",
                    models.CharField(
                        blank=True, db_column="project", max_length=150, null=True
                    ),
                ),
                (
                    "team",
                    models.CharField(
                        blank=True, db_column="team", max_length=150, null=True
                    ),
                ),
                (
                    "manager",
                    models.CharField(
                        blank=True, db_column="manager", max_length=150, null=True
                    ),
                ),
                (
                    "employee_name",
                    models.CharField(
                        blank=True, db_column="employee_name", max_length=250, null=True
                    ),
                ),
                (
                    "employee_id",
                    models.CharField(
                        blank=True, db_column="employee_id", max_length=150, null=True
                    ),
                ),
                (
                    "designation",
                    models.CharField(
                        blank=True, db_column="designation", max_length=150, null=True
                    ),
                ),
                (
                    "crt_date",
                    models.CharField(
                        blank=True, db_column="crt_date", max_length=150, null=True
                    ),
                ),
                (
                    "hr_id",
                    models.CharField(
                        blank=True, db_column="hr_id", max_length=150, null=True
                    ),
                ),
            ],
            options={
                "db_table": "project_team",
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="ProjectDetails",
            fields=[
                (
                    "id",
                    models.AutoField(db_column="ID", primary_key=True, serialize=False),
                ),
                (
                    "project_name",
                    models.CharField(
                        blank=True, db_column="PROJECT_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "client_name",
                    models.CharField(
                        blank=True, db_column="CLIENT_NAME", max_length=50, null=True
                    ),
                ),
                (
                    "manager_id",
                    models.IntegerField(blank=True, db_column="MANAGER_ID", null=True),
                ),
                (
                    "employee_id",
                    models.IntegerField(blank=True, db_column="EMPLOYEE_ID", null=True),
                ),
                (
                    "start_date",
                    models.DateField(blank=True, db_column="START_DATE", null=True),
                ),
                (
                    "end_date",
                    models.DateField(blank=True, db_column="END_DATE", null=True),
                ),
                (
                    "status",
                    models.CharField(
                        blank=True, db_column="STATUS", max_length=50, null=True
                    ),
                ),
                (
                    "crt_date",
                    models.DateTimeField(blank=True, db_column="CRT_DATE", null=True),
                ),
                (
                    "manager",
                    models.CharField(
                        blank=True, db_column="MANAGER", max_length=50, null=True
                    ),
                ),
                (
                    "team",
                    models.CharField(
                        blank=True, db_column="TEAM", max_length=50, null=True
                    ),
                ),
                (
                    "hr_id",
                    models.CharField(
                        blank=True, db_column="hr_id", max_length=50, null=True
                    ),
                ),
            ],
            options={
                "db_table": "PROJECT_DETAILS",
                "managed": True,
            },
        ),
    ]
