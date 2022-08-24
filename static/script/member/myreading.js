$(document).ready(function () {
  const ID = $("#Member").attr("IDs");
  if (ID != "" && ID != undefined) {
    myReading(ID);
  }

  function myReading(id) {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "getmyreading");
    formData.append("Member", id);
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_member_dashbord/" + 0,
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
          
          
        ])
        .draw();
    }
  }

});
