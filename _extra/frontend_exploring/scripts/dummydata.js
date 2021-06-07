const createDummyData = () => {
  let people = []
  let emails = []

  const num_of_people = 100
  const num_of_clusters = 5

  const num_of_emails = 5000;
  const cluster_chance = 0.95;

  for (let i = 0; i < num_of_people; i++) {
    people.push({
      id: i,
      group_id: Math.floor(Math.random() * num_of_clusters)
    })
  }

  for (let i = 0; i < num_of_emails; i++) {
    let from = people[Math.floor(Math.random() * people.length)]
    let optionsTo
    if (Math.random() < cluster_chance) {
      optionsTo = people.filter(p => p.id !== from.id && p.group_id === from.group_id)
    } else {
      optionsTo = people.filter(p => p.id !== from.id)
    }
    let to = optionsTo[Math.floor(Math.random() * optionsTo.length)]
    emails.push({
      from_id: from.id,
      to_id: to.id
    })
  }

  return {
    people: people,
    emails: emails
  }
}