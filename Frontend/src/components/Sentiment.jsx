import React, {useEffect,useState} from 'react';
import BASE_URL from './config';
import ReactEcharts from "echarts-for-react";
import SelectTopic from './SelectTopic';
import SelectStats from './SelectStats';

const Sentiment = () => {
    const [topic, setTopic] = React.useState("");
    const [stats, setStats] = React.useState("");
    const [xaxis, setXaxis] = useState([]);
    const [yaxis_p, setYaxisP] = useState([]);
    const [yaxis_n, setYaxisN] = useState([]);
    const [min_p, setMinP] = useState(0);
    const [min_n, setMinN] = useState(-1);
    const [max_p, setMaxP] = useState(1);
    const [max_n, setMaxN] = useState(0);
    const [inverse, setInverse] = useState(true);
    const [liquor_time, setLiquorTime] = useState([]);
    const [p_liquor_s, setPLiquorS] = useState(0);
    const [n_liquor_s, setNLiquorS] = useState(0);
    const [p_liquor_c, setPLiquorC] = useState(0);
    const [n_liquor_c, setNLiquorC] = useState(0);
    const [p_liquor_a, setPLiquorA] = useState(0);
    const [n_liquor_a, setNLiquorA] = useState(0);
    const [crash_time, setCrashTime] = useState([]);
    const [p_crash_s, setPCrashS] = useState(0);
    const [n_crash_s, setNCrashS] = useState(0);
    const [p_crash_c, setPCrashC] = useState(0);
    const [n_crash_c, setNCrashC] = useState(0);
    const [p_crash_a, setPCrashA] = useState(0);
    const [n_crash_a, setNCrashA] = useState(0);
    const [crime_time, setCrimeTime] = useState([]);
    const [p_crime_s, setPCrimeS] = useState(0);
    const [n_crime_s, setNCrimeS] = useState(0);
    const [p_crime_c, setPCrimeC] = useState(0);
    const [n_crime_c, setNCrimeC] = useState(0);
    const [p_crime_a, setPCrimeA] = useState(0);
    const [n_crime_a, setNCrimeA] = useState(0);


    let headers = new Headers();
    headers.append('Access-Control-Allow-Origin', 'http://localhost:3000');
    headers.append('Content-Type', 'application/json');
    headers.append('Accept', 'application/json');

    const fetchPostiveLiquor = async () => {
        const response = await fetch(BASE_URL + "tweet_data_yuan/view/tweet/PositiveLiquorByTime?reduce=true&group=true", {method:"GET", headers:headers});
        const data = await response.json();
        const time = data.map(d => d.key);
        const sum = data.map(d => d.value.sum);
        const count = data.map(d => d.value.count);
        const average = data.map(d => d.value.sum / d.value.count);
        setLiquorTime(time);
        setPLiquorS(sum);
        setPLiquorC(count);
        setPLiquorA(average);
    };
    
    const fetchNegativeLiquor = async () => {
        const response = await fetch(BASE_URL + "tweet_data_yuan/view/tweet/NegativeLiquorByTime?reduce=true&group=true", {method:"GET", headers:headers})
        const data = await response.json();
        const sum = data.map(d => d.value.sum);
        const count = data.map(d => d.value.count);
        const average = data.map(d => d.value.sum / d.value.count);
        setNLiquorS(sum);
        setNLiquorC(count);
        setNLiquorA(average);
    };

    const fetchPostiveCrash = async () => {
        const response = await fetch(BASE_URL + "tweet_data_yuan/view/tweet/PositiveCrashByTime?reduce=true&group=true", {method:"GET", headers:headers});
        const data = await response.json();
        const time = data.map(d => d.key);
        const sum = data.map(d => d.value.sum);
        const count = data.map(d => d.value.count);
        const average = data.map(d => d.value.sum / d.value.count);
        setCrashTime(time);
        setPCrashS(sum);
        setPCrashC(count);
        setPCrashA(average);
    };
    
    const fetchNegativeCrash = async () => {
        const response = await fetch(BASE_URL + "tweet_data_yuan/view/tweet/NegativeCrashByTime?reduce=true&group=true", {method:"GET", headers:headers})
        const data = await response.json();
        const sum = data.map(d => d.value.sum);
        const count = data.map(d => d.value.count);
        const average = data.map(d => d.value.sum / d.value.count);
        setNCrashS(sum);
        setNCrashC(count);
        setNCrashA(average);
    };

    const fetchPostiveCrime = async () => {
        const response = await fetch(BASE_URL + "tweet_data_yuan/view/tweet/PositiveCrimeByTime?reduce=true&group=true", {method:"GET", headers:headers});
        const data = await response.json();
        const time = data.map(d => d.key);
        const sum = data.map(d => d.value.sum);
        const count = data.map(d => d.value.count);
        const average = data.map(d => d.value.sum / d.value.count);
        setCrimeTime(time);
        setPCrimeS(sum);
        setPCrimeC(count);
        setPCrimeA(average);
    };
    
    const fetchNegativeCrime = async () => {
        const response = await fetch(BASE_URL + "tweet_data_yuan/view/tweet/NegativeCrimeByTime?reduce=true&group=true", {method:"GET", headers:headers})
        const data = await response.json();
        const sum = data.map(d => d.value.sum);
        const count = data.map(d => d.value.count);
        const average = data.map(d => d.value.sum / d.value.count);
        setNCrimeS(sum);
        setNCrimeC(count);
        setNCrimeA(average);
    };

    

    useEffect(() => {
        if (topic === "Liquor") {
            fetchPostiveLiquor();
            fetchNegativeLiquor();
            if (stats === "Sum") {
                setXaxis(liquor_time);
                setYaxisP(p_liquor_s);
                setYaxisN(n_liquor_s);
                setMinP(0);
                setMaxP(100);
                setMinN(-100);
                setMaxN(0);
                setInverse(true);
            } else if (stats === "Count") {
                setXaxis(liquor_time);
                setYaxisP(p_liquor_c);
                setYaxisN(n_liquor_c);
                setMinP(0);
                setMaxP(250);
                setMinN(0);
                setMaxN(250);
                setInverse(false);
            } else if (stats === "Average") {
                setXaxis(liquor_time);
                setYaxisP(p_liquor_a);
                setYaxisN(n_liquor_a);
                setMinP(0);
                setMaxP(1);
                setMinN(-1);
                setMaxN(0);
                setInverse(true);
            }
        } else if (topic === "Crash") {
            fetchPostiveCrash();
            fetchNegativeCrash();
            if (stats === "Sum") {
                setXaxis(crash_time);
                setYaxisP(p_crash_s);
                setYaxisN(n_crash_s);
                setMinP(0);
                setMaxP(100);
                setMinN(-100);
                setMaxN(0);
                setInverse(true);
            } else if (stats === "Count") {
                setXaxis(crash_time);
                setYaxisP(p_crash_c);
                setYaxisN(n_crash_c);
                setMinP(0);
                setMaxP(250);
                setMinN(0);
                setMaxN(250);
                setInverse(false);
            } else if (stats === "Average") {
                setXaxis(crash_time);
                setYaxisP(p_crash_a);
                setYaxisN(n_crash_a);
                setMinP(0);
                setMaxP(1);
                setMinN(-1);
                setMaxN(0);
                setInverse(true);
            }
        } else if (topic === "Crime") {
            fetchPostiveCrime();
            fetchNegativeCrime();
            if (stats === "Sum") {
                setXaxis(crime_time);
                setYaxisP(p_crime_s);
                setYaxisN(n_crime_s);
                setMinP(0);
                setMaxP(100);
                setMinN(-100);
                setMaxN(0);
                setInverse(true);
            } else if (stats === "Count") {
                setXaxis(crime_time);
                setYaxisP(p_crime_c);
                setYaxisN(n_crime_c);
                setMinP(0);
                setMaxP(250);
                setMinN(0);
                setMaxN(250);
                setInverse(false);
            } else if (stats === "Average") {
                setXaxis(crime_time);
                setYaxisP(p_crime_a);
                setYaxisN(n_crime_a);
                setMinP(0);
                setMaxP(1);
                setMinN(-1);
                setMaxN(0);
                setInverse(true);
            }
        }
        
      }, [topic, stats]);


    var option = {
        title: {
        text: 'Sentiment Statistics across 24 hours',
        left: 'center'
        },
        grid: {
        bottom: 80
        },
        toolbox: {
        feature: {
            dataZoom: {
            yAxisIndex: 'none'
            },
            restore: {},
        }
        },
        tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            animation: false,
            label: {
            backgroundColor: '#505765'
            }
        }
        },
        legend: {
        data: ['Positive', 'Negative'],
        left: 10
        },
        dataZoom: [
        {
            show: true,
            realtime: true,
            start: 0,
            end: 100
        },
        {
            type: 'inside',
            realtime: true,
            start: 65,
            end: 85
        }
        ],
        xAxis: [
        {
            type: 'category',
            boundaryGap: false,
            axisLine: { onZero: false },
            // prettier-ignore
            data: xaxis
        }
        ],
        yAxis: [
        {
            name: 'Positive Statistic',
            type: 'value',
            min: min_p,
            max: max_p
        },
        {
            name: 'Nagetive Statistic',
            nameLocation: 'start',
            min: min_n,
            max: max_n,
            alignTicks: true,
            type: 'value',
            inverse: inverse
        }
        ],
        series: [
        {
            name: 'Positive',
            type: 'line',
            areaStyle: {},
            lineStyle: {
            width: 1
            },
            emphasis: {
            focus: 'series'
            },
            markArea: {
            silent: true,
            itemStyle: {
                opacity: 0.3
            },
            },
            // prettier-ignore
            data: yaxis_p,
            color: "green"
        },
        {
            name: 'Negative',
            type: 'line',
            yAxisIndex: 1,
            areaStyle: {},
            lineStyle: {
            width: 1
            },
            emphasis: {
            focus: 'series'
            },
            markArea: {
            silent: true,
            itemStyle: {
                opacity: 0.3
            },
            },
            // prettier-ignore
            data: yaxis_n,
            color: "pink"
        }
        ]
    };

    return (
        <div width="700px" height="500px">
            <SelectTopic onTopicChange={setTopic}/>
            <SelectStats onStatsChange={setStats}/>
            <ReactEcharts style={{width: 700,height: 500}} option={option} />
        </div>
      ) 
}

export default Sentiment;