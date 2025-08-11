var chartOptions = {
  chart: {
    height: 400,
    fontFamily: 'Helvetica, Arial, sans-serif',
    foreColor: '#6E729B',
    toolbar: {
      show: false,
    },
  },
  stroke: {
    curve: 'smooth',
    width: 2,
  },
  series: [
    {
      name: 'Install',
      data: [1, 15, 26, 20, 33, 27],
    },
    {
      name: 'CPI',
      data: [3, 33, 21, 42, 19, 32],
    },
  ],
  title: {
    text: 'Performance',
    align: 'left',
    offsetY: 25,
    offsetX: 5,
    style: {
      fontSize: '14px',
      fontWeight: 'bold',
      color: '#373d3f',
    },
  },
  markers: {
    size: 6,
    strokeWidth: 0,
    hover: {
      size: 9,
    },
  },
  grid: {
    show: true,
    padding: {
      bottom: 0,
    },
  },
  labels: ['20/12', '21/12', '22/12', '23/12', '24/12', '25/12'],
  xaxis: {
    tooltip: {
      enabled: false,
    },
  },
  legend: {
    position: 'top',
    horizontalAlign: 'right',
    offsetY: -10,
    labels: {
      colors: '#373d3f',
    },
  },
  yaxis: [
    {
      title: {
        text: 'Install',
      },
      labels:{
        formatter: function (value) {
          return parseInt(value); // Tam sayı olarak göster
        }

      },
      
      // Set the max value for the left y-axis
    },
    {
      opposite: true,
      title: {
        text: 'CPI',
      },
      labels:{
        formatter: function (value) {
          return parseFloat(value); // Tam sayı olarak göster
        }
      },
      
      // Set the max value for the right y-axis to match the left axis
    },
  ],
  grid: {
    borderColor: '#D9DBF3',
    xaxis: {
      lines: {
        show: true,
      },
    },
  }
};

var lineChart = new ApexCharts(document.querySelector('#line-chart'), chartOptions);
lineChart.render();

window.updateLineChartData=async function updateLineChartData(gameId)
{     
  const response = await fetch('/update_line_chart_data', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ game_id: gameId })
  });
  if(response.ok){
    datas= await response.json();
    console.log();


    const installData = [];
    const cpiData = [];
    
    datas.forEach(element => {
        installData.push(parseInt(element.install)); // Install değerini ekle
        cpiData.push(parseFloat(element.cpi));        // CPI değerini ekle
    });
    
    // Series kısmını güncelle
    lineChart.updateSeries([
        {
            name: 'Install',
            data: installData
        },
        {
            name: 'CPI',
            data: cpiData
        }
    ]);
    

    //chartOptions.series.push({name:"Installs",data:})
  }

}



