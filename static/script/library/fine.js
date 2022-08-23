$(document).ready(function () {
  AllFine();

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
          rows[i].phone,
          rows[i].book,
          rows[i].amount,
          rows[i].paid,
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
          <button type="button" class="btn btn-info Show" ID='${dataRows[i][0]}'> <i class="fa fa-print"></i></button>
          <button type="button" class="btn btn-danger Delete" ID='${dataRows[i][0]}'> <i class="fa fa-trash"></i></button>
          </td>`,
        ])
        .draw();
    }
  }
  $("#datatable tbody").on("click", ".Show", function () {
    const ID = $(this).attr("ID");
    if (ID != "" && ID != undefined) {
      $.ajax({
        async: false,
        method: "GET",
        url: URLS + "Library/manage_fine/" + ID,
        headers: { "X-CSRFToken": csrftoken },
        async: false,
        success: function (response) {
          if (!response.isError) {
            sessionStorage.setItem("Fine", JSON.stringify(response.Message));
            window.location.replace(URLS + "Library/print_fine");
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
          url: URLS + "Library/manage_fine/" + ID,
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
});
