
// standard d3 inits
const margin = { top: 10, right: 5, bottom: 10, left: 5 }
const width   = Math.min(1400, window.innerWidth)-margin.left-margin.right
const height = Math.min(900, window.innerHeight) - margin.top - margin.bottom
  
// creating an svg element in the webpage (that is basically a blank drawing)
const svg = d3.select("#container").append("svg")
  .attr("width",width)
  .attr("height", height)
  .append("g")
    .attr("transform","translate(" + margin.left + "," + margin.top + ")")

// variables need a global scope for the tick function
let link, node

// we call a function createData in the file at scripts/createData.js
createData('http://127.0.0.1:5500/data.json').then(data => {
  giveColours(data);
  // we transform the seperate emails to a list of links, drastically reducing
  // their number and giving a more meaningfull representation later.
  let links = []
  for (let i = 0; i < data.emails.length; i++) {
    let existingLink = links.filter(l => (
      (l.source === data.emails[i].from_id && l.target === data.emails[i].to_id) ||
      (l.target === data.emails[i].from_id && l.source === data.emails[i].to_id)
    ))
    switch (existingLink.length) {
      // the link is not yet in the list
      case 0:
        links.push({
          source: data.emails[i].from_id,
          target: data.emails[i].to_id,
          numberOfEmails: 1,
          totalSentiment: data.emails[i].sentiment
        })
        break
      // the link is in the list
      case 1:
        existingLink[0].numberOfEmails++
        existingLink[0].totalSentiment += data.emails[i].sentiment
        break
      // the link is duplicate in the list
      case 2:
        console.error("DUPLICATE LINKS DETECTED!")
    }
  }
  
  // creating svg drawings of all the lines in the plot
  link = svg
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
      .style("stroke", d => `hsla(${60+60*d.totalSentiment/d.numberOfEmails},100%,25%,0.05)`) // mean sentiment of correspondence
      .style("stroke-width", d => Math.sqrt(d.numberOfEmails) + 'px') // line width is sqrt(number of emails)
      
  // creating svg drawings of all the nodes
  node = svg
    .selectAll("circle")
    .data(data.people)
    .enter()
    .append("circle")
      .attr("r", 4)
      .style("fill", d => d.colour) // colour as calculated in giveColours
      
  // simulation code, straight from the docs ;)
  let simulation = d3.forceSimulation(data.people)                 // Force algorithm is applied to data.nodes
    .force("link", d3.forceLink()                               // This force provides links between nodes
      .id(function(d) { return d.id; })                     // This provide  the id of a node
      .links(links)                            // and this the list of links
    )
      .force("charge", d3.forceManyBody().strength(-80))         // This adds repulsion between nodes. Play with the -400 for the repulsion strength
      .force("center", d3.forceCenter(width / 2, height / 2))     // This force attracts nodes to the center of the svg area
      .on("end", ticked)
})

// this function will be more usefull when things move, now it is just called in the beginning.
function ticked() {
  link
    .attr("x1", function (d) { return d.source.x; })
    .attr("y1", function(d) { return d.source.y; })
    .attr("x2", function(d) { return d.target.x; })
    .attr("y2", function(d) { return d.target.y; });

  node
    .attr("cx", function (d) { return d.x-2; })
    .attr("cy", function(d) { return d.y-2; });
}

