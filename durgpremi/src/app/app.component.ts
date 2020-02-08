import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  serverData: JSON;
  employeeData: JSON;
  name;
  mobileno;
  page = 1;
  otpResponse;
  mailid;
  fullname;
  username;
  password;
 
  title = 'Durgpremi..';
  
  constructor(private httpClient: HttpClient) {

  }
  
  changepage(){
    if(this.page == 1){
      this.page = 0;
    }
    else{
      this.page = 1;
    }
  }
  
  userregister(mailid,fullname,username,password) {
    this.mailid = mailid;
    this.fullname = fullname;
    this.username = username;
    this.password = password;

    console.log(mailid,fullname,username,password);
    let userdata = JSON.stringify({'mailid':mailid,'fullname':fullname,'username':username,'password':password});
    console.log("userdata ==> ",userdata);

    this.httpClient.get('http://127.0.0.1:5002/userregister',{ params:{ senduserdata : userdata }}).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
      
      this.otpResponse = this.serverData['response'];
      if(this.otpResponse == 'success')
      {
        document.getElementById('otpDiv').style.display = "block";
      }
    })
  }

  otpVerify(otp) {
    let userdata = JSON.stringify({'otp': otp,'mailid':this.mailid,'fullname':this.fullname,'username':this.username,'password':this.password});
    console.log("otp------->>>>>>",userdata)
    this.httpClient.get('http://127.0.0.1:5002/otpverification', { params:  { senduserdata : userdata } }).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }
 
  userlogin(u, p){
    var logininfo = JSON.stringify({ 'userid': u, 'password':p });
    console.log("logininfo--->>>",logininfo)
    this.httpClient.get('http://127.0.0.1:5002/userlogin/', { params:  { logininfo : logininfo } }).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }
  mobilecall() {
    var mobileno = JSON.stringify({'first':'9970679900'});
    console.log("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$");
    this.httpClient.get('http://127.0.0.1:5002/ap/', { params:  { phone : mobileno } }).subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }

  sayHi() {
    this.httpClient.get('http://127.0.0.1:5002/').subscribe(data => {
      this.serverData = data as JSON;
      console.log(this.serverData);
    })
  }

  getAllEmployees() {
    this.httpClient.get('http://127.0.0.1:5002/employees').subscribe(data => {
      this.employeeData = data as JSON;
      var employee = this.employeeData['employees'];
      console.log("---------->",employee)
      console.log("---------->",employee[0].name)
      console.log("---------->",employee.length)
      console.log("---------->",typeof(employee))
      this.name = employee[0].name;
    })
  }
}
