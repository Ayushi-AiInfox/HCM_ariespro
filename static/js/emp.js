//add emp
$(document).ready(function () {
    $("#empManager").select2();
    setTimeout(function () {
        $(".successMessageCard").fadeOut();
    }, 7000);

    $("#contactNo, #altContact, #acct_No").keypress(function(evt){
        evt = (evt) ? evt : window.event;
        var charCode = (evt.which) ? evt.which : evt.keyCode;
        if (charCode > 31 && (charCode < 48 || charCode > 57)) {
            return false;
        }
        return true;
    });

    $("#AddPlus").on('click', function () {
        const listbox = document.querySelector('#addEmployeeDesignation');
        const enterDes = document.querySelector('#empDesignation');
        if ($("#empDesignation").val() == '') {
            document.getElementById('emp_insert').innerHTML = "Enter designation";
            return false;
        } else {
            var search = $('#empDesignation').val();
            console.log(search);
            const option = new Option(enterDes.value, enterDes.value);
            // add it to the list
            listbox.append(option);
            document.getElementById('DesignationAdd').innerHTML = "Designation added";
            setTimeout(function () {
                $("#DesignationAdd").fadeOut();
            }, 5000);
        }
    });
});


$(document).ready(function () {
    var DOB = document.getElementById('birthDate');
    var DOJ = document.getElementById('joiningDate');

    $("#add_emp").click(function () {

        if ($('#fname').val() == '' || $('#lname').val() == '' || $('#uname').val() == '' || $('#pwd').val() == '' || $('#mailID').val() == ''
            || !DOB.value || !DOJ.value || '0' === $('#empGender').val() || '0' === $('#empManager').val() || '0' === $('#empHR').val() || $('#contactNo').val() == '' ||
            $('#empSalary').val() == '' || $('#bank_name').val() == '' || $('#acct_No').val() == '' || $("#empDesignation").val() == '' ||
            $('#ifsc_code').val() == '' || $('#empBranch').val() == '' || $('#currProject').val() == '' || $('#empAddr').val() == '') {
            document.getElementById("firstName").innerHTML = "Enter first name";
            document.getElementById('LastName').innerHTML = "Enter last name";
            document.getElementById('userName').innerHTML = "Enter username date";
            document.getElementById('emailID').innerHTML = "Enter Email-ID";
            document.getElementById('dateofBirth').innerHTML = "Select birth date";
            document.getElementById('gender').innerHTML = "Select gender";
            document.getElementById('passwd').innerHTML = "Enter password";
            document.getElementById('emp_insert').innerHTML = "Enter designation";
            document.getElementById('dateJoin').innerHTML = "Select joining date";

            document.getElementById('phoneNo').innerHTML = "Enter contact";
            document.getElementById('salary').innerHTML = "Enter salary";
            document.getElementById('bankName').innerHTML = "Enter bank name";
            document.getElementById('acctNo').innerHTML = "Enter account no.";
            document.getElementById('ifscCode').innerHTML = "Enter IFSC code";
            document.getElementById('branchName').innerHTML = "Enter branch name";
            document.getElementById('currentProject').innerHTML = "Enter project name";
            document.getElementById('manName').innerHTML = "Select manager";
            document.getElementById('HRName').innerHTML = "Select HR";
            document.getElementById('addr').innerHTML = "Enter address";
            return false;
        }
    });

    $("#fname, #lname, #uname, #pwd, #mailID, #contactNo, #empDesignation, #empSalary, #bank_name, #acct_No, #ifsc_code, #empBranch, #currProject, #empAddr").keyup(function () {
        if ($('#fname').val() != '') {
            $("#firstName").hide();
        } else {
            $("#firstName").show();
        }
        if ($('#lname').val() != '') {
            $("#LastName").hide();
        } else {
            $("#LastName").show();
        }
        if ($('#empDesignation').val() != '') {
            $("#emp_insert").hide();
        } else {
            $("#emp_insert").show();
        }
        if ($('#uname').val() != '') {
            $("#userName").hide();
        } else {
            $("#userName").show();
        }
        if ($('#pwd').val() != '') {
            $("#passwd").hide();
        } else {
            $("#passwd").show();
        }
        if ($('#mailID').val() != '') {
            $("#emailID").hide();
        } else {
            $("#emailID").show();
        }
        if ($('#contactNo').val() != '') {
            $("#phoneNo").hide();
        } else {
            $("#phoneNo").show();
        }
        if ($('#empSalary').val() != '') {
            $("#salary").hide();
        } else {
            $("#salary").show();
        }
        if ($('#bank_name').val() != '') {
            $("#bankName").hide();
        } else {
            $("#bankName").show();
        }
        if ($('#acct_No').val() != '') {
            $("#acctNo").hide();
        } else {
            $("#acctNo").show();
        }
        if ($('#ifsc_code').val() != '') {
            $("#ifscCode").hide();
        } else {
            $("#ifscCode").show();
        }
        if ($('#empBranch').val() != '') {
            $("#branchName").hide();
        } else {
            $("#branchName").show();
        }
        if ($('#currProject').val() != '') {
            $("#currentProject").hide();
        } else {
            $("#currentProject").show();
        }
        if ($('#empAddr').val() != '') {
            $("#addr").hide();
        } else {
            $("#addr").show();
        }
    });
    $('#birthDate, #empGender, #joiningDate, #empManager, #empHR').change(function () {

        if (DOB.value) {
            $("#dateofBirth").hide();
        } else {
            $("#dateofBirth").show();
        }
        if (DOJ.value) {
            $("#dateJoin").hide();
        } else {
            $("#dateJoin").show();
        }
        if ('0' !== $('#empGender').val()) {
            $("#gender").hide();
        } else {
            $("#gender").show();
        }
        if ('0' !== $('#empManager').val()) {
            $("#manName").hide();
        } else {
            $("#manName").show();
        }
        if ('0' !== $('#empHR').val()) {
            $("#HRName").hide();
        } else {
            $("#HRName").show();
        }
    });
});

//edit emp
// $(document).ready(function () {
//     $("#editempManager").select2();
//     setTimeout(function () {
//         $(".successMessageCard").fadeOut();
//     }, 7000);

//     $("#editcontactNo, #editaltContact, #editacct_No").keypress(function(evt){
//         evt = (evt) ? evt : window.event;
//         var charCode = (evt.which) ? evt.which : evt.keyCode;
//         if (charCode > 31 && (charCode < 48 || charCode > 57)) {
//             return false;
//         }
//         return true;
//     });

//     $("#AddPlus-edit").on('click', function () {
//         const listbox = document.querySelector('#editaddEmployeeDesignations');
//         const enterDes = document.querySelector('#editempDesignations');
//         if ($("#editempDesignations").val() == '') {
//             document.getElementById('editemp_insert').innerHTML = "Enter designation";
//             return false;
//         } else {
//             var search = $('#editempDesignations').val();
//             console.log(search);
//             const option = new Option(enterDes.value, enterDes.value);
//             // add it to the list
//             listbox.append(option);
//             document.getElementById('editDesignationAdd').innerHTML = "Designation added";
//             setTimeout(function () {
//                 $("#editDesignationAdd").fadeOut();
//             }, 5000);
//         }
//     });
// });

// $(document).ready(function () {
//     var DOB1 = document.getElementById('editbirthDate');
//     var DOJ1 = document.getElementById('editjoiningDate');

//     $("#edit_emp").click(function () {

//         if ($('#editfname').val() == '' || $('#editlname').val() == '' || $('#edituname').val() == '' || $('#editpwd').val() == '' || $('#editmailID').val() == ''
//             || !DOB1.value || !DOJ1.value || '0' === $('#editempGender').val() || '0' === $('#editempManager').val() || '0' === $('#editempHR').val() || $('#editcontactNo').val() == '' ||
//             $('#editempSalary').val() == '' || $('#editbank_name').val() == '' || $('#editacct_No').val() == '' || $("#editempDesignations").val() == '' ||
//             $('#editifsc_code').val() == '' || $('#editempBranch').val() == '' || $('#editcurrProject').val() == '' || $('#editempAddr').val() == '') {
//             document.getElementById("editfirstName").innerHTML = "Enter first name";
//             document.getElementById('editLastName').innerHTML = "Enter last name";
//             document.getElementById('edituserName').innerHTML = "Enter username date";
//             document.getElementById('editemailID').innerHTML = "Enter Email-ID";
//             document.getElementById('editdateofBirth').innerHTML = "Select birth date";
//             document.getElementById('editgender').innerHTML = "Select gender";
//             document.getElementById('editpasswd').innerHTML = "Enter password";
//             document.getElementById('editdateJoin').innerHTML = "Select joining date";
//             document.getElementById('editemp_insert').innerHTML = "Enter designation";

//             document.getElementById('editphoneNo').innerHTML = "Enter contact";
//             document.getElementById('editsalary').innerHTML = "Enter salary";
//             document.getElementById('editbankName').innerHTML = "Enter bank name";
//             document.getElementById('editacctNo').innerHTML = "Enter account no.";
//             document.getElementById('editifscCode').innerHTML = "Enter IFSC code";
//             document.getElementById('editbranchName').innerHTML = "Enter branch name";
//             document.getElementById('editcurrentProject').innerHTML = "Enter project name";
//             document.getElementById('editmanName').innerHTML = "Select manager";
//             document.getElementById('editHRName').innerHTML = "Select HR";
//             document.getElementById('editaddr').innerHTML = "Enter address";
//             return false;
//         }
//     });

//     $("#editfname, #editlname, #edituname, #editpwd, #editmailID, #editcontactNo, #editempDesignation, #editempSalary, #editbank_name, #editacct_No, #editifsc_code, #editempBranch, #editcurrProject, #editempAddr").keyup(function () {
//         if ($('#editfname').val() != '') {
//             $("#editfirstName").hide();
//         } else {
//             $("#editfirstName").show();
//         }
//         if ($('#editlname').val() != '') {
//             $("#editLastName").hide();
//         } else {
//             $("#editLastName").show();
//         }
//         if ($('#editempDesignation').val() != '') {
//             $("#editemp_insert").hide();
//         } else {
//             $("#editemp_insert").show();
//         }
//         if ($('#edituname').val() != '') {
//             $("#edituserName").hide();
//         } else {
//             $("#edituserName").show();
//         }
//         if ($('#editpwd').val() != '') {
//             $("#editpasswd").hide();
//         } else {
//             $("#editpasswd").show();
//         }
//         if ($('#editmailID').val() != '') {
//             $("#editemailID").hide();
//         } else {
//             $("#editemailID").show();
//         }
//         if ($('#editcontactNo').val() != '') {
//             $("#editphoneNo").hide();
//         } else {
//             $("#editphoneNo").show();
//         }
//         if ($('#editempSalary').val() != '') {
//             $("#editsalary").hide();
//         } else {
//             $("#editsalary").show();
//         }
//         if ($('#editbank_name').val() != '') {
//             $("#editbankName").hide();
//         } else {
//             $("#editbankName").show();
//         }
//         if ($('#editacct_No').val() != '') {
//             $("#editacctNo").hide();
//         } else {
//             $("#editacctNo").show();
//         }
//         if ($('#editifsc_code').val() != '') {
//             $("#editifscCode").hide();
//         } else {
//             $("#editifscCode").show();
//         }
//         if ($('#editempBranch').val() != '') {
//             $("#editbranchName").hide();
//         } else {
//             $("#editbranchName").show();
//         }
//         if ($('#editcurrProject').val() != '') {
//             $("#editcurrentProject").hide();
//         } else {
//             $("#editcurrentProject").show();
//         }
//         if ($('#editempAddr').val() != '') {
//             $("#editaddr").hide();
//         } else {
//             $("#editaddr").show();
//         }
//     });
//     $('#editbirthDate, #editempGender, #editjoiningDate, #editempManager, #editempHR').change(function () {

//         if (DOB1.value) {
//             $("#editdateofBirth").hide();
//         } else {
//             $("#editdateofBirth").show();
//         }
//         if (DOJ1.value) {
//             $("#editdateJoin").hide();
//         } else {
//             $("#editdateJoin").show();
//         }
//         if ('0' !== $('#editempGender').val()) {
//             $("#editgender").hide();
//         } else {
//             $("#editgender").show();
//         }
//         if ('0' !== $('#editempManager').val()) {
//             $("#editmanName").hide();
//         } else {
//             $("#editmanName").show();
//         }
//         if ('0' !== $('#editempHR').val()) {
//             $("#editHRName").hide();
//         } else {
//             $("#editHRName").show();
//         }
//     });
// });