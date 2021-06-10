const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
const slider = document.querySelector('.doubleSlider')
const hands = slider.querySelectorAll('.hand')
const leftHand = slider.querySelector('.leftHand')
const rightHand = slider.querySelector('.rightHand')
const highlight = slider.querySelector('.highlight')
const minValue = slider.querySelector('.minValue')
const maxValue = slider.querySelector('.maxValue')

let currentHand = null

let dateRange

const initTimeSlider = (dateRangeInit) => {
  dateRange = generateDateRange(dateRangeInit)
  document.addEventListener('mousemove', handleMouseMove)
  resetInputs()
}

for (let i = 0; i < hands.length; i++) {
  hands[i].addEventListener('mousedown', function (e) {
    currentHand = e.target
  })
}
document.addEventListener('mouseup', function (e) {
  currentHand = null
})

function handleMouseMove(e) {
  if (currentHand) {
    let sliderWidth = slider.getBoundingClientRect().width
    let x0 = slider.getBoundingClientRect().left;
    let handX = e.clientX - x0 - 32
    handX = Math.max(-16, handX)
    handX = Math.min(sliderWidth -48, handX)
    currentHand.style.left = handX + 'px'
    
    let leftX = parseInt(leftHand.style.left)
    let rightX = parseInt(rightHand.style.left)
    newLeftX = Math.min(leftX, rightX) || leftX
    rightX = Math.max(leftX, rightX) || rightX || (sliderWidth - 48)
    leftX = newLeftX

    leftHand.style.left = leftX + 'px'
    rightHand.style.left = rightX + 'px'
    highlight.style.left = leftX + 16 + 'px'
    highlight.style.width = rightX - (leftX || -16) + 'px'

    if (leftX) {
      const date = dateRange[Math.floor((dateRange.length + 2) * (leftX + 16) / sliderWidth)]
      minValue.value = date.humanValue
      minValue.setAttribute('data-date', date.value+'-00')
    }
    if (rightX) {
      const date = dateRange[Math.ceil((dateRange.length + 2) * (rightX + 16) / sliderWidth)]
      maxValue.value = date.humanValue
      maxValue.setAttribute('data-date', date.value+'-32')
    }
  }
}

function generateDateRange(timeData) {
  let dates = []
  for (let year = timeData.startYear, month = timeData.startMonth;
      year < timeData.endYear || (year === timeData.endYear && month <= timeData.endMonth);
      month++) {
    dates.push({
      value: year + '-' + month,
      humanValue: months[month -1] + ' ' + year
    })
    if (month === 12) {
      month = 0
      year ++
    }
  }
  return dates
}

function resetInputs() {
  const startDate = dateRange[0]
  minValue.value = startDate.humanValue
  minValue.setAttribute('data-date', startDate.value + '-00')
  const endDate = dateRange[dateRange.length -1]
  maxValue.value = endDate.humanValue
  maxValue.setAttribute('data-date', endDate.value + '-32')
}

document.querySelector('.allTimeButton').addEventListener('click', function (e) {
  e.preventDefault()
  resetInputs()
  leftHand.style.left = ''
  rightHand.style.left = ''
  highlight.style.left = ''
  highlight.style.width = ''
})