const getData = () => {
  const formData = new FormData();
  const files = document.querySelector('#inputForm [name=csv_data]').files;
  formData.append('csv_data', files[0])

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', function (event) {
    const response = JSON.parse(event.target.response)
    const sizeSpan = document.querySelector('#sizeSpan')
    const sizeP = document.querySelector('#sizeP')
    sizeP.classList.remove('hidden')
    sizeSpan.innerHTML = response.size
  })

  xhttp.open("POST", "/base-data", true);
  xhttp.send(formData);
}