const roodId = 'BaseDataPlot'
const root = document.querySelector('#'+roodId)

const makeFormDataFromCsvInput = () => {
  const formData = new FormData();
  const files = document.querySelector('#inputForm [name=csv_data]').files;
  formData.append('csv_data', files[0])
  return formData
}

const getFullSizeGraph = () => {
  const formData = makeFormDataFromCsvInput()

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', function (event) {
    root.innerHTML = ''
    root.classList.remove('hidden')

    Bokeh.embed.embed_item(JSON.parse(JSON.parse(event.target.response)), roodId)
      .then(resizePlot)
  })

  xhttp.open("POST", "/full-size-graph", true);
  xhttp.send(formData);
}

const getChordDiagram = () => {
  const formData = makeFormDataFromCsvInput()

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', function (event) {
    console.log(event.target.response)
  })

  xhttp.open("POST", "/chord-diagram", true);
  xhttp.send(formData);
}

const resizePlot = () => {
  const maxHeight = window.innerHeight - root.getBoundingClientRect().top
  const maxWidth = window.innerWidth
  const size = Math.min(maxHeight, maxWidth) - 50
  const wrap = document.querySelector('.bk-root > .bk')
  wrap.style.width = size + 'px'
  wrap.style.height = size + 'px'
  console.log(maxHeight)
}

window.addEventListener('resize', ()=>{window.setTimeout(resizePlot, 1)})