$(document).ready(function () {
  AllBooks();
  Avatar = "";
  $("#Avatar").on("change", function (e) {
    Avatar = e.target.files[0];
    $("#AvatarName").text(Avatar.name);
  });
  //Show Category Model
  $("#showModel").on("click", function () {
    $("#Title").val("");
    $("#ISBN").val("");
    $("#Coppy").val("");
    $("#Availabe").val("");
    $("#Publisher").val("");
    $("#Summary").val("");
    Author();
    Category();
  });
  //Add Book
  $("#add").on("click", function () {
    const Title = $("#Title").val();
    const Author = $("#Author").val();
    const Category = $("#Category").val();
    const ISBN = $("#ISBN").val();
    const Coppy = $("#Coppy").val();
    const Available = $("#Available").val();
    const Publisher = $("#Publisher").val();
    const Summary = $("#Summary").val();
    if (Title == "") {
      toastr.error("error Please Enter Title");
      // SendMessage("error", "Enter First Name");
    } else if (Author == "") {
      toastr.error("error Please Select Author ");
      // SendMessage("error", "Enter First Name");
    } else if (Category == "") {
      toastr.error("error Please Select Category");
      // SendMessage("error", "Enter First Name");
    } else if (ISBN == "") {
      toastr.error("error Please Enter ISBN Number");
      // SendMessage("error", "Enter First Name");
    } else if (Coppy == "") {
      toastr.error("error Please Enter number of coppies");
      // SendMessage("error", "Enter First Name");
    } else if (Available == "") {
      toastr.error("error Please Enter Available coppies");
      // SendMessage("error", "Enter First Name");
    } else if (Publisher == "") {
      toastr.error("error Please Enter Publisher");
      // SendMessage("error", "Enter First Name");
    } else if (Summary == "") {
      toastr.error("error Please Enter Summary");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("Title", Title);
      formData.append("Author", Author);
      formData.append("Category", Category);
      formData.append("ISBN", ISBN);
      formData.append("Coppy", Coppy);
      formData.append("Available", Available);
      formData.append("Publisher", Publisher);
      formData.append("Summary", Summary);
      formData.append("Avatar", Avatar);
      formData.append("type", "add");
      if (Available > Coppy) {
        toastr.error(
          "error Available coppies must less dhan number of coppies"
        );
      } else {
        $.ajax({
          method: "POST",
          url: URLS + "Library/manage_book/" + 0,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              toastr.success(response.Message);
              $("#AddCategory").modal("hide");
              AllBooks();
            } else {
              toastr.error(response.Message);
            }
          },
          error: function (response) {},
        });
      }
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
        url: URLS + "Library/manage_book/" + ID,
        headers: { "X-CSRFToken": csrftoken },
        processData: false,
        contentType: false,
        data: formData,
        async: true,
        success: function (response) {
          if (!response.isError) {
            toastr.success(response.Message);
            $("#UpdateCategory").modal("hide");
            AllBooks();
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
          url: URLS + "Library/manage_book/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          async: false,
          success: function (response) {
            if (!response.isError) {
              swal(response.Message, {
                icon: "success",
              });
              AllBooks();
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
      url: URLS + "Library/manage_book/" + ID,
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

  function AllBooks() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_book/" + 0,
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
          rows[i].title,
          rows[i].author,
          rows[i].category,
          rows[i].copy,
          rows[i].available,
          rows[i].created_at,
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
          `<td>${dataRows[i][7]}</td>`,
          `
          <button type="button" class="btn btn-info Edit" ID=${dataRows[i][0]}> <i class="far fa-edit"></i></button>
          <button type="button" class="btn btn-danger Delete" ID=${dataRows[i][0]}> <i class="fa fa-trash"></i></button>

          </td>`,
        ])
        .draw();
    }
  }
  function Author() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_author/" + 0,
      processData: false,
      contentType: false,
      data: formData,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        rows = response.Message;
      },
      error: function (response) {},
    });

    var dataRow = "";
    if (rows.length > 0) {
      dataRow = `<option value=''>Select Author</option>`;
      for (var i = 0; i < rows.length; i++) {
        dataRow +=
          `
          <option value='` +
          rows[i].id +
          `'>` +
          rows[i].name +
          `</option>
          `;
      }
      $("#Author").html(dataRow);
    } else {
    }
  }
  function Category() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_category/" + 0,
      processData: false,
      contentType: false,
      data: formData,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        rows = response.Message;
      },
      error: function (response) {},
    });

    var dataRow = "";
    if (rows.length > 0) {
      dataRow = `<option value=''>Select Category</option>`;
      for (var i = 0; i < rows.length; i++) {
        dataRow +=
          `
          <option value='` +
          rows[i].id +
          `'>` +
          rows[i].name +
          `</option>
          `;
      }
      $("#Category").html(dataRow);
    } else {
    }
  }
});
