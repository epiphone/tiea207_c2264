// GLOBAALIT
var svg, y, dt1Btn, dt2Btn, durationBtn, transfersBtn, priceBtn;


// UTILS
Date.prototype.addHours = function (h) {
    this.setTime(this.getTime() + (h * 60 * 60 * 1000));
    return this;
};

Date.prototype.addMinutes = function (m) {
    this.setTime(this.getTime() + (m * 60 * 1000));
    return this;
};

function getSortFunction(param) {
    return function(a, b) { return a[param] - b[param]; };
}

function init(data, query_date) {
// DATA
for (var i=0; i<data.length; i++) {
    dt1 = new Date(data[i].js_lahtoaika);
    dt2 = new Date(dt1.getTime()).addHours(data[i].tunnit);
    data[i].dt1 = dt1;
    data[i].dt2 = dt2;
}
data = data.sort(getSortFunction("dt1"));


// SORT-BUTTONIT
var btns = $(".results-header .btn-group button");
dt1Btn = btns[0];
dt2Btn = btns[1];
durationBtn = btns[2];
priceBtn = btns[3];
transfersBtn = btns[4];


// ASETUKSET
var margin = {top: 40, right: 10, bottom: 40, left:10},
    width = ($(".results").width() - 20) || 850,
    barHeight = 60,
    barMargin = 5,
    height = d3.max([margin.top + margin.bottom + data.length * (barHeight + barMargin), 400]);


// SKAALAUS
var firstDt = d3.min(data, function(d) { return d.dt1; }),
    lastDt = d3.max(data, function(d) { return d.dt2; });

var x = d3.time.scale()
    .domain([d3.time.minute.offset(firstDt, -30), d3.time.hour.offset(lastDt, 2)])
    .rangeRound([0, width - margin.left - margin.right]);

y = d3.scale.linear()
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
svg = d3.select(".results").append("svg")
    .attr("class", "chart")
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
    .attr("class", function(d) { return "bar " + d.luokka; })
    .attr("x", function (d) { return x(d.dt1); })
    .attr("y", function(d, i) { return y(i); })
    .attr("rx", "4")
    .attr("ry", "4")
    .attr("data-href", function(d) { return d.row_id; })
    .attr("width", 0)
    .attr("height", barHeight)
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
        d3.select(this).transition().duration(200)
            .attr("opacity", 0.5);
    })
    .on("mouseout", function() {
        d3.select(this).transition().duration(200)
            .attr("opacity", 0.9);
    });


// TEKSTIT
function generateContent(d) {
    var content = "<div class='content top'><span class='label'>" + d.lahtoaika +
    " - " + d.saapumisaika + " <strong>" + d.hinta+ "€</strong></span></div>" +
    "<div class='content middle'>" + d.tyyppi + "</div>";
    if (d.luokka != "auto") {
        content += "<div class='content bottom'>Vaihtoja: <strong>" + d.vaihdot_lkm +
        "</strong>";
    } else {
        content += "<div class='content bottom'>Pituus: " + d.pituus +
        "km</div>";
    }
    return content;
}

g.append("foreignObject")
    .attr("class", "bar-content")
    .attr("x", function (d) { return x(d.dt1); })
    .attr("y", function(d, i) { return y(i); })
    .attr("width", function(d) { return width - x(d.dt1); })
    .attr("height", function(d) { return barHeight; })
    .attr("pointer-events", "none")
    .append("xhtml:body")
        .attr("class", "content-body")
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
}


// SORT BUTTONS
function sortByDt1() {
    sortBars(getSortFunction("dt1"), dt1Btn);
}

function sortByDt2() {
    sortBars(getSortFunction("dt2"), dt2Btn);
}

function sortByDuration() {
    sortBars(getSortFunction("tunnit"), durationBtn);
}

function sortByPrice() {
    sortBars(getSortFunction("hinta"), priceBtn);
}

function sortByTransfers(e) {
    sortBars(getSortFunction("vaihdot_lkm"), transfersBtn);
}

function sortBars(sort_func, btn) {
    var transition = svg.transition().duration(1750).ease("elastic"),
        delay = function(d, i) { return i * 50; };

    svg.selectAll(".bar-g .bar")
        .sort(sort_func)
        .attr("pointer-events", "none")
        .transition(transition)
        .delay(delay)
        .attr("y", function(d, i) { return y(i); })
        .each("end", function() {
            d3.select(this).attr("pointer-events", "null");
        });

    svg.selectAll(".bar-g .bar-content")
    .sort(sort_func)
        .transition(transition)
        .delay(delay)
        .attr("y", function(d, i) { return y(i); });

    $(".btn-group .disabled").removeClass("disabled");
    $(btn).addClass("disabled");
}
