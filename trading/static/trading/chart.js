// https://plotly.com/javascript/figure-labels/

// the below rangeselector helped with AI
x_axis = {
   type: "date",
   title:{
      text: "Date",
      font: {
         family: "Courier New, monospace",
         size: 18,
         color: "#7f7f7f"
      }
   },
   rangeselector: {
      buttons: [
      { label: "1m", step: "month", count: 1, stepmode: "backward" },
      { label: "6m", step: "month", count: 6, stepmode: "backward" },
      { label: "YTD", step: "year", stepmode: "todate" },
      { label: "1y", step: "year", count: 1, stepmode: "backward" },
      { label: "all", step: "all" }
      ]
   }
}

y_axis = {
   title: {
      text: "Daily Price",
      standoff: 20,
      font: {
         family: "Courier New, monospace",
         size: 18,
         color: "#7f7f7f"
      }
   }
}

document.addEventListener('DOMContentLoaded', function(){

   const chart = document.querySelector('#chart-data');

   if (chart) {

      const data = JSON.parse(chart.textContent);
      const close = {x: data.dates, y: data.close, type: "scatter", mode: "lines", name: "Close", fill: "none", connectgaps: false};
      const adj_close = {x: data.dates, y: data.adj_close, type: "scatter", mode: "lines", name: "Adjust Close",fill: "none", connectgaps: false};
      const open = {x: data.dates, y: data.open, type: "scatter", mode: "lines", name: "Open", fill: "none", connectgaps: false};
      const high = {x: data.dates, y: data.high, type: "scatter", mode: "lines", name: "High", fill: "none", connectgaps: false};
      const low = {x: data.dates, y: data.low, type: "scatter", mode: "lines", name: "Low", fill: "none", connectgaps: false};

      const layout1 = {
         title: {text: data.ticker + " High-Low Price", font:{family: "Courier New, monospace"} },
         xaxis: x_axis,
         yaxis: y_axis
      };

      const layout2 = {
         title: {text: data.ticker + " Open-Close Price", font:{family: "Courier New, monospace"}},
         xaxis: x_axis,
         yaxis: y_axis
      };

      const layout3 = {
         title: {text: data.ticker + " Close-Adj_Close Price", font:{family: "Courier New, monospace"} },
         xaxis: x_axis,
         yaxis: y_axis
      };

      Plotly.newPlot("chart1", [high, low], layout1);
      Plotly.newPlot("chart2", [open, close], layout2);
      Plotly.newPlot("chart3", [close, adj_close], layout3);
   }

});



