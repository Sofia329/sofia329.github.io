// https://plotly.com/javascript/figure-labels/

// the below rangeselector helped with AI
const x_axis = {
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
};

const y_axis = {
   title: {
      text: "Daily Price",
      standoff: 20,
      font: {
         family: "Courier New, monospace",
         size: 18,
         color: "#7f7f7f"
      }
   }
};




document.addEventListener('DOMContentLoaded', function(){

        document.querySelectorAll('.Watchlist').forEach(watchlist => {
            // add eventlistener to each of the watchlist table
            watchlist.addEventListener('click' , event => {
                if (event.target.tagName === 'A'){
                    let ticker = event.target.dataset.ticker;
                    let category = watchlist.dataset.category;
                    // plot the chart for the ticker user clicked
                    const data = document.getElementById(category);
                    if (data){
                        const chart = JSON.parse(data.textContent);
                        const item = chart.find(function(item) {
                           return item.ticker === ticker;
                        });
                        if (item && item.plot){
                           const close = {x: Object.keys(item.plot), y: Object.values(item.plot) , type: "scatter", mode:"lines", name: "Close Price", fill: "none", connectgaps: false};
                           const layout = {
                              title : {text: `${item.fullname} <Ticker: ${item.ticker}>` , font: { family: "Courier New, monospace"}},
                              xaxis: x_axis,
                              yaxis: y_axis
                           };
                            Plotly.newPlot('dashboard-chart', [close], layout);
                        }
                    }
                }
            });
        });


        // add eventlistener to the category click, and show corresponding table
        document.querySelector('.menu').addEventListener('click', function(event) {
            const button = event.target.closest('button');

            // hide all tables before show the clicked one
            document.querySelectorAll('.Watchlist').forEach(watchlist =>{
                watchlist.hidden=true;
            })
            const category = button.dataset.category;
            let table = document.querySelector(`table[data-category="${category}"]`);
            table.hidden=false;

        });
        // setInterval Polling for live stream data of the ticker every 5 secs
        // start setInterval when the watchlist tables all loaded
        const tables = document.querySelectorAll('.Watchlist');
        if (tables.length > 0){

            setInterval(() => {
               fetch('/dashboard?livestream=true')
               .then(response => response.json())
               .then(live => {
                  console.log(live);
                  tables.forEach(table => {
                     console.log(table);
                     table.querySelectorAll('tr').forEach(row => {
                        const ticker = row.querySelector('a').dataset.ticker;
                        const liveprice = live.liveprice[ticker];

                        // update the td with new price, change, change percent
                        if (liveprice){
                           const pricetd = row.querySelector('.price');
                           const changetd = row.querySelector('.change');
                           const changepercenttd= row.querySelector('.change_percent');

                           pricetd.textContent = liveprice.price.toFixed(2);
                           changetd.textContent = liveprice.change.toFixed(2);
                           changepercenttd.textContent = liveprice.change_percent.toFixed(2) +'%';

                           // design the green/red flash of liveprice
                           pricetd.classList.remove('up','down');
                           changetd.classList.remove('up','down');
                           changepercenttd.classList.remove('up','down');

                           void pricetd.offsetWidth;
                           void changetd.offsetWidth;
                           void changepercenttd.offsetWidth;

                           if(liveprice.change > 0){
                              pricetd.classList.add('up');
                              changetd.classList.add('up');
                              changepercenttd.classList.add('up');
                           } else if (liveprice.change < 0 ) {
                              pricetd.classList.add('down');
                              changetd.classList.add('down');
                              changepercenttd.classList.add('down');
                           }
                        }
                     }) // finish each row updates
                  }) // finish each table updates

              })
              .catch(error =>{alert(error.message);})

            }, 5000); // fetch for live stream data every 5 secs

        }

});


