$(document).ready(function () {
  Author();
  Category();
  Book();
  users();
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
      dataRow = `<option value='All'>All Author</option>`;
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
  $("#Author").on("change", function () {
    Book();
  });
  $("#Category").on("change", function () {
    Book();
  });
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
      dataRow = `<option value='All'>All Category</option>`;
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
  function Book() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "getbook");
    formData.append("Category", $("#Category").val());
    formData.append("Author", $("#Author").val());

    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_dashboard/" + 0,
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
      for (var i = 0; i < rows.length; i++) {
        dataRow += `
          <div class="filtr-item col-ms-2" >
          <a href="/media/${rows[i].image}" data-toggle="lightbox"
            data-title=${rows[i].title}>
            <img src="/media/${rows[i].image}" class="img-fluid mb-2"
              alt="white sample" />
          </a>
        </div>
            `;
      }
      $("#gallary").html(dataRow);
    } else {
      dataRow += `
      <div class="filtr-item col-ms-2" >
     <h4><center>No Data is available</center></h4>
    </div>
        `;
      $("#gallary").html(dataRow);
    }
  }
  function users() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "getusers");
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_dashboard/" + 0,
      processData: false,
      contentType: false,
      data: formData,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        rows = response.Message;
        $("#staffs").text(rows[0].staff);
        $("#members").text(rows[0].members);
        $("#books").text(rows[0].books);
      },
      error: function (response) {},
    });

    var dataRow = "";
    if (rows.length > 0) {
    } else {
    }
  }
});
