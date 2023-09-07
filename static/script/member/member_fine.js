$(document).ready(function () {
  const ID = $("#Member").attr("IDs");
  if (ID != "" && ID != undefined) {
    AllFine(ID);
  }

  function AllFine(id) {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "memberfine");
    formData.append("Member", id);
    $.ajax({
      method: "POST",
      url: "/Library/manage_member_dashbord/" + 0,
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
        ])
        .draw();
    }
  }
});
