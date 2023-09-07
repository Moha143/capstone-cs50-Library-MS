$(document).ready(function () {
  AllAuthor();
  Avatar = "";
  //Show Author Model
  $("#showModel").on("click", function () {
    $("#FName").val("");
  });
  //Add Author
  $("#add").on("click", function () {
    const FName = $("#FName").val();
    if (FName == "") {
      toastr.error("error Please Enter Author Name");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("FName", FName);
      formData.append("type", "add");
      $.ajax({
        method: "POST",
        url: "/Library/manage_author/" + 0,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: true,
        success: function (response) {
          if (!response.isError) {
            swal(response.Message, {
              icon: "success",
            });
            $("#AddAuthor").modal("hide");
            AllAuthor();
          } else {
            swal(response.Message, {
              icon: "error",
            });
          }
        },
        error: function (response) {},
      });
    }
  });
  //Update Author
  $("#update").on("click", function () {
    const FName = $("#UFName").val();
    const ID = $("#ID").val();
    if (FName == "") {
      toastr.error("error Please Enter Author Name");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("FName", FName);
      $.ajax({
        method: "POST",
        url: "/Library/manage_author/" + ID,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: true,
        success: function (response) {
          if (!response.isError) {
            swal(response.Message, {
              icon: "success",
            });
            $("#UpdateAuthor").modal("hide");
            AllAuthor();
          } else {
            swal(response.Message, {
              icon: "error",
            });
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
          url: "/Library/manage_author/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          async: false,
          success: function (response) {
            if (!response.isError) {
              swal(response.Message, {
                icon: "success",
              });
              AllAuthor();
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
    $("#UpdateAuthor").modal("show");
    $.ajax({
      async: false,
      method: "GET",
      url: "/Library/manage_author/" + ID,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          $("#UFName").val(response.Message.name);
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

  function AllAuthor() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: "/Library/manage_author/" + 0,
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
        dataRows.push([rows[i].id, num++, rows[i].name, rows[i].created_at]);
      }
    }
    let dataTable = $("#datatable").DataTable().clear();
    for (var i = 0; i < dataRows.length; i++) {
      dataTable.row
        .add([
          `<tr><td>${dataRows[i][1]}</td>`,
          `<td>${dataRows[i][2]}</td>`,
          `<td>${dataRows[i][3]}</td>`,
          `
          <button type="button" class="btn btn-info Edit" ID=${dataRows[i][0]}> <i class="far fa-edit"></i></button>
          <button type="button" class="btn btn-danger Delete" ID=${dataRows[i][0]}> <i class="fa fa-trash"></i></button>

          </td>`,
        ])
        .draw();
    }
  }
});
