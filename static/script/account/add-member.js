$(document).ready(function () {
  Avatar = "";
  $("#Avatar").on("change", function (e) {
    Avatar = e.target.files[0];

    $("#AvatarName").text(Avatar.name);
  });
  $("#save").on("click", function () {
    const FName = $("#FName").val();
    const LName = $("#LName").val();
    const Gender = $("#Gender").val();
    const Email = $("#Email").val();
    const Username = $("#Username").val();
    const Phone = $("#Phone").val();

    if (FName == "") {
      toastr.error("error Please Enter First Name");
    } else if (LName == "") {
      toastr.error("Warning Please Enter Last Name");
    } else if (Email == "") {
      toastr.error("Warning Please Enter Email Address");
    } else if (Username == "") {
      toastr.error("Warning Please Enter username");
    } else if (Gender == "") {
      toastr.error("Warning Please Select Gender");
    } else if (Phone == "") {
      toastr.error("Warning Please Phone Number");
    } else if (Avatar == "") {
      toastr.error("Warning Please Enter Image");
    } else {
      let formData = new FormData();
      formData.append("FName", FName);
      formData.append("LName", LName);
      formData.append("Email", Email);
      formData.append("Gender", Gender);
      formData.append("Phone", Phone);
      formData.append("Username", Username);
      formData.append("type", "add");
      formData.append("Avatar", Avatar);
      $.ajax({
        method: "POST",
        url: URLS + "Library/manage_member/" + 0,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: false,
        success: function (response) {
          if (!response.isError) {
            swal({
              title: "GOOD !!!!",
              text: response.Message,
              icon: "success",
              buttons: true,
              dangerMode: false,
            }).then((ok) => {
              if (ok) {
                window.location.reload();
              } else {
                window.location.reload();
              }
            });

            // toastr.success(response.Message);
          } else {
            toastr.error(response.Message);
          }
        },
        error: function (response) {},
      });
    }
  });
});
