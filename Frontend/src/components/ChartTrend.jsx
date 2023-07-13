import React from 'react';
import BASE_URL from './config';
import ReactEcharts from "echarts-for-react"; 
import SelectYear from './SelectYear';

const ChartTrend = () => {
  const [year, setYear] = React.useState("-");
  const [liquor, setLiquor] = React.useState(null);
  const [crash, setCrash] = React.useState(null);
  const [crime, setCrime] = React.useState(null);

  const xs = ['Melbourne', 'Yarra', 'Casey', 'Hume', 'Baw baw', 'Hepburn', 'Bayside', 'Darebin', 'Ballarat', 'Frankston', 'Gannawarra'];
  let headers = new Headers();
  headers.append('Access-Control-Allow-Origin', 'http://localhost:3000');
  headers.append('Content-Type', 'application/json');
  headers.append('Accept', 'application/json');

  React.useEffect(() => {
    if (year === '2017') {
      fetch2017LiquorLga();
      fetch2017CrashLga();
      fetch2017CrimeLga();
    } else if (year === '2018') {
      fetch2018LiquorLga();
      fetch2018CrashLga();
      fetch2018CrimeLga();
    } else if (year === '2019') {
      fetch2019LiquorLga();
      fetch2019CrashLga();
      fetch2019CrimeLga();
    }
  }, [year]);

  const fetch2017LiquorLga = async () => {
    const response = await fetch(BASE_URL + "liquor_data/view/sudo/2017LGA?reduce=true&group=true", {method:"GET", headers:headers});
    const data = await response.json();
    let liquor_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {liquor_list[xs.indexOf(place)] = d.value}});
    })
    setLiquor(liquor_list);
  }

  const fetch2018LiquorLga = async () => {
    const response = await fetch(BASE_URL + "liquor_data/view/sudo/2018LGA?reduce=true&group=true", {method:"GET", headers:headers});
    const data = await response.json();
    let liquor_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {liquor_list[xs.indexOf(place)] = d.value}});
    })
    setLiquor(liquor_list);
  }
  const fetch2019LiquorLga = async () => {
    const response = await fetch(BASE_URL + "liquor_data/view/sudo/2019LGA?reduce=true&group=true", {method:"GET", headers:headers});
    const data = await response.json();
    let liquor_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {liquor_list[xs.indexOf(place)] = d.value}});
    })
    setLiquor(liquor_list);
  }

  const fetch2017CrashLga = async () => {
    const response = await fetch(BASE_URL + "crash_data/view/test/2017crashByLga?reduce=true&group=true", {method:"GET", headers:headers});
    const data = await response.json();
    let crash_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {crash_list[xs.indexOf(place)] = d.value}});
    })
    setCrash(crash_list);
  }

  const fetch2018CrashLga = async () => {
    const response = await fetch(BASE_URL + "crash_data/view/test/2018crashByLga?reduce=true&group=true", {method:"GET", headers:headers});
    const data = await response.json();
    let crash_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {crash_list[xs.indexOf(place)] = d.value}});
    })
    setCrash(crash_list);
  }

  const fetch2019CrashLga = async () => {
    const response = await fetch(BASE_URL + "crash_data/view/test/2019crashByLga?reduce=true&group=true", {method:"GET", headers:headers});
    const data = await response.json();
    let crash_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {crash_list[xs.indexOf(place)] = d.value}});
    })
    setCrash(crash_list);
  }

  const fetch2017CrimeLga = async () => {
    const response = await fetch(BASE_URL + "crime_data/view/statistic/2017crimeByLga", {method:"GET", headers:headers});
    const data = await response.json();
    let crime_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {crime_list[xs.indexOf(place)] = d.value}});
    })
    setCrime(crime_list);
  }

  const fetch2018CrimeLga = async () => {
    const response = await fetch(BASE_URL + "crime_data/view/statistic/2018crimeByLga", {method:"GET", headers:headers});
    const data = await response.json();
    let crime_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {crime_list[xs.indexOf(place)] = d.value}});
    })
    setCrime(crime_list);
  }

  const fetch2019CrimeLga = async () => {
    const response = await fetch(BASE_URL + "crime_data/view/statistic/2019crimeByLga", {method:"GET", headers:headers});
    const data = await response.json();
    let crime_list = new Array(12).fill(0);
    xs.forEach(place => {
      let re = new RegExp(`${place}`, "gi");
      data.forEach(d => { if (d.key.match(re)) {crime_list[xs.indexOf(place)] = d.value}});
    })
    setCrime(crime_list);
  }


  var option;
  option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['Liquor', 'Crash', 'Crime']
    },
    toolbox: {
      show: true,
      orient: 'vertical',
      left: 'right',
      top: 'center',
      feature: {
        mark: { show: true },
        dataView: { show: true, readOnly: false },
        magicType: { show: true, type: ['line', 'bar', 'stack'] },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    xAxis: [
      {
        name: 'LGA',
        type: 'category',
        axisTick: { show: false },
        data: xs,
        axisLabel: {
          show: true,
          interval: 0,
          rotate: 45,
        },
      }
    ],
    yAxis: [
      {
        name: 'Number of Records',
        type: 'value'
      }
    ],
    series: [
      {
        name: 'Liquor',
        type: 'bar',
        barGap: 0,
        emphasis: {
          focus: 'series'
        },
        data: liquor
      },
      {
        name: 'Crash',
        type: 'bar',
        emphasis: {
          focus: 'series'
        },
        data: crash
      },
      {
        name: 'Crime',
        type: 'bar',
        emphasis: {
          focus: 'series'
        },
        data: crime
      },
    ]
  };

  return (
    <div width="700px" height="500px">

        <div className="chart-title">Chart2 - Trend Similarity Comparison Across LGA </div>
        <SelectYear onYearChange={setYear} />
        <ReactEcharts style={{width: 800,height: 600}} option={option} />
    </div>
  ) 
}

export default ChartTrend;