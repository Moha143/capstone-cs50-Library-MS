$(document).ready(function () {
  const BookID = $("#BookID").attr("BookIDs");
  if (BookID != "" && BookID != undefined) {
    bookdetail(BookID);
  }
});

function bookdetail(id) {
  $.ajax({
    async: false,
    method: "GET",
    url: URLS + "Library/manage_book/" + id,
    headers: { "X-CSRFToken": csrftoken },
    async: false,
    success: function (response) {
      if (!response.isError) {
        $("#imgbook").attr("src", "/media/" + response.Message.image);
        $("#Title").text(response.Message.title);
        $("#Author").text(response.Message.authorname);
        $("#Category").text(response.Message.categoryname);
        $("#ISBN").text(response.Message.ISBN);
        $("#Coppy").text(response.Message.copy);
        $("#Available").text(response.Message.available);
        $("#Publisher").text(response.Message.publisher);
        $("#Publisher").text(response.Message.publisher);
        $("#Summary").text(response.Message.summary);
        $("#ID").text(response.Message.id);
      } else {
        swal(response.Message, {
          icon: "error",
        });
      }
    },
    error: function (response) {},
  });
}
