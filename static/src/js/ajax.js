const roodId = 'BaseDataPlot'
const root = document.querySelector('#'+roodId)
const errorP = document.querySelector('p.error')
const graph_loading = document.querySelector('#graph_loading')
const individual = document.querySelector('#individualInfo')
const individual_loading = document.querySelector('#individual_loading')
// const left = document.querySelector('.mainRow > .left')
const right = document.querySelector('.mainRow > .right')
const initialOverlay = document.querySelector('#initialOverlay')

const makeFormDataFromCsvInput = (formData) => {
  const files = document.querySelector('#inputForm [name=csv_data]').files;
  if (!files.length || (files[0].type !== 'text/csv' && files[0].type !== 'application/vnd.ms-excel')) {
    throw 'Please upload a csv file'
  }
  formData.append('csv_data', files[0])
}

const initialGraphCall = () => {
  errorP.classList.add('hidden')
  root.innerHTML = ''
  root.classList.remove('hidden')
  graph_loading.classList.remove('hidden')

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

  xhttp.addEventListener('load', function (event) {
    graph_loading.classList.add('hidden')

    if (event.target.status !== 200) {
      showFormError(event.target.statusText)
      return
    }

    response = JSON.parse(event.target.response)

    initialOverlay.classList.add('hidden')
    Bokeh.embed.embed_item(JSON.parse(response.graph), roodId)
      .then(resizePlot)
    
    initTimeSlider(response.parameters.timeSlider)
  })

  xhttp.open("POST", "/initial-full-size-graph", true);
  xhttp.send(formData);
}

const getFullSizeGraph = () => {
  errorP.classList.add('hidden')
  root.innerHTML = ''
  root.classList.remove('hidden')
  graph_loading.classList.remove('hidden')

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

  xhttp.addEventListener('load', function (event) {
    graph_loading.classList.add('hidden')

    if (event.target.status !== 200) {
      showFormError(event.target.statusText)
      return
    }

    initialOverlay.classList.add('hidden')
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
  root.scrollIntoView({behavior: 'smooth'})
}

function calculateGraphSize() {
  const maxHeight = window.innerHeight
  const maxWidth = window.innerWidth * 0.6
  return Math.floor(Math.min(maxHeight, maxWidth) - 50)
}

window.addEventListener('resize', () => { window.setTimeout(resizePlot, 1) })

function showFormError(text) {
  errorP.classList.remove('hidden')
  errorP.textContent = text;
}

root.addEventListener('mouseup', function (e) {
  right.classList.remove('hidden')
  individual_loading.classList.remove('hidden')
  individual.classList.add('hidden')
  const formData = new FormData()
  formData.append('person_id', document.querySelector('.bk-tooltip .bk .bk .bk-tooltip-row-value span').innerHTML)
  formData.append('start_date', document.querySelector('.minValue').getAttribute('data-date'))
  formData.append('end_date', document.querySelector('.maxValue').getAttribute('data-date'))
  makeFormDataFromCsvInput(formData)
  const xhttp = new XMLHttpRequest();
  xhttp.addEventListener('load', function (event) {
    individual_loading.classList.add('hidden')
    individual.classList.remove('hidden')
    fillIndividualInfo(JSON.parse(event.target.response))
  })
  xhttp.open("POST", "/individual-info", true);
  xhttp.send(formData);
})

function fillIndividualInfo(data) {
  document.querySelector('#meta .id').innerHTML = '#'+data.meta.person_id
  document.querySelector('#meta .email').innerHTML = data.meta.mail_address
  document.querySelector('#meta .job_title').innerHTML = data.meta.job_title
  const keys = Object.keys(data.all_time)
  let html = '<tr class="text-right"><td colspan="2"><strong>selected time</strong></td><td>all time<td></tr>'
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i]
    html += '<tr>'
    html += '<td>' + key.replace(/_/g, ' ') + '</td>'
    html += '<td class="text-right"><strong>' + Math.round(data.time_filtered[key]*100)/100 + '</strong></td>'
    html += '<td class="text-right">' + Math.round(data.all_time[key]*100)/100 + '</td>'
    html += '</tr>'
  }
  individual.innerHTML = html
}

// function getParamsFromCsv(text) {
//   var lines = text.split('\n');
//   let params = {
//     start_date: {
//       value: '5000-00-00',
//       function: function(val){val < this.value && (this.value = val)},
//       index: lines[0].indexOf('date'),
//     },
//     end_date: {
//       value: '0000-00-00',
//       function: function(val){val > this.value && (this.value = val)},
//       index: lines[0].indexOf('date')
//     }
//   }
//   const paramKeys = Object.keys(params)
//   for (var j = 1 /*skip line 1 */; j < lines.length; j++) {
//     if (lines[j] != "") {
//       var information = lines[j].split(',');
//       for (let k = 0; k < paramKeys.length; k++) {
//         let key = paramKeys[k]
//         let param = params[key]
//         let newVal = information[param.index]
//         param.function(newVal)
//       }
//     }
//   }
//   return params
// }