const jobTitleWrap = document.querySelector('.jobTitleWrap')

const initJobTitleFilter = jobTitles => {
  html = ''
  for (let i = 0; i < jobTitles.length; i++) {
    html += '<label for="jobTitle-' + i + '">'
    html += '<input name="jobTitle" type="checkbox" id="jobTitle-' + i + '" value="' + jobTitles[i] + '" checked></input>'
    html += '<p>' + jobTitles[i] + '</p>'
    html += '</label>'
  }
  jobTitleWrap.innerHTML = html
}

const getSelectedJobTitles = () => {
  const checkBoxes = jobTitleWrap.querySelectorAll('.jobTitleWrap input')
  let selected = []
  for (let i = 0; i < checkBoxes.length; i++) {
    if (checkBoxes[i].checked) {
      selected.push(checkBoxes[i].value)
    }
  }
  if (checkBoxes.length === selected.length) {
    return false
  }
  console.log(selected)
  return selected
}