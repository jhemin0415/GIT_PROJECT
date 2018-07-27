function check_id(){
  var id_value = document.querySelector('#registerID').value;
  if(id_value == ""){
    document.querySelector('.inpID').innerHTML = "아이디를 입력해주세요";
    document.querySelector('.inpID').style.display = "block";
    document.querySelector('.inpID').style.color ="rgb(220, 50, 30)"  ;
  }
  else {
    document.querySelector('.inpID').style.display = "block";
    $.ajax({
      type: 'POST',
      contentType: 'application/json;charset=utf-8',
      url: '/register',
      traditional: 'true',
      data: JSON.stringify({"value": "id", "ID": id_value}),
      dataType: 'json',
      success: function(data){
        if(data.judge == 0){
          document.querySelector('.inpID').innerHTML = "이미 사용된 아이디입니다. 다른 아이디를 입력하세요"
        }
        else {
          document.querySelector('.inpID').innerHTML = "사용가능한 아이디 입니다.";
          document.querySelector('.inpID').style.color="rgb(51, 51, 255)";
        }
      }
    });
  }
}


function check_pw(){
  var mark_valid = document.querySelectorAll('.mark_valid');
  var pw_value = document.querySelector('#registerPW1').value;
  document.querySelector('.inpPW').style.display="block";
  if(pw_value.length < 8){
    mark_valid[0].style.display="block";
    mark_valid[0].innerHTML = "불가";
    mark_valid[0].style.color="rgb(220, 50, 30)";
    document.querySelector('.inpPW').style.color="rgb(220, 50, 30)";
    document.querySelector('.inpPW').innerHTML = "8자 이상으로 입력해주세요";
  }
  else{
    mark_valid[0].style.display="block";
    mark_valid[0].style.color="rgb(51, 51, 255)";
    mark_valid[0].innerHTML = "가능";
    document.querySelector('.inpPW').innerHTML = "";
  }
}


function check_pw_compleate(){
  var mark_valid = document.querySelectorAll('.mark_valid');
  var pw_value1 = document.querySelector('#registerPW1').value;
  var pw_value2 = document.querySelector('#registerPW2').value;
  if(pw_value2 == ""){
    mark_valid[1].style.display="block";
    mark_valid[1].style.color="rgb(220, 50, 30)";
    document.querySelector('.inpPW').style.color="rgb(220, 50, 30)";
    document.querySelector('.inpPW').innerHTML = "비밀번호 재확인을 입력해주세요";
  }
  else if(pw_value1 != pw_value2){
    mark_valid[1].style.display="block";
    mark_valid[1].style.color="rgb(220, 50, 30)";
    document.querySelector('.inpPW').style.color="rgb(220, 50, 30)";
    document.querySelector('.inpPW').innerHTML = "비밀번호가 일치하지 않습니다. 다시 입력해주세요."
  }
  else if(pw_value1 == pw_value2 && pw_value1 != "" && pw_value2 != ""){
    mark_valid[1].style.display = "block";
    mark_valid[1].style.color = "rgb(51, 51, 255)";
    mark_valid[1].innerHTML = "일치";
    $.ajax({
      type: 'POST',
      contentType: 'application/json;charset=utf-8',
      url: '/register',
      traditional: 'true',
      data: JSON.stringify({"value":"compleate_pw", "PW": pw_value2}),
      dataType: 'json',
      success: function(data){
          document.querySelector('.inpPW').innerHTML = "비밀번호가 일치하며 사용가능한 비밀번호 입니다.";
          document.querySelector('.inpPW').style.color="rgb(51, 51, 255)";
      }
    });
  }
  else {
    document.querySelector('.inpPW').innerHTML = "문제 발생";
  }
}


function check_alias(){
  var Username = document.querySelector('#UserName').value;
  $.ajax({
      type: 'POST',
      contentType: 'application/json;charset=utf-8',
      url: '/register',
      traditional: 'true',
      data: JSON.stringify({"value":"alias", "Alias": Username}),
      dataType: 'json',
      success: function(data){
        document.querySelector('.inpAlias').style.display="block";
        if(data.judge == 0){
          document.querySelector('.inpAlias').innerHTML = "이미 사용된 닉네임입니다. 다른 닉네임을 입력하세요";
          document.querySelector('.inpAlias').style.color="rgb(220, 50, 30)";
        }
        else {
          document.querySelector('.inpAlias').innerHTML = "사용가능한 닉네임 입니다.";
          document.querySelector('.inpAlias').style.color="rgb(51, 51, 255)";
        }
      }
  });
}

var email_auth_code;
var auth_confirm = 0;
function send_auth(){
  var email = document.querySelector('#email').value;
  document.querySelector('.inpEmail').style.display="block";
  if(email.includes("@") == true && email.includes(".") == true){
    document.querySelector('.inpEmail').innerHTML = "이메일을 확인했습니다. 입력하신 이메일로 인증번호를 발송하니 확인하여 인증번호를 입력해주세요.";
    document.querySelector('.inpEmail').style.color="rgb(51, 51, 255)";
    $.ajax({
      type: 'POST',
      contentType: 'application/json;charset=utf-8',
      url: '/register',
      traditional: 'true',
      data: JSON.stringify({"value":"email", "email": email}),
      dataType: 'json',
      success: function(response){
        document.querySelector('#inpAuthCode').disabled=false;
        email_auth_code = response.auth_code
      }
    });
  }
  else {
    document.querySelector('.inpEmail').innerHTML = "이메일이 아닙니다. 다시 입력해주세요";
    document.querySelector('.inpEmail').style.color="rgb(220, 50, 30)";
  }
}


function check_auth_number(){
  var auth_num = document.querySelector('#inpAuthCode').value;
  if(auth_num == email_auth_code){
    auth_confirm = 1;
  }
}


function submit(){
  var id_value = document.querySelector('#registerID').value;
  var pw_value = document.querySelector('#registerPW1').value;
  var Username = document.querySelector('#UserName').value;
  var email = document.querySelector('#email').value;
  if(auth_confirm == 1){
    $.ajax({
        type: 'POST',
        contentType: 'application/json;charset=utf-8',
        url: '/register',
        traditional: 'true',
        data: JSON.stringify({"value": "submit", "ID": id_value, "PW": pw_value, "UserName": Username, "Email": email}),
        dataType: 'json',
        success: function(data){
          if(data.message == 'success'){
            alert('회원가입을 성공했습니다.')
            location.replace('/login');
          }
          else {
            document.querySelector('.inpAuth').style.display="block";
            document.querySelector('.inpAuth').style.color="rgb(220, 50, 30)";
            document.querySelector('.inpAuth').innerHTML="회원가입 실패했습니다."
          }
        }
      });
    }
    else{
      document.querySelector('.inpAuth').style.display="block";
      document.querySelector('.inpAuth').style.color="rgb(220, 50, 30)";
      document.querySelector('.inpAuth').innerHTML="이메일 인증이 완료되지 않았습니다."
    }
};
