/**
 * Created by Michael on 4/2/14
 */

var margin = {
    top: 50,
    right: 50,
    bottom: 50,
    left: 50
};

var width = 1060 - margin.left - margin.right;
var height = 800 - margin.bottom - margin.top;
var centered;
var active = d3.select(null);

var bbVis = {
    x: 100,
    y: 10,
    w: width - 100,
    h: 300
};

var detailVis = d3.select("#detailVis").append("svg").attr({
    width:450,
    height:300
})

var detailVis2 = d3.select("#detailVis2").append("svg").attr({
    width:450,
    height:300
})

var bbDetailVis = {
    w: 350,
    h: 200
}

var canvas = d3.select("#vis").append("svg").attr({
    width: width + margin.left + margin.right,
    height: height + margin.top + margin.bottom
    })

var svg = canvas.append("g").attr({
        transform: "translate(" + margin.left + "," + margin.top + ")"
    })
    .call(d3.behavior.zoom().scaleExtent([1, 8]).on("zoom", zoom))
    .append("g");

svg.append("rect")
    .attr("class", "background")
    .attr("width", width)
    .attr("height", height)
    .on("click", clicked);

var g = svg.append("g");

var latitude = 42.360024;
var longitude = -71.060168;

var projection = d3.geo.albers().translate([width / 2, height / 2]);//.precision(.1);
var path = d3.geo.path().projection(projection);
var screencoord = projection([longitude, latitude]);

var dataSet = {};

function loadStations() {
    d3.csv("../data/Site_table_dummy3.csv",function(error,data){

    // write a time parser, and sort the data 
    var timeParser = d3.time.format("%b%b");
    var monthParser = d3.time.format("%b");

    data.forEach(function(d) {

        d.AirTemp = {};
        d.BestSurfing = {};
        d.TypicalSwell = {};
        d.WaterTemp = {};

        var parsed_air;
        var parsed_water;

        for (property in d){
          var value = d[property];
          if (property.slice(0, 7) == "AirTemp" && typeof value != 'object'){
            parsed_air = monthParser(timeParser.parse(property.slice(8)));
            if (typeof d.AirTemp[parsed_air] === "undefined") {
                d.AirTemp[parsed_air] = 0;
            }
            d.AirTemp[parsed_air] += +value;
          }
          else if (property.slice(0, 11) == "BestSurfing" && typeof value != 'object'){
            if (typeof d.BestSurfing[property.slice(12)] === "undefined") {
                d.BestSurfing[property.slice(12)] = 0;
            }
            d.BestSurfing[property.slice(12)] += +value;
          }
          else if (property.slice(0, 12) == "TypicalSwell" && typeof value != 'object'){
            if (typeof d.TypicalSwell[property.slice(13)] === "undefined") {
                d.TypicalSwell[property.slice(13)] = 0;
            }
            d.TypicalSwell[property.slice(13)] += +value;
          }
          else if (property.slice(0, 9) == "WaterTemp" && typeof value != 'object'){
            parsed_water = monthParser(timeParser.parse(property.slice(10)));
            if (typeof d.WaterTemp[parsed_water] === "undefined") {
                d.WaterTemp[parsed_water] = 0;
            }
            d.WaterTemp[parsed_water] += +value;
          }
        }
    })

    console.log(data);
    createDetailVis(data[0], data[0].Spot);


    // var div = d3.select("body").append("div")   
    //     .attr("class", "tooltip")               
    //     .style("opacity", 0);

    // var circle = svg.selectAll("circle")
    //    .data(completeDataSet)
    //    .enter()
    //    .append("circle")
    //    .attr("cx", function(d) {
    //         if (projection([d[Object.keys(d)].lon, d[Object.keys(d)].lat]) != null) {
    //             return projection([d[Object.keys(d)].lon, d[Object.keys(d)].lat])[0];
    //         }
    //    })
    //    .attr("cy", function(d) {
    //         if (projection([d[Object.keys(d)].lon, d[Object.keys(d)].lat]) != null) {
    //             return projection([d[Object.keys(d)].lon, d[Object.keys(d)].lat])[1];
    //         }
    //    })
    //    .attr("r", function(d) {
    //         if (d[Object.keys(d)].sum > 0) {
    //            return Math.sqrt(parseInt(d[Object.keys(d)].sum) * 0.000001);
    //         }
    //         else {
    //            return 2;
    //         }
    //    })
    //    .style("fill", function(d) {
    //         if (d[Object.keys(d)].sum == 0) {
    //             return "black";
    //         }
    //         else {
    //             return "yellow";
    //         }
    //    })
    //    .style("opacity", 0.75)
    //    .on("click", function(d) {
    //       createDetailVis(d[Object.keys(d)].hourly, d[Object.keys(d)].station);   
    //    })
    //    .on("mouseover", function(d){

    //         d3.select(this)
    //             .style("fill", "orange")

    //         div.transition()        
    //             .duration(200)      
    //             .style("opacity", .9);      
    //         div .html(d[Object.keys(d)].station + "<br/>"  + d[Object.keys(d)].sum)  
    //             .style("left", (d3.event.pageX) + "px")     
    //             .style("top", (d3.event.pageY - 28) + "px");
 
    //         })      
    //    .on("mouseout", function(d){
    //         d3.select(this)  
    //            .style("fill", function(d) {
    //                 if (d[Object.keys(d)].sum == 0) {
    //                     return "black";
    //                 }
    //                 else {
    //                     return "yellow";
    //                 }
    //         })

    //         div.transition()        
    //             .duration(500)      
    //             .style("opacity", 0); 
    //     });
    })
}
loadStations();

var createDetailVis = function(data, name){

    updateDetailVis(data, name);

        var airData = [];
        var waterData = [];

        parse_date = d3.time.format('%b')

        var this_data = data.AirTemp;
        var this_data2 = data.WaterTemp;

        // make new array of objects to contain the hourly object data
        for (key in this_data) {
            d = {};
            d.date = parse_date.parse(key);
            d.value = this_data[key];
            airData.push(d);
        }

        airData.sort(function(a,b){
            return d3.ascending(a.date, b.date);
        });

        for (key in this_data2) {
            d = {};
            d.date = parse_date.parse(key);
            d.value = this_data2[key];
            waterData.push(d);
        }

        waterData.sort(function(a,b){
            return d3.ascending(a.date, b.date);
        });

        console.log(airData);
        console.log(waterData);

        var x = d3.scale.ordinal()
            .rangeRoundBands([0, bbDetailVis.w], .1);
        var x2 = x;

        var y = d3.scale.linear()
            .range([bbDetailVis.h, 0]);
        var y2 = y;

        x.domain(airData.map(function(d) { 
                return +d.date.getMonth(); 
        }));
        x2.domain(waterData.map(function(d) { 
                return +d.date.getMonth(); 
        }));

        y.domain([0, d3.max(airData, function(d) { 
                return d.value; 
        })]);
        y2.domain([0, d3.max(waterData, function(d) { 
                return d.value; 
        })]);

        var xAxis = d3.svg.axis()
            .scale(x)
            .orient("bottom");
        var x2Axis = d3.svg.axis()
            .scale(x2)
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("right");
        var y2Axis = d3.svg.axis()
            .scale(y2)
            .orient("right");

        // Air Temperature Visualization
        detailVis.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 10)
            .text("Air Temperature");

        detailVis.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + bbDetailVis.h + ")")
          .call(xAxis);

        detailVis.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(" + bbDetailVis.w + ", 0)")
          .call(yAxis)

        detailVis.selectAll(".bar")
            .data(airData)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { 
            return x(+d.date.getMonth()); })
          .attr("width", x.rangeBand())
          .attr("y", function(d) { 
            return y(d.value); })
          .attr("height", function(d) { return bbDetailVis.h - y(d.value); })
          .attr("fill", function(d) {
            return "rgb(" + (d.value * 10) + ", 0, 0)";
            });

        // Water Temperature Visualization
        detailVis2.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 10)
            .text("Water Temperature");

        detailVis2.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + bbDetailVis.h + ")")
          .call(x2Axis);

        detailVis2.append("g")
          .attr("class", "y axis")
          .attr("transform", "translate(" + bbDetailVis.w + ", 0)")
          .call(y2Axis)

        detailVis2.selectAll(".bar2")
            .data(waterData)
        .enter().append("rect")
          .attr("class", "bar2")
          .attr("x", function(d) { 
            return x2(+d.date.getMonth()); })
          .attr("width", x.rangeBand())
          .attr("y", function(d) { 
            return y2(d.value); })
          .attr("height", function(d) { return bbDetailVis.h - y2(d.value); })
          .attr("fill", function(d) {
            return "rgb(0, 0, " + (d.value * 10) + ")";
            });

}


var updateDetailVis = function(data, name){
    detailVis.selectAll(".axis").data(data).exit().remove();
    detailVis.selectAll(".bar").data(data).exit().remove();
    detailVis.selectAll(".bar2").data(data).exit().remove();
    detailVis.selectAll(".label").data(data).exit().remove();
}

// zoom function taken from click-to-zoom example: http://bl.ocks.org/mbostock/2206590
function clicked(d) {
  if (active.node() === this) return reset();
  active.classed("active", false);
  active = d3.select(this).classed("active", true);

  var bounds = path.bounds(d),
      dx = bounds[1][0] - bounds[0][0],
      dy = bounds[1][1] - bounds[0][1],
      x = (bounds[0][0] + bounds[1][0]) / 2,
      y = (bounds[0][1] + bounds[1][1]) / 2,
      scale = .9 / Math.max(dx / width, dy / height),
      translate = [width / 2 - scale * x, height / 2 - scale * y];

  svg.transition()
      .duration(750)
      .style("stroke-width", 1.5 / scale + "px")
      .attr("transform", "translate(" + translate + ")scale(" + scale + ")");
}


function reset() {
  active.classed("active", false);
  active = d3.select(null);

  svg.transition()
      .duration(750)
      .style("stroke-width", "1.5px")
      .attr("transform", "");
}


function zoom() {
  svg.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
}



