const sentimentBoxes = document.querySelectorAll('.sentimentWrap input')

const getSentimentValue = () => {
  let selected = []
  for (let i = 0; i < sentimentBoxes.length; i++) {
    if (sentimentBoxes[i].checked) {
      selected.push(sentimentBoxes[i].value)
    }
  }
  if (selected.length === 0) {
    for (let i = 0; i < sentimentBoxes.length; i++) {
      sentimentBoxes[i].checked = true
    }
  }
  if (selected.length === sentimentBoxes.length) {
    return []
  }
  return selected
}