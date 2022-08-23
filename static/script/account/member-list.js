$(document).ready(function () {
  AllMembers();
  Avatar = "";
  $("#save").on("click", function () {
    const FName = $("#FName").val();
    const LName = $("#LName").val();
    const Gender = $("#Gender").val();
    const Email = $("#Email").val();
    const Phone = $("#Phone").val();
    const Username = $("#Username").val();
    const ID = $("#ID").val();
    if (FName == "") {
      toastr.error("error Please Enter First Name");
      // SendMessage("error", "Enter First Name");
    } else if (LName == "") {
      toastr.error("Warning Please Enter Last Name");
    } else if (Username == "") {
      toastr.error("Warning Please Enter Username");
    } else if (Email == "") {
      toastr.error("Warning Please Enter Email Address");
    } else if (Gender == "") {
      toastr.error("Warning Please Select Gender");
    } else if (Phone == "") {
      toastr.error("Warning Please Phone Number");
    } else {
      let formData = new FormData();
      formData.append("FName", FName);
      formData.append("LName", LName);
      formData.append("Email", Email);
      formData.append("Phone", Phone);
      formData.append("Username", Username);
      formData.append("Gender", Gender);
      $.ajax({
        method: "POST",
        url: URLS + "Library/manage_member/" + ID,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: true,
        success: function (response) {
          if (!response.isError) {
            toastr.success(response.Message);
            $("#member").modal("hide");
            AllMembers();
          } else {
            toastr.error(response.Message);
          }
        },
        error: function (response) {},
      });
    }
  });

  $("#datatable tbody").on("click", ".Delete", function () {
    const ID = $(this).attr("ID");
    swal({
      title: "Are you sure?",
      text: "Once deleted, you will not be able to recover this data!",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((willDelete) => {
      if (willDelete) {
        $.ajax({
          async: true,
          method: "DELETE",
          url: URLS + "Library/manage_member/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          async: false,
          success: function (response) {
            if (!response.isError) {
              swal(response.Message, {
                icon: "success",
              });
              AllMembers();
            } else {
              swal(response.Message, {
                icon: "error",
              });
            }
          },
          error: function (response) {},
        });
      } else {
      }
    });
  });
  $("#datatable tbody").on("click", ".Edit", function () {
    const ID = $(this).attr("ID");
    $("#member").modal("show");
    $.ajax({
      async: false,
      method: "GET",
      url: URLS + "Library/manage_member/" + ID,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          $("#FName").val(response.Message.first_name);
          $("#LName").val(response.Message.last_name);
          $("#Gender").val(response.Message.gender);
          $("#Email").val(response.Message.email);
          $("#Phone").val(response.Message.phone);
          $("#Username").val(response.Message.username);
          $("#ID").val(response.Message.id);
        } else {
          swal(response.Message, {
            icon: "error",
          });
        }
      },
      error: function (response) {},
    });
  });

  function AllMembers() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_member/" + 0,
      headers: { "X-CSRFToken": csrftoken },
      processData: false,
      contentType: false,
      data: formData,
      async: false,
      success: function (response) {
        if (response.Message != 0) {
          rows = response.Message;
        } else {
          $("#datatable").DataTable().clear().draw();
        }
      },
      error: function (response) {},
    });

    let dataRows = [];
    let num = 1;
    if (rows.length > 0) {
      for (var i = 0; i < rows.length; i++) {
        dataRows.push([
          rows[i].id,
          num++,
          rows[i].username,
          rows[i].name,
          rows[i].email,
          rows[i].phone,
          rows[i].gender,
          rows[i].avatar,
          rows[i].date_joined,
          rows[i].is_active,
        ]);
      }
    }
    let dataTable = $("#datatable").DataTable().clear();
    for (var i = 0; i < dataRows.length; i++) {
      dataTable.row
        .add([
          `<tr><td>${dataRows[i][1]}</td>`,
          `<td>${dataRows[i][2]}</td>`,
          `<td>${dataRows[i][3]}</td>`,
          `<td>${dataRows[i][4]}</td>`,
          `<td>${dataRows[i][5]}</td>`,
          `<td>${dataRows[i][6]}</td>`,
          `<td>${dataRows[i][8]}</td>`,
          `
          <button type="button" class="btn btn-info Edit" ID=${dataRows[i][0]}> <i class="far fa-edit"></i></button>
          <button type="button" class="btn btn-danger Delete" ID=${dataRows[i][0]}> <i class="fa fa-trash"></i></button>

          </td>`,
        ])
        .draw();
    }
  }
});
