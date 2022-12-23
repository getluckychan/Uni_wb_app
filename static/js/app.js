function showPassword() {
  var x = document.getElementById("id_password");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
function showConfirmPassword() {
  var x = document.getElementById("id_password2");
    if (x.type === "password") {
      x.type = "text";
    }
    else {
      x.type = "password";
    }
}
function showCurrentPassword() {
  var x = document.getElementById("id_password1");
    if (x.type === "password") {
      x.type = "text";
    }
    else {
      x.type = "password";
    }
}

