// UTILS
Date.prototype.addHours = function (h) {
    this.setTime(this.getTime() + (h * 60 * 60 * 1000));
    return this;
};

Date.prototype.addMinutes = function (m) {
    this.setTime(this.getTime() + (m * 60 * 1000));
    return this;
};

// DATA
var query_date = "2012-03-20T23:44";
var data = [
    {"transfers":1,"duration":"3:20","type":"juna","name":"InterCity","price":16.70,"date":"2012-03-20T18:30","total":3},
    {"transfers":3,"duration":"3:20","type":"juna","name":"Pendolino","price":52.40,"date":"2012-03-20T19:21","total":4},
    {"transfers":0,"duration":"3:20","type":"bussi","name":"Pikavuoro","price":112.40,"date":"2012-03-20T22:00","total":2},
    {"transfers":4,"duration":"3:20","type":"bussi","name":"Perus","price":122.40,"date":"2012-03-20T23:00","total":1.5},
    {"transfers":3,"duration":"3:20","type":"auto","name":"Auto","price":11.00,"date":"2012-03-20T23:44","total":0.5},
    {"transfers":2,"duration":"3:20","type":"bussi","name":"Pikavuoro","price":2.40,"date":"2012-03-21T00:10","total":3},
    {"transfers":3,"duration":"3:20","type":"juna","name":"JunaBussi","price":36.44,"date":"2012-03-21T02:30","total":2}];

for (var i=0; i<data.length; i++) {
    dt1 = new Date(data[i].date);
    dt2 = new Date(dt1.getTime()).addHours(data[i].total);
    data[i].dt1 = dt1;
    data[i].dt2 = dt2;
}


// ASETUKSET
var margin = {top: 40, right: 10, bottom: 40, left:10},
    width = 1000,
    barHeight = 60,
    barMargin = 5,
    height = d3.max([margin.top + margin.bottom + data.length * (barHeight + barMargin), 400]);


// SKAALAUS
var firstDt = d3.min(data, function(d) { return d.dt1; }),
    lastDt = d3.max(data, function(d) { return d.dt2; });

var x = d3.time.scale()
    .domain([d3.time.hour.offset(firstDt, -1), d3.time.hour.offset(lastDt, 1)])
    .rangeRound([0, width - margin.left - margin.right]);

var y = d3.scale.linear()
    .domain([0, data.length])
    .range([0, height - margin.top - margin.bottom]);


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

var minDate = x.domain()[0],
    maxDate = x.domain()[1],
    lineY1 = 0,
    lineY2 = height - margin.top - margin.bottom;

minDate.addMinutes(60 - minDate.getMinutes());
maxDate.setMinutes(0);
while (minDate <= maxDate) {
    var lineX = x(minDate);
    svg.append("line")
        .attr("x1", lineX)
        .attr("x2", lineX)
        .attr("y1", lineY1)
        .attr("y2", lineY2)
        .attr("stroke-width", 0.8)
        .style("stroke-dasharray", "5, 5")
        .attr("stroke", "gray");
    minDate.addHours(1);
}


// PALIKAT
var g = svg.selectAll("g")
    .data(data).enter().append("g")
    .attr("class", "bar-g");

var rectEnter = g.append("rect")
    .attr("class", function(d) { return "bar " + d.type; })
    .attr("x", function (d) { return x(d.dt1); })
    .attr("y", function(d, i) { return y(i); })
    .attr("rx", "4")
    .attr("ry", "4")
    .attr("width", 0)
    .attr("height", function(d) { return barHeight; })
    .attr("data-placement", "top")
    .attr("opacity", 0.9)
    .attr("pointer-events", "none");

rectEnter.transition().duration(1400).delay(100)
    .attr("width", function(d) { return x(d.dt2) - x(d.dt1); })
    .each("end", function() {
        d3.select(this)
            .attr("pointer-events", "null");
        });

svg.selectAll(".bar")
    .on("mouseover", function() {
        d3.select(this).transition().duration(300)
            .attr("opacity", 0.5);
    })
    .on("mouseout", function() {
        d3.select(this).transition().duration(300)
            .attr("opacity", 0.9);
    });


// TEKSTIT
function generateContent(d) {
    var dep = d.dt1.toTimeString().substr(0, 5),
        arr = d.dt2.toTimeString().substr(0, 5);
    return "<div class='content top'>" + d.name + "</div>" +
    "<div class='content middle'>" + dep + " - " + arr + "</div>" +
    "<div class='content bottom'>Vaihtoja: <strong>" + d.transfers + "</strong></div>";
}

g.append("foreignObject")
    .attr("x", function (d) { return x(d.dt1); })
    .attr("y", function(d, i) { return y(i); })
    .attr("width", function(d) { return width - x(d.dt1); })
    .attr("height", function(d) { return barHeight; })
    .attr("pointer-events", "none")
    .append("xhtml:body")
        .attr("class", "content-body")
    // .append("xhtml:div")
    //     .attr("class", "content")
        .html(function(d) { return generateContent(d); });


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


// SORT BUTTONS
function getSortFunction(param) {
    return function(a, b) { return a[param] - b[param]; };
}

var transition = svg.transition().duration(1750).ease("elastic"),
    delay = function(d, i) { return i * 50; };

function sortByDt1() {
    sortBars(getSortFunction("dt1"));
}

function sortByDt2() {
    sortBars(getSortFunction("dt2"));
}

function sortByDuration() {
    sortBars(getSortFunction("total"));
}

function sortByPrice() {
    sortBars(getSortFunction("price"));
}

function sortByTransfers() {
    sortBars(getSortFunction("transfers"));
}

function sortBars(sort_func) {
    svg.selectAll(".bar-g .bar")
        .sort(sort_func)
        .transition(transition)
        .delay(delay)
        .attr("y", function(d, i) { return y(i); });

    svg.selectAll(".bar-g foreignObject")
        .sort(sort_func)
        .transition(transition)
        .delay(delay)
        .attr("y", function(d, i) { return y(i); });
}
