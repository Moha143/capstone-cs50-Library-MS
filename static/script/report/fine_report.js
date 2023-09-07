$(document).ready(function () {
  Member();
  const ID = $("#Member").val();
  if (ID == "" || ID == 0 || ID == null || ID == undefined) {
  } else {
    AllFine();
  }

  $("#Member").on("change", function () {
    const IDs = $(this).val();
    if (IDs == "" || IDs == 0 || IDs == null || IDs == undefined) {
    } else {
      AllFine();
    }
  });
  function AllFine() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "finedetails");
    formData.append("Member", $("#Member").val());
    $.ajax({
      method: "POST",
      url: "/Library/manage_fine/" + 0,
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
          rows[i].IDs,
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
  function Member() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "getmember");
    $.ajax({
      method: "POST",
      url: "/Library/manage_member/" + 0,
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
      dataRow = `<option value="All">All Member</option>`;
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
    } else {
    }
  }
});
