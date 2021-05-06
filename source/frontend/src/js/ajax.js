const getData = () => {
  const formData = new FormData(document.querySelector('#inputForm'));

  const xhttp = new XMLHttpRequest();

  xhttp.open("POST", "/", true);
  xhttp.send(formData);
}