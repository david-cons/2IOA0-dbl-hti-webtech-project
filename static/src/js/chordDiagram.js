const getChordDiagram = () => {
  const formData = new FormData()
  
  makeFormDataFromCsvInput(formData)

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', event => {
    console.log(event.target.response)
  })

  xhttp.open("POST", "/chord-diagram", true);
  xhttp.send(formData);
}