
var margin = {
    top: 50,
    right: 50,
    bottom: 50,
    left: 50
};

var width = 1060 - margin.left - margin.right;
var height = 800 - margin.bottom - margin.top;

/**
** Intro code for merge
*/

var bbAirWater = {
    w: 350,
    h: 200,
    x: 0,
    y: 0
}

var bbBest = {
    w: 350,
    h: 500,
    x: 0,
    y: 300
}

var bbSwell = {
    w: 350,
    h: 800,
    x: 0,
    y: 600
}

var detailCanvas = d3.select("#detailVis").append("svg").attr({
  width: 450 + margin.left + margin.right,
  height: 800 + margin.top + margin.bottom
})

var detailVis = detailCanvas.append("g").attr({
  transform: "translate(" + margin.left + "," + margin.top + ")"
})

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
    // .on("click", clicked);

var g = svg.append("g");

/*
**
*/

var centered;

var projection = d3.geo.mercator()
    .center([0, 60 ])
    .scale(150)
    .rotate([0,0]);

var path = d3.geo.path()
    .projection(projection);

var dataSet = {};

// load and display the World
d3.json("world-110m2.json", function(error, topology) {
    g.selectAll("path")
      .data(topojson.feature(topology, topology.objects.countries)
          .features)
    .enter()
      .append("path")
      .attr("d", path)
	  .on("click", clicked)
	  
d3.csv("../data/Site_table_dummy5.csv", function(error, data) {
    dataSet = data;
        g.selectAll("circle")
          .data(data)
          .enter()
		  .append("circle")
		  .filter(function(d) { return d.Country != null ? this : null; })

    /*
    ** Data wrangling
    */

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
        var parsed_best;
        var parsed_swell;

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
            parsed_best = monthParser(timeParser.parse(property.slice(12)));
            if (typeof d.BestSurfing[parsed_best] === "undefined") {
                d.BestSurfing[parsed_best] = 0;
            }
            d.BestSurfing[parsed_best] += +value;
          }
          else if (property.slice(0, 12) == "TypicalSwell" && typeof value != 'object'){
            parsed_swell = monthParser(timeParser.parse(property.slice(13)));
            if (typeof d.TypicalSwell[parsed_swell] === "undefined") {
                d.TypicalSwell[parsed_swell] = 0;
            }
            d.TypicalSwell[parsed_swell] += +value;
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
		   
d3.selectAll(".filter_button").on("change", function() {
  var type = this.value, 
  // I *think* "inline" is the default.
  display = this.checked ? "inline" : "none";

svg.selectAll("circle")
    .filter(function(d) { return d.Country === type })
	.attr("cx", function(d) {
                   return projection([d.Longitude, d.Latitude])[0];
           })
    .attr("cy", function(d) {
                   return projection([d.Longitude, d.Latitude])[1];
           })
    .attr("r", 2)
    .style("fill", "orange")
    .style("opacity", .7)
    .attr("display", display)
  .on("click", function(d) {
          createDetailVis(d, d.Spot);   
       })
	.on("mouseover", function(d) { 
      d3.select(this)
                .style("fill", "blue")

            div.transition()        
                .duration(200)      
                .style("opacity", .9);      
            div .html(d.Spot + ", " + d.Country)
                .style("left", (d3.event.pageX) + "px")     
                .style("top", (d3.event.pageY - 28) + "px");    
            })                  
        .on("mouseout", function(d) {    
          d3.select(this)   
            .style("fill", "orange")

            div.transition()        
                .duration(500)      
                .style("opacity", 0);   
        });	   
});		     
	
var div = d3.select("body").append("div")   
    .attr("class", "tooltip")               
    .style("opacity", 0);	  


	
});

})

/*
**
*/

var createDetailVis = function(data, name){

    updateDetailVis(data, name);

        var multiObj = []; 
        var bestSurfing = [];
        var typicalSwell = [];
        var airObj = {};
        var airValue = [];
        var waterObj = {};
        var waterValue = [];

        var parse_date = d3.time.format('%b');

        var air_data = data.AirTemp;
        var water_data = data.WaterTemp;
        var best_data = data.BestSurfing;
        var swell_data = data.TypicalSwell;

        /*
        ** Air Temperature + Water Temperature line graph data wrangling
        */

        airObj.name = 'Air Temperature';
        airObj.values = airValue;
        for (key in air_data) {
            d = {};
            d.date = parse_date.parse(key);
            d.temp = air_data[key];
            d.name = airObj.name;
            airValue.push(d);
        }

        airValue.sort(function(a,b){
            return d3.ascending(a.date, b.date);
        });

        multiObj.push(airObj);

        waterObj.name = 'Water Temperature';
        waterObj.values = waterValue;
        for (key in water_data) {
            e = {};
            e.date = parse_date.parse(key);
            e.temp = water_data[key];
            e.name = waterObj.name;
            waterValue.push(e);
        }

        waterValue.sort(function(a,b){
            return d3.ascending(a.date, b.date);
        });

        multiObj.push(waterObj);

        /*
        ** Best Surfing data wrangling
        */ 

        for (key in best_data) {
            b = {};
            b.date = parse_date.parse(key);
            b.value = best_data[key];
            b.name = 'Best Surfing';
            bestSurfing.push(b);
        }

        bestSurfing.sort(function(a,b){
            return d3.ascending(a.date, b.date);
        });

        console.log(bestSurfing);
        console.log(multiObj);

        /*
        ** Typical Swell data wrangling
        */

        for (key in swell_data) {
            s = {};
            s.date = parse_date.parse(key);
            s.value = swell_data[key];
            s.name = 'Typical Swell';
            typicalSwell.push(s);
        }

        typicalSwell.sort(function(a,b){
            return d3.ascending(a.date, b.date);
        });

        console.log(typicalSwell);

        // Water & Air Temperature multiline graph
        var x = d3.time.scale()
          .domain([
            d3.min(multiObj, function(d) { return d3.min(d.values, function(x) { return x.date; }); }), 
            d3.max(multiObj, function(d) { return d3.max(d.values, function(x) { return x.date; }); })
          ])
          .range([0, bbAirWater.w])

        var y = d3.scale.linear()
          .domain([
            d3.min(multiObj, function(c) { return d3.min(c.values, function(v) { return v.temp; }); }), 
            d3.max(multiObj, function(c) { return d3.max(c.values, function(v) { return v.temp; }); })
          ])
          .range([bbAirWater.h, 0]);

        var color = d3.scale.category10();

        var xAxis = d3.svg.axis()
            .scale(x)
            .tickFormat(d3.time.format('%b'))
            .orient("bottom");

        var yAxis = d3.svg.axis()
            .scale(y)
            .orient("left");

        var line = d3.svg.line()
            .interpolate("cardinal")
            .x(function(d) { return x(d.date); })
            .y(function(d) { return y(d.temp); });

        detailVis.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", -10)
            .text("Air/Water Temperature");

        detailVis.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + (bbAirWater.h) + ")")
            .call(xAxis);

        detailVis.append("g")
            .attr("class", "y axis")
            .call(yAxis)
          .append("text")
            .attr("transform", "rotate(-90)", "translate(" + (bbAirWater.w) + ", 0)")
            .attr("y", 6)
            .attr("dy", ".71em")
            .style("text-anchor", "end")
            .text("Temperature \xB0C");

        var multiline = detailVis.selectAll(".multiline")
            .data(multiObj)
          .enter().append("g")
            .attr("class", "multiline");

        multiline.append("path")
            .attr("class", "line")
            .attr("d", function(d) { return line(d.values); })
            .style("stroke", function(d) { return color(d.name); });

        multiline.append("text")
            .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
            .attr("transform", function(d) { return "translate(" + x(d.value.date) + "," + y(d.value.temp) + ")"; })
            .attr("x", 3)
            .attr("dy", ".35em")
            .text(function(d) { return d.name; });

        detailVis.selectAll('g.dot')
          .data(multiObj)
          .enter().append('g')
          .attr("class", "dot")
          .selectAll('circle')
          .data(function(d) { return d.values })
          .enter().append('circle')
          .attr("cx", function(d) { return x(d.date) })
          .attr("cy", function(d) { return y(d.temp) })
          .attr("r", 3)
          .style("fill", function(d) { 
              return color(d.name);
          });

        // Best Surfing Bar Graph
        var x2 = d3.time.scale()
          .domain(d3.extent(bestSurfing, function(d){ return d.date; })) 
          .range([0, bbBest.w])

        var y2 = d3.scale.linear()
            .domain([0, 5]) 
            .range([bbBest.h, bbBest.y]);

        var x2Axis = d3.svg.axis()
            .scale(x2)
            .tickFormat(d3.time.format('%b'))
            .orient("bottom");

        var y2Axis = d3.svg.axis()
            .scale(y2)
            .ticks(6)
            .orient("left");

        detailVis.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 290)
            .text("Best Surfing");

        detailVis.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + bbBest.h + ")")
          .call(x2Axis);

        detailVis.append("g")
          .attr("class", "y axis")
          .call(y2Axis)
        .append("text")
          .attr("transform", "rotate(-90)", "translate(" + (bbBest.w) + ",0)")
          .attr("x", -300)
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Rating");

        detailVis.selectAll(".bar")
            .data(bestSurfing)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { 
            return x2(d.date); })
          .attr("width", 20)
          .attr("y", function(d) { 
            return y2(d.value); })
          .attr("height", function(d) { return bbBest.h - y2(d.value); })
          .attr("fill", function(d) {
            return "rgb(" + (d.value * 40) + ", 0, 0)";
            });

        // Typical Swell Bar Graph
        var x3 = d3.time.scale()
          .domain(d3.extent(typicalSwell, function(d){ return d.date; })) 
          .range([0, bbSwell.w])

        var y3 = d3.scale.linear()
            .domain([0, 5]) 
            .range([bbSwell.h, bbSwell.y]);

        var x3Axis = d3.svg.axis()
            .scale(x3)
            .tickFormat(d3.time.format('%b'))
            .orient("bottom");

        var y3Axis = d3.svg.axis()
            .scale(y3)
            .ticks(6)
            .orient("left");

        detailVis.append("text")
            .attr("class", "label")
            .attr("x", 0)
            .attr("y", 590)
            .text("Typical Swell Size");

        detailVis.append("g")
          .attr("class", "x axis")
          .attr("transform", "translate(0," + bbSwell.h + ")")
          .call(x3Axis);

        detailVis.append("g")
          .attr("class", "y axis")
          .call(y3Axis)
        .append("text")
          .attr("transform", "rotate(-90)", "translate(" + (bbSwell.w) + ",0)")
          .attr("x", -600)
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Rating");

        detailVis.selectAll(".swell_bar")
            .data(typicalSwell)
        .enter().append("rect")
          .attr("class", "bar swell_bar")
          .attr("x", function(d) { 
            return x3(d.date); })
          .attr("width", 20)
          .attr("y", function(d) { 
            return y3(d.value); })
          .attr("height", function(d) { return bbSwell.h - y3(d.value); })
          .attr("fill", function(d) {
            return "rgb(0, 0, " + (d.value * 40) + ")";
            });

}

var updateDetailVis = function(data, name){
    detailVis.selectAll(".axis").data(data).exit().remove();
    detailVis.selectAll(".dot").data(data).exit().remove();
    detailVis.selectAll(".multiline").data(data).exit().remove();
    detailVis.selectAll(".bar").data(data).exit().remove();
    detailVis.selectAll(".swell_bar").data(data).exit().remove();
    detailVis.selectAll(".label").data(data).exit().remove();
}

/*
**
*/

function clicked(d) {
  var x, y, k;
  if (d && centered !== d) {
    var centroid = path.centroid(d);
    x = centroid[0];
    y = centroid[1];
    k = 4;
    centered = d;
  } else {
    x = width / 2;
    y = height / 2;
    k = 1;
    centered = null;
  }
  g.selectAll("path")
      .classed("active", centered && function(d) { return d === centered; });
  g.transition()
      .duration(750)
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")scale(" + k + ")translate(" + -x + "," + -y + ")")
      .style("stroke-width", 1.5 / k + "px");
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


//references
//http://bl.ocks.org/d3noob/5189284
//


