const giveColours = data => {
  const colourJumpSize = 360 / data.jobs.length
  for (let i = 0; i < data.people.length; i++) {
    const jobIdx = data.jobs.indexOf(data.people[i].job)
    data.people[i].colour = `hsl(${jobIdx*colourJumpSize}, 100%, 50%)`
  }
}