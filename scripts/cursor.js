document.getElementById('map-graph').on('plotly_hover', function(data) {
    var element = document.getElementById('map-graph');
    console.log(element);
    element.style.cursor = 'pointer';
});

document.getElementById('map-graph').on('plotly_unhover', function(data) {
    var element = document.getElementById('map-graph');
    console.log(element);
    element.style.cursor = 'default';
});