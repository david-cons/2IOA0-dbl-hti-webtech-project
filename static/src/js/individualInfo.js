const individual = document.querySelector('#individualInfo')
const individual_loading = document.querySelector('#individual_loading')
const right = document.querySelector('.mainRow > .right')
const meta = document.querySelector('#meta')
const chordFrame = document.querySelector('#chordFrame')
const node_id_input = document.querySelector('.node_id')

let justAClick = false;

const SearchById = () => {
  const id = node_id_input.value
  if (id > 0) {
    makeIndividualInfoRequest(null, id)
  }
}
node_id_input.addEventListener("keyup", e => {
  if (e.keyCode === 13) {
    SearchById()
  }
})

const makeIndividualInfoRequest = (e, id = null) => {
  if (id === null) {
    const idElement = document.querySelector('.bk-tooltip .bk .bk .bk-tooltip-row-value span')
    if (idElement.offsetWidth === 0) {
      if (justAClick) {
        right.classList.add('hidden')
      }
      justAClick = false
      return
    }
    id = idElement.innerHTML
  }
  right.classList.remove('hidden')
  individual_loading.classList.remove('hidden')
  individual.classList.add('hidden')
  meta.classList.add('hidden')
  chordFrame.classList.add('hidden')
  const formData = new FormData()
  formData.append('person_id', id)
  makeGeneralFilters(formData)
  makeFormDataFromCsvInput(formData)
  const xhttp = new XMLHttpRequest();
  xhttp.addEventListener('load', event => {
    individual_loading.classList.add('hidden')
    individual.classList.remove('hidden')
    if (event.target.status !== 200) {
      individual.innerHTML = event.target.statusText
      return
    }
    node_id_input.value = ''
    node_id_input.blur()
    meta.classList.remove('hidden')
    chordFrame.classList.remove('hidden')
    const data = JSON.parse(event.target.response)
    showChord(data.chord)
    fillIndividualInfo(data)
  })
  xhttp.open("POST", "/individual-info", true);
  xhttp.send(formData);
}

const fillIndividualInfo = data => {
  document.querySelector('#meta .id').innerHTML = '#' + data.meta.person_id
  const email = data.meta.mail_address
  document.querySelector('#meta .email').innerHTML = email.substring(0, email.indexOf('@')).replace(/\./g, ' ')
  document.querySelector('#meta .job_title').innerHTML = data.meta.job_title
  const keys = Object.keys(data.all_time)
  let html = '<tr class="text-right"><td colspan="2"><strong>filtered data</strong></td><td>all data<td></tr>'
  for (let i = 0; i < keys.length; i++) {
    const key = keys[i]
    html += '<tr>'
    if (key.substring(0, 6) === 'array_') {
      html += emailArrayHtml(data.time_filtered[key])
      html += '</tr><tr>'
      html += emailArrayHtml(data.all_time[key])
    } else if (key.substring(0, 7) === 'hspace_') {
      html += '<td colspan="3" class="paddingBottom"></td>'
    } else {
      html += '<td>' + key.replace(/_/g, ' ') + '</td>'
      html += '<td class="text-right"><strong>' + Math.round(data.time_filtered[key]*100)/100 + '</strong></td>'
      html += '<td class="text-right">' + Math.round(data.all_time[key]*100)/100 + '</td>'
    }
    html += '</tr>'
  }
  individual.innerHTML = html.replace(/NaN/g, '')
}

const emailArrayHtml = data => {
  let html = ''
  let all_time
  try {
    all_time = JSON.parse(data).count
  } catch (e) {
    return '<td>no data</td>'
  }
  const all_time_keys = Object.keys(all_time)
  const all_time_values = Object.values(all_time)
  const singleOpeningDiv = '<div style="width: ' + 100/all_time_keys.length + '%">'
  const maxEmails = all_time_values.reduce((e, acc) => e > acc ? e : acc)
  html += '<td colspan="3" class="email_array ' + (all_time_keys.length < 10 ? 'borders' : '') + '">'
  for (let j = 0; j < all_time_keys.length; j++) {
    html += singleOpeningDiv
    html += '<div style="opacity: ' + all_time_values[j] / maxEmails + '"></div>'
    html += '<p>#' + all_time_keys[j] + ': ' + all_time_values[j] + ' email' + (all_time_values[j] > 1 ? 's' : '') + ' sent</p>'
    html += '</div>'
  }
  html += '</td>'
  return html
}

const showChord = data => {
  chordFrame.innerHTML = ''
  Bokeh.embed.embed_item(JSON.parse(data), 'chordFrame')
  // chordFrame.setAttribute('srcdoc', data)
  // chordFrame.style.height = chordFrame.contentWindow.document.documentElement.scrollHeight + 'px'
}

// root is the root of the full size graph
root.addEventListener('mousedown', e => {
  justAClick = true
})
root.addEventListener('mousemove', e => {
  justAClick = false
})
root.addEventListener('mouseup', makeIndividualInfoRequest)