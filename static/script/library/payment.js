$(document).ready(function () {
  Member();

  //Save fine
  $("#save").on("click", function () {
    const ID = $("#ID").val();
    const fines = $("#fines").val();
    const Member = $("#Member").val();
    const remaining = $("#remaining").val();
    const borrow = $("#borrow").val();
    const totalamount = $("#tamount").val();
    if (Member == "" || Member == null || Member == undefined) {
      toastr.error("error Please Enter Member name");
    } else if (borrow == "" || borrow == null || borrow == undefined) {
      toastr.error("error Please Select Book ");
    } else if (fines == "") {
      toastr.error("error Please Enter amount of fine");
    } else {
      let formData = new FormData();
      formData.append("fines", fines);
      formData.append("borrow", borrow);
      if (parseFloat(fines) > parseFloat(remaining)) {
        toastr.error(
          "error amount of fine must be less than  or equal total remaining"
        );
      } else {
        $.ajax({
          method: "POST",
          url: URLS + "Library/manage_fine/" + ID,
          headers: { "X-CSRFToken": csrftoken },
          processData: false,
          contentType: false,
          data: formData,
          async: true,
          success: function (response) {
            if (!response.isError) {
              swal({
                title: "GOOD !!!!",
                text: response.Message,
                icon: "success",
                buttons: true,
                dangerMode: false,
              }).then((ok) => {
                if (ok) {
                  window.location.reload();
                } else {
                  window.location.reload();
                }
              });
            } else {
              toastr.error(response.Message);
            }
          },
          error: function (response) {},
        });
      }
    }
  });

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
    } else {
      $("#Member").attr("disabled", true);
      swal("Sorry: member does not exists", {
        icon: "error",
      });
    }
  }
  $("#Member").on("change", function () {
    $("#tamount").val("");
    $("#tpaid").val("");
    $("#end").val("");
    $("#start").val("");
    $("#remaining").val("");
    $("#ID").val("");
    const member = $(this).val();
    if (member != "") {
      Book();
    }
  });
  $("#borrow").on("change", function () {
    const borrow = $(this).val();
    if (borrow != "") {
      finedetail();
    }
  });
  function Book() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "memberbook");
    formData.append("Member", $("#Member").val());
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_fine/" + 0,
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
      $("#borrow").attr("disabled", false);
      dataRow = `<option value=''>Select Book</option>`;
      for (var i = 0; i < rows.length; i++) {
        dataRow +=
          `
          <option value='` +
          rows[i].id +
          `'>` +
          rows[i].book +
          `</option>
          `;
      }
      $("#borrow").html(dataRow);
    } else {
      $("#borrow").attr("disabled", true);
      swal("Sorry This member does not have fine", {
        icon: "error",
      });
    }
  }
  function finedetail() {
    var rows = "";
    let formData = new FormData();
    formData.append("type", "finedetails");
    formData.append("Member", $("#Member").val());
    formData.append("borrow", $("#borrow").val());
    $.ajax({
      method: "POST",
      url: URLS + "Library/manage_fine/" + 0,
      processData: false,
      contentType: false,
      data: formData,
      headers: { "X-CSRFToken": csrftoken },
      async: false,
      success: function (response) {
        if (!response.isError) {
          rows = response.Message[0];
          $("#tamount").val(rows.amount);
          $("#tpaid").val(rows.paid);
          $("#end").val(rows.end);
          $("#start").val(rows.start);
          $("#remaining").val(rows.remaining);
          $("#ID").val(rows.id);
        } else {
          $("#tamount").val("");
          $("#tpaid").val("");
          $("#end").val("");
          $("#start").val("");
          $("#remaining").val("");
          $("#ID").val("");
        }
      },
      error: function (response) {},
    });
  }
});
