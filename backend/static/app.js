$('form input[type="file"]').change((event) => {
  let archives = event.target.files;

  if (archives.length === 0) {
    console.log("Sem imagem para mostrar.");
  } else {
    console.log(archives[0].type)
    if (archives[0].type == "image/jpeg") {
      $("img").remove();
      let image = $('<img class="img-responsive img-cover">');
      image.attr("src", window.URL.createObjectURL(archives[0]));
      $("figure").prepend(image);
    } else {
      alert("Formato não suportado.");
    }
  }
});
