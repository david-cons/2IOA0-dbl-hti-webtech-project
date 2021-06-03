const roodId = 'BaseDataPlot'
const root = document.querySelector('#'+roodId)
const errorP = document.querySelector('p.error')
const loading = document.querySelector('#loading')

const makeFormDataFromCsvInput = (formData) => {
  const files = document.querySelector('#inputForm [name=csv_data]').files;
  if (!files.length || files[0].type !== 'text/csv') {
    throw 'Please upload a csv file'
  }
  formData.append('csv_data', files[0])
}

const getFullSizeGraph = () => {
  errorP.classList.add('hidden')
  root.innerHTML = ''
  root.classList.remove('hidden')
  loading.classList.remove('hidden')

  let formData = new FormData()

  formData.append('start_date', document.querySelector('.minValue').getAttribute('data-date'))
  formData.append('end_date', document.querySelector('.maxValue').getAttribute('data-date'))

  try {
    makeFormDataFromCsvInput(formData)
  } catch (e) {
    showFormError(e)
    loading.classList.add('hidden')
    return
  }

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', function (event) {
    loading.classList.add('hidden')

    if (event.target.status !== 200) {
      showFormError(event.target.statusText)
      return
    }

    console.log(JSON.parse(JSON.parse(event.target.response)))

    Bokeh.embed.embed_item(JSON.parse(JSON.parse(event.target.response)), roodId)
      .then(resizePlot)
  })

  xhttp.open("POST", "/full-size-graph", true);
  xhttp.send(formData);
}

const getChordDiagram = () => {
  const formData = new FormData()
  
  makeFormDataFromCsvInput(formData)

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', function (event) {
    console.log(event.target.response)
  })

  xhttp.open("POST", "/chord-diagram", true);
  xhttp.send(formData);
}

const resizePlot = () => {
  // const maxHeight = window.innerHeight
  // const maxWidth = window.innerWidth
  // const size = Math.min(maxHeight, maxWidth) - 50
  // const wrap = document.querySelector('.bk-root > .bk')
  // //wrap.style.width = size + 'px'
  // //wrap.style.height = size + 'px'
  // wrap.style.transform = 'scale('+ (size / 950) +')'
  root.scrollIntoView({behavior: 'smooth'})
}

window.addEventListener('resize', () => { window.setTimeout(resizePlot, 1) })

function showFormError(text) {
  errorP.classList.remove('hidden')
  errorP.textContent = text;
}

root.addEventListener('mouseup', function (e) {
  const formData = new FormData()
  formData.append('node_id', document.querySelector('.bk-tooltip .bk .bk .bk-tooltip-row-value span').innerHTML)
  makeFormDataFromCsvInput(formData)

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', function (event) {
    console.log(event.target.response)
  })

  xhttp.open("POST", "/individual-info", true);
  xhttp.send(formData);
})