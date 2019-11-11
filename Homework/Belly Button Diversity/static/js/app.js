function buildMetadata(sample) {

  // Use `d3.json` to fetch the metadata for a sample
  // Use d3 to select the panel with id of `#sample-metadata`
  var metadataURL = `/metadata/${sample}`;
  d3.json(metadataURL).then(function(data){
    console.log(data);
    var panel = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    panel.html("");

    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
    Object.entries(data).forEach(function([key,value]){
      panel.append("h6").text(`${key}:${value}`);
    })
  });
}

function buildCharts(sample) {
  // @TODO: Use `d3.json` to fetch the sample data for the plots
    // @TODO: Build a Bubble Chart using the sample data
    var plotdataURL = `/samples/${sample}`;
    d3.json(plotdataURL).then(function(data){
      console.log(data);
      var otu_ids = data.otu_ids;
      var otu_labels = data.otu_labels;
      var sample_values = data.sample_values;

      var bubble = {
        x: otu_ids,
        y: sample_values,
        text: otu_labels,
        mode: `markers`,
        marker: {
          size: sample_values,
          color: otu_ids
        }
      };
      var bubble_plot = [bubble];
      var bubble_layout = {
        title: "Belly Button Bacteria",
        xaxis: {title: "OTU ID"}
      };
      Plotly.newPlot("bubble", bubble_plot, bubble_layout);

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
    d3.json(plotdataURL).then(function(data){
      console.log(data);
      var pie_plot = [{
        "labels": otu_ids.slice(0,10),
        "values": sample_values.slice(0,10),
        "hovertext": otu_labels.slice(0,10),
        "type": "pie"
      }];
      var pie_layout = {
        title: "Top 10 Belly Button Bacteria Samples"
      };
    Plotly.newPlot("pie", pie_plot, pie_layout);
    });
  });
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
