$(document).ready(function () {
  AllBookBorrow();
  Avatar = "";
  $("#Avatar").on("change", function (e) {
    Avatar = e.target.files[0];
    $("#AvatarName").text(Avatar.name);
  });
  //Show Book Model
  $("#showModel").on("click", function () {
    $("#Start").val("");
    $("#End").val("");
    $("#NBook").val("");

    Member();
    Book();
  });
  //Add Book Borrow
  $("#add").on("click", function () {
    const Start = $("#Start").val();
    const End = $("#End").val();
    const NBook = $("#NBook").val();
    const Member = $("#Member").val();
    const Book = $("#Book").val();

    if (Member == "") {
      toastr.error("error Please Enter Member name");
      // SendMessage("error", "Enter First Name");
    } else if (Book == "") {
      toastr.error("error Please Select Book ");
      // SendMessage("error", "Enter First Name");
    } else if (Start == "") {
      toastr.error("error Please Enter Start Date");
      // SendMessage("error", "Enter First Name");
    } else if (End == "") {
      toastr.error("error Please Enter End Date");
      // SendMessage("error", "Enter First Name");
    } else if (NBook == "") {
      toastr.error("error Please Enter  number of book");
    } else {
      let formData = new FormData();
      formData.append("Start", Start);
      formData.append("End", End);
      formData.append("Member", Member);
      formData.append("Book", Book);
      formData.append("NBook", NBook);
      formData.append("type", "add");
      if (Start > End) {
        toastr.error("error Start Date  must less dhan End Date");
      } else {
        $.ajax({
          method: "POST",
          url: URLS + "Library/manage_bookborrow/" + 0,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              toastr.success(response.Message);
              $("#AddBorrow").modal("hide");
              AllBookBorrow();
            } else {
              toastr.error(response.Message);
            }
          },
          error: function (response) {},
        });
      }
    }
  });

  //Update Book Borrow
  $("#update").on("click", function () {
    const Start = $("#UStart").val();
    const End = $("#UEnd").val();
    const NBook = $("#UNBook").val();
    const Member = $("#UMember").val();
    const Book = $("#UBook").val();
    const ID = $("#ID").val();

    if (Member == "") {
      toastr.error("error Please Enter Member name");
      // SendMessage("error", "Enter First Name");
    } else if (Book == "") {
      toastr.error("error Please Select Book ");
      // SendMessage("error", "Enter First Name");
    } else if (Start == "") {
      toastr.error("error Please Enter Start Date");
      // SendMessage("error", "Enter First Name");
    } else if (End == "") {
      toastr.error("error Please Enter End Date");
      // SendMessage("error", "Enter First Name");
    } else if (NBook == "") {
      toastr.error("error Please Enter  number of book");
    } else {
      let formData = new FormData();
      formData.append("Start", Start);
      formData.append("End", End);
      formData.append("Member", Member);
      formData.append("Book", Book);
      formData.append("NBook", NBook);
      if (Start > End) {
        toastr.error("error Start Date  must less dhan End Date");
      } else {
        $.ajax({
          method: "POST",
          url: URLS + "Library/manage_bookborrow/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              toastr.success(response.Message);
              $("#UpdateBorrow").modal("hide");
              AllBookBorrow();
            } else {
              toastr.error(response.Message);
            }
          },
          error: function (response) {},
        });
      }
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
          url: URLS + "Library/manage_bookborrow/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          async: false,
          success: function (response) {
            if (!response.isError) {
              swal(response.Message, {
                icon: "success",
              });
              AllBookBorrow();
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
    $("#UpdateBorrow").modal("show");
    $.ajax({
      async: false,
      method: "GET",
      url: URLS + "Library/manage_bookborrow/" + ID,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          Member();
          Book();
          $("#UMember").val(response.Message.Member);
          $("#UBook").val(response.Message.BookID);
          $("#UNBook").val(response.Message.NBook);
          $("#UEnd").val(response.Message.end_date);
          $("#UStart").val(response.Message.start_date);
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

  function AllBookBorrow() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_bookborrow/" + 0,
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
          rows[i].member,
          rows[i].BookName,
          rows[i].author,
          rows[i].category,
          rows[i].start,
          rows[i].end,
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
          <button type="button" class="btn btn-info Edit" ID='${dataRows[i][0]}'> <i class="far fa-edit"></i></button>
          <button type="button" class="btn btn-danger Delete" ID='${dataRows[i][0]}'> <i class="fa fa-trash"></i></button>
          <button type="button" class="btn btn-success Show" ID='${dataRows[i][0]}'> <i class="fa fa-eye"></i></button>

          </td>`,
        ])
        .draw();
    }
  }
  function Member() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "getmember");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_member/" + 0,
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
      dataRow = `<option value=''>Select Member</option>`;
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
      $("#Member").html(dataRow);
      $("#UMember").html(dataRow);
    } else {
    }
  }
  function Book() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_book/" + 0,
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
      dataRow = `<option value=''>Select Book</option>`;
      for (var i = 0; i < rows.length; i++) {
        dataRow +=
          `
          <option value='` +
          rows[i].id +
          `'>` +
          rows[i].title +
          `</option>
          `;
      }
      $("#Book").html(dataRow);
      $("#UBook").html(dataRow);
    } else {
    }
  }
});
