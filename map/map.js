
var width = 960,
    height = 500;

var centered;

var projection = d3.geo.mercator()
    .center([0, 5 ])
    .scale(150)
    .rotate([0,0]);

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

var path = d3.geo.path()
    .projection(projection);

var g = svg.append("g");

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
	  
d3.csv("Site_table_dummy3.csv", function(error, data) {
    dataSet = data;
        g.selectAll("circle")
          .data(data)
          .enter()
		  .append("circle")
		  .filter(function(d) { return d.Country != null ? this : null; })
		  

		   
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
    .style("fill", "red")
    .attr("display", display)
	.on("mouseover", function(d) {      
            div.transition()        
                .duration(200)      
                .style("opacity", .9);      
            div .html(d.Spot + ", " + d.Country)
                .style("left", (d3.event.pageX) + "px")     
                .style("top", (d3.event.pageY - 28) + "px");    
            })                  
        .on("mouseout", function(d) {       
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

// zoom and pan
//var zoom = d3.behavior.zoom()
  //  .on("zoom",function() {
    //    g.attr("transform","translate("+ 
      //      d3.event.translate.join(",")+")scale("+d3.event.scale+")");
        //g.selectAll("path")  
          //  .attr("d", path.projection(projection)); 
  //});

//svg.call(zoom)

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



//references
//http://bl.ocks.org/d3noob/5189284
//


