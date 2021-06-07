const createData = path => new Promise((resolve, reject) => {
  let people = []
  let emails = []
  let jobs = []
  let sents = []

  // we read the json data at the specified path
  d3.json(path).then(data => {
    for (let i = 0; i < data.length; i++) {
      let from = data[i].fromId
      let to = data[i].toId
      let job = data[i].toJobtitle
      sents.push(data[i].sentiment)
      // push the email to the list
      emails.push({
        from_id: from,
        to_id: to,
        sentiment: data[i].sentiment
      })
      // check if sender is already in the list if people, else add them
      if (people.filter(e => e.id === from).length === 0) {
        people.push({
          id: from,
          job: job
        })
      }
      // check if receiver is already in the list if people, else add them
      if (people.filter(e => e.id === to).length === 0) {
        people.push({
          id: to,
          job: job
        })
      }
      // check if job is already in the list if jobs, else add it
      if (jobs.filter(e => e === job).length === 0) {
        jobs.push(job)
      }
    }
  }).then(() => {
    // return to the function in plot.js with and object containing people and emails
    resolve({
      people: people,
      emails: emails,
      jobs: jobs,
    })
  })
})