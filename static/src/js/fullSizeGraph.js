const rootId = 'BaseDataPlot'
const root = document.querySelector('#'+rootId)
const graph_loading = document.querySelector('#graph_loading')

const prepareGraphCall = () => {
  errorP.classList.add('hidden')
  root.innerHTML = ''
  root.classList.remove('hidden')
  graph_loading.classList.remove('hidden')
}

const initialGraphCall = () => {
  prepareGraphCall()

  let formData = new FormData()
  formData.append('graph_size', calculateGraphSize())

  try {
    makeFormDataFromCsvInput(formData)
  } catch (e) {
    showFormError(e)
    graph_loading.classList.add('hidden')
    return
  }

  const xhttp = new XMLHttpRequest();
  xhttp.addEventListener('load', handleInitialGraphCall)
  xhttp.open("POST", "/initial-full-size-graph", true);
  xhttp.send(formData);
  initialOverlay.classList.add('hidden')
}

const getFullSizeGraph = () => {
  prepareGraphCall()

  let formData = new FormData()

  formData.append('start_date', document.querySelector('.minValue').getAttribute('data-date'))
  formData.append('end_date', document.querySelector('.maxValue').getAttribute('data-date'))
  formData.append('graph_size', calculateGraphSize())

  try {
    makeFormDataFromCsvInput(formData)
  } catch (e) {
    showFormError(e)
    graph_loading.classList.add('hidden')
    return
  }

  const xhttp = new XMLHttpRequest();

  xhttp.addEventListener('load', handleGraphCall)

  xhttp.open("POST", "/full-size-graph", true);
  xhttp.send(formData);
}

const handleInitialGraphCall = event => {
  graph_loading.classList.add('hidden')

  if (event.target.status !== 200) {
    showFormError(event.target.statusText)
    return
  }

  response = JSON.parse(event.target.response)

  Bokeh.embed.embed_item(JSON.parse(response.graph), rootId)
    .then(resizePlot)
  
  initTimeSlider(response.parameters.timeSlider)
}

const handleGraphCall = event => {
  graph_loading.classList.add('hidden')

  if (event.target.status !== 200) {
    showFormError(event.target.statusText)
    return
  }

  initialOverlay.classList.add('hidden')
  Bokeh.embed.embed_item(JSON.parse(JSON.parse(event.target.response)), rootId)
    .then(resizePlot)
}

const resizePlot = () => {
  root.scrollIntoView({behavior: 'smooth'})
}

const calculateGraphSize = () => {
  const maxHeight = window.innerHeight
  const maxWidth = window.innerWidth * 0.6
  return Math.floor(Math.min(maxHeight, maxWidth) - 50)
}

window.addEventListener('resize', () => { window.setTimeout(resizePlot, 1) })