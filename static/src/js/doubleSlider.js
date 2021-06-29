const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
const slider = document.querySelector('.doubleSlider')
const handWrap = document.querySelector('.handWrap')
const hands = slider.querySelectorAll('.hand')
const leftHand = slider.querySelector('.leftHand')
const rightHand = slider.querySelector('.rightHand')
const leftCover = slider.querySelector('.cover.left')
const rightCover = slider.querySelector('.cover.right')
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
  hands[i].addEventListener('mousedown', e => {
    currentHand = e.target
  })
}
document.addEventListener('mouseup', e => {
  currentHand = null
})

const handleMouseMove = e => {
  if (currentHand) {
    let sliderWidth = slider.getBoundingClientRect().width - 48
    let x0 = slider.getBoundingClientRect().left;
    let handX = e.clientX - x0 - 32
    handX = Math.max(-16, handX)
    handX = Math.min(sliderWidth, handX)
    currentHand.style.left = handX + 'px'
    
    let leftX = parseInt(leftHand.style.left)
    let rightX = parseInt(rightHand.style.left)
    newLeftX = Math.min(leftX, rightX) || leftX
    rightX = Math.max(leftX, rightX) || rightX || sliderWidth
    leftX = newLeftX

    leftHand.style.left = leftX + 'px'
    rightHand.style.left = rightX + 'px'
    leftCover.style.width = leftX + 16 + 'px'
    rightCover.style.width = sliderWidth - rightX + 'px'

    if (leftX) {
      const date = dateRange[Math.floor((dateRange.length + 2) * (leftX + 16) / (sliderWidth + 48))]
      minValue.value = date.humanValue
      minValue.setAttribute('data-date', date.value+'-00')
    }
    if (rightX) {
      const date = dateRange[Math.ceil((dateRange.length + 2) * (rightX) / (sliderWidth + 48))]
      maxValue.value = date.humanValue
      maxValue.setAttribute('data-date', date.value+'-32')
    }
  }
}

const generateDateRange = timeData => {
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

const resetInputs = () => {
  const startDate = dateRange[0]
  minValue.value = startDate.humanValue
  minValue.setAttribute('data-date', startDate.value + '-00')
  const endDate = dateRange[dateRange.length -1]
  maxValue.value = endDate.humanValue
  maxValue.setAttribute('data-date', endDate.value + '-32')
}

document.querySelector('.allTimeButton').addEventListener('click', e => {
  e.preventDefault()
  resetInputs()
  leftHand.style.left = ''
  rightHand.style.left = ''
  leftCover.style.width = ''
  rightCover.style.width = ''
})

const showSentimentGradient = data => {
  let gradientText = 'linear-gradient(90deg'
  for (let i = 0; i < data.length; i++) {
    const hue = Math.round(data[i] * 120)
    const lightness = 100 - Math.round(Math.abs(data[i]-0.5) * 100)
    gradientText += ',hsl('+hue+',100%,'+lightness+'%)'
  }
  handWrap.style.background = gradientText + ')'
}