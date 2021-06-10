const individual = document.querySelector('#individualInfo')
const individual_loading = document.querySelector('#individual_loading')
const right = document.querySelector('.mainRow > .right')

// root is the root of the full size graph
root.addEventListener('mouseup', e => {
  right.classList.remove('hidden')
  individual_loading.classList.remove('hidden')
  individual.classList.add('hidden')
  const formData = new FormData()
  formData.append('person_id', document.querySelector('.bk-tooltip .bk .bk .bk-tooltip-row-value span').innerHTML)
  formData.append('start_date', document.querySelector('.minValue').getAttribute('data-date'))
  formData.append('end_date', document.querySelector('.maxValue').getAttribute('data-date'))
  makeFormDataFromCsvInput(formData)
  const xhttp = new XMLHttpRequest();
  xhttp.addEventListener('load', event => {
    individual_loading.classList.add('hidden')
    individual.classList.remove('hidden')
    fillIndividualInfo(JSON.parse(event.target.response))
  })
  xhttp.open("POST", "/individual-info", true);
  xhttp.send(formData);
})

const fillIndividualInfo = data => {
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