$(document).ready(function () {
  AllCategory();
  Avatar = "";
  //Show Category Model
  $("#showModel").on("click", function () {
    $("#CName").val("");
  });
  //Add Category
  $("#add").on("click", function () {
    const CName = $("#CName").val();
    if (CName == "") {
      toastr.error("error Please Enter Category Name");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("CName", CName);
      formData.append("type", "add");
      $.ajax({
        method: "POST",
        url: URLS + "Library/manage_category/" + 0,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: true,
        success: function (response) {
          if (!response.isError) {
            toastr.success(response.Message);
            $("#AddCategory").modal("hide");
            AllCategory();
          } else {
            toastr.error(response.Message);
          }
        },
        error: function (response) {},
      });
    }
  });
  //Update Category
  $("#update").on("click", function () {
    const CName = $("#UCName").val();
    const ID = $("#ID").val();
    if (CName == "") {
      toastr.error("error Please Enter Category Name");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("CName", CName);
      $.ajax({
        method: "POST",
        url: URLS + "Library/manage_category/" + ID,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: true,
        success: function (response) {
          if (!response.isError) {
            toastr.success(response.Message);
            $("#UpdateCategory").modal("hide");
            AllCategory();
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
          url: URLS + "Library/manage_category/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          async: false,
          success: function (response) {
            if (!response.isError) {
              swal(response.Message, {
                icon: "success",
              });
              AllCategory();
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
    $("#UpdateCategory").modal("show");
    $.ajax({
      async: false,
      method: "GET",
      url: URLS + "Library/manage_category/" + ID,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          $("#UCName").val(response.Message.name);
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

  function AllCategory() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_category/" + 0,
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
