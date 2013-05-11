function init() {
Date.prototype.addHours = function(h) {
   this.setTime(this.getTime() + (h*60*60*1000));
   return this;
};


// DATA
var query_date = "2012-03-20T23:44";
var data = [
    {"transfers":3,"duration":"3:20","type":"juna","name":"yhteyden nimi","price":"12.40e","date":"2012-03-20T18:30","total":3},
    {"transfers":3,"duration":"3:20","type":"juna","name":"yhteyden nimi","price":"12.40e","date":"2012-03-20T19:21","total":4},
    {"transfers":3,"duration":"3:20","type":"bussi","name":"yhteyden nimi","price":"12.40e","date":"2012-03-20T22:00","total":2},
    {"transfers":3,"duration":"3:20","type":"bussi","name":"yhteyden nimi","price":"12.40e","date":"2012-03-20T23:00","total":1.5},
    {"transfers":3,"duration":"3:20","type":"auto","name":"yhteyden nimi","price":"12.40e","date":"2012-03-20T23:44","total":0.5},
    {"transfers":3,"duration":"3:20","type":"bussi","name":"yhteyden nimi","price":"12.40e","date":"2012-03-21T00:10","total":3},
    {"transfers":3,"duration":"3:20","type":"juna","name":"yhteyden nimi","price":"12.40e","date":"2012-03-21T02:30","total":2}];

for (var i=0; i<data.length; i++) {
    dt1 = new Date(data[i].date);
    dt2 = new Date(dt1.getTime()).addHours(data[i].total);
    data[i].dt1 = dt1;
    data[i].dt2 = dt2;
}


// ASETUKSET
var margin = {top: 40, right: 10, bottom: 40, left:10},
    width = 1000,
    barHeight = 40,
    barMargin = 5,
    height = margin.top + margin.bottom + data.length * (barHeight + barMargin);


// SKAALAUS
var x = d3.time.scale()
    .domain([d3.time.hour.offset(data[0].dt1, -1), d3.time.hour.offset(data[data.length - 1].dt2, 1)])
    .rangeRound([0, width - margin.left - margin.right]);

var y = d3.scale.linear()
    .domain([0, data.length])
    .range([height - margin.top - margin.bottom, 0]);


// AKSELIT
var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(d3.time.hours, 1)
    .tickFormat(d3.time.format("%H:%M"))
    .tickPadding(5);

var xAxisDays = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .ticks(d3.time.days, 1)
    .tickFormat(d3.time.format("%d.%m.%Y"))
    .tickPadding(20);

var xAxisTop = d3.svg.axis()
    .scale(x)
    .orient("top")
    .ticks(d3.time.hours, 1)
    .tickFormat(d3.time.format("%H:%M"))
    .tickPadding(5);


// CONTAINER
var svg = d3.select(".results").append("svg")
    .attr("class", "char")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");


// PYSTYVIIVAT
svg.append("line")
    .attr("x1", x(new Date(query_date)))
    .attr("x2", x(new Date(query_date)))
    .attr("y1", 0)
    .attr("y2", height - margin.top - margin.bottom)
    .attr("stroke-width", 1)
    .style("stroke-dasharray", "10, 5")
    .attr("stroke", "red");


// PALIKAT
var chart = svg.selectAll(".chart");
chart.data(data)
    .enter().append("rect")
    .attr("class", function(d) { return "bar " + d.type; })
    .attr("x", function (d) { return x(d.dt1); })
    .attr("y", function(d, i) { return y(i) - barHeight; })
    .attr("rx", "4")
    .attr("ry", "4")
    .attr("width", 0)
    .attr("data-content", function(d) { return d.name; })
    .attr("data-placement", "top")
    .attr("opacity", 0.9)
    .on("mouseover", function() {
        d3.select(this).transition().duration(300)
            .attr("opacity", 0.5);
    })
    .on("mouseout", function() {
        d3.select(this).transition().duration(300)
            .attr("opacity", 0.9);
    })
    .transition().duration(1400).delay(100)
    .attr("width", function(d) { return x(d.dt2) - x(d.dt1); })
    .attr("height", function(d) { return barHeight; });


// AKSELIEN LISÄYS
svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0, " + (height - margin.top - margin.bottom) + ")")
    .call(xAxis);

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0, " + 0 + ")")
    .call(xAxisTop);

svg.append("g")
    .attr("class", "x axis axis-days")
    .attr("transform", "translate(0, " + (height - margin.top - margin.bottom) + ")")
    .call(xAxisDays);
}

window.onload = function() {
    init();
};
