$(document).ready(function () {
  AllFine();
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
  });
  //Add Reading Books
  $("#add").on("click", function () {
    const time_in = $("#In").val();
    const time_out = $("#Out").val();
    const Member = $("#Member").val();

    if (Member == "") {
      toastr.error("error Please Enter Member name");
      // SendMessage("error", "Enter First Name");
    } else if (time_in == "") {
      toastr.error("error Please Time in ");
      // SendMessage("error", "Enter First Name");
    } else if (time_out == "") {
      toastr.error("error Please Enter time out ");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("time_in", time_in);
      formData.append("time_out", time_out);
      formData.append("Member", Member);
      formData.append("type", "add");
      if (time_in > time_out) {
        toastr.error("error Sorry Time in  must less then time out");
      } else {
        $.ajax({
          method: "POST",
          url: URLS + "Library/manage_reading/" + 0,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              toastr.success(response.Message);
              $("#AddReading").modal("hide");
              AllFine();
            } else {
              toastr.error(response.Message);
            }
          },
          error: function (response) {},
        });
      }
    }
  });
  //Update Reading book
  $("#update").on("click", function () {
    const time_in = $("#UIn").val();
    const time_out = $("#UOut").val();
    const Member = $("#UMember").val();
    const ID = $("#UMember").val();

    if (Member == "") {
      toastr.error("error Please Enter Member name");
      // SendMessage("error", "Enter First Name");
    } else if (time_in == "") {
      toastr.error("error Please Time in ");
      // SendMessage("error", "Enter First Name");
    } else if (time_out == "") {
      toastr.error("error Please Enter time out ");
      // SendMessage("error", "Enter First Name");
    } else {
      let formData = new FormData();
      formData.append("time_in", time_in);
      formData.append("time_out", time_out);
      formData.append("Member", Member);
      if (time_in > time_out) {
        toastr.error("error Sorry Time in  must less then time out");
      } else {
        $.ajax({
          method: "POST",
          url: URLS + "Library/manage_reading/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              toastr.success(response.Message);
              $("#UpdateReading").modal("hide");
              AllFine();
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
          url: URLS + "Library/manage_reading/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          async: false,
          success: function (response) {
            if (!response.isError) {
              swal(response.Message, {
                icon: "success",
              });
              AllFine();
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
    $("#UpdateReading").modal("show");
    $.ajax({
      async: false,
      method: "GET",
      url: URLS + "Library/manage_reading/" + ID,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          Member();
          $("#UMember").val(response.Message.member);
          $("#UIn").val(response.Message.time_in);
          $("#UOut").val(response.Message.time_out);
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

  function AllFine() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "get");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_fine/" + 0,
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
          rows[i].Phone,
          rows[i].time_in,
          rows[i].time_out,
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
          `
          <button type="button" class="btn btn-info Edit" ID='${dataRows[i][0]}'> <i class="far fa-edit"></i></button>
          <button type="button" class="btn btn-danger Delete" ID='${dataRows[i][0]}'> <i class="fa fa-trash"></i></button>
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
});
