const errorP = document.querySelector('p.error')
const initialOverlay = document.querySelector('#initialOverlay')

const makeFormDataFromCsvInput = (formData) => {
  const files = document.querySelector('#inputForm [name=csv_data]').files;
  if (!files.length || (files[0].type !== 'text/csv' && files[0].type !== 'application/vnd.ms-excel')) {
    throw 'Please upload a csv file'
  }
  formData.append('csv_data', files[0])
}


const showFormError = text => {
  errorP.classList.remove('hidden')
  errorP.textContent = text;
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