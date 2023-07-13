import React, { useRef, useEffect, useState } from 'react';
import BASE_URL from './config';
import mapboxgl from 'mapbox-gl';
import SelectYear from './SelectYear';
import 'mapbox-gl/dist/mapbox-gl.css';
import '../App.css';

mapboxgl.accessToken =
  'pk.eyJ1IjoiY2VsZXN0ZTEyMyIsImEiOiJjbGhmNXlnMXQwMHhoM2VtcWhwMGVoeGNvIn0.jAcXS46hEOeykQWkr8994Q';

const MyMap = () => {

  const [year, setYear] = React.useState("-");
  const [liquor, setLiquor] = useState(null)
  // const [geo1, setGeo1] = useState(null)
  // const [geo2, setGeo2] = useState(null)
  const [crash, setCrash] = useState(null)
  const mapContainer = useRef(null);

  const [map, setMap] = useState(null);
  const [isDataSourceAdded, setIsDataSourceAdded] = useState(false);
  const [isLayerVisible, setIsLayerVisible] = useState(true);
  const [isLayerVisible2, setIsLayerVisible2] = useState(true);



  let headers = new Headers();
  headers.append('Access-Control-Allow-Origin', 'http://localhost:3000');
  headers.append('Content-Type', 'application/json');
  headers.append('Accept', 'application/json');

  
  // React.useEffect(() => {
  //   if (year === '2017') {
  //     fetch2017Liquor();
  //     fetch2017Crash();
  //   } else if (year === '2018') {
  //     fetch2018Liquor();
  //     fetch2018Crash();
  //   } else if (year === '2019') {
  //     fetch2019Liquor();
  //     fetch2019Crash();
  //   }
  // }, [year]);


  const fetch2017Liquor = async () => {
    const response = await fetch(BASE_URL + "liquor_data/view/map/2017LiquorLicence", {method:"GET", headers:headers});
    const data = await response.json();
    var geo1 = [];
    data.forEach(function(d) {
      // geo1.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+d.value[0]+']}}'));
      geo1.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+d.value[0]+']},"properties": {"key":"'+d.key+'"}}'));
      });
    if (geo1.length !== 0) {
      setLiquor(geo1);
      setIsDataSourceAdded(false);
    }else{
      console.log("no data");
    }
  };

  const fetch2017Crash = async () => {
    const response2 = await fetch(BASE_URL + "crash_data/view/map/2017Crash", {method:"GET", headers:headers});
    const data2 = await response2.json();
    var geo2 = [];
    data2.forEach(function(d) {
      geo2.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+ d.value[0]+']}}'));
    });
    if (geo2.length !== 0){
    setCrash(geo2)
    setIsDataSourceAdded(false);
    }else{
      console.log("no data");
    }
  };

  
  const fetch2018Liquor = async () => {
    const response = await fetch(BASE_URL + "liquor_data/view/map/2018LiquorLicence", {method:"GET", headers:headers});
    const data = await response.json();
    var geo1 = [];
    data.forEach(function(d) {
      geo1.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+d.value[0]+']},"properties": {"key":"'+d.key+'"}}'));
      });
    if (geo1.length !== 0) {
      setLiquor(geo1);
      setIsDataSourceAdded(false);
    }else{
      console.log("no data");
    }
  };

  const fetch2018Crash = async () => {
    const response2 = await fetch(BASE_URL + "crash_data/view/map/2018Crash", {method:"GET", headers:headers});
    const data2 = await response2.json();
    var geo2 = [];
    data2.forEach(function(d) {
      geo2.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+ d.value[0]+']}}'));
    });
    if (geo2.length !== 0){
    setCrash(geo2)
    setIsDataSourceAdded(false);
    }else{
      console.log("no data");
    }
  };

  const fetch2019Liquor = async () => {
    const response = await fetch(BASE_URL + "liquor_data/view/map/2019LiquorLicence", {method:"GET", headers:headers});
    const data = await response.json();
    var geo1 = [];
    data.forEach(function(d) {
      geo1.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+d.value[0]+']},"properties": {"key":"'+d.key+'"}}'));
      });
    if (geo1.length !== 0) {
      setLiquor(geo1);
      setIsDataSourceAdded(false);
    }else{
      console.log("no data");
    }
  };

  const fetch2019Crash = async () => {
    const response2 = await fetch(BASE_URL + "crash_data/view/map/2019Crash", {method:"GET", headers:headers});
    const data2 = await response2.json();
    var geo2 = [];
    data2.forEach(function(d) {
      geo2.push(JSON.parse('{"type": "Feature", "geometry": {"type": "Point", "coordinates": ['+d.value[1]+','+ d.value[0]+']}}'));
    });
    if (geo2.length !== 0){
    setCrash(geo2)
    setIsDataSourceAdded(false);
    }else{
      console.log("no data");
    }
  };



  useEffect(() => {

    const map = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/light-v9',
      center: [144.9628854, -37.826985],
      zoom: 5
    });
    setMap(map)


    return () => {
      map.remove();
    };

  },[]);

  React.useEffect(() => {
    if (year === '2017') {
      fetch2017Liquor();
      fetch2017Crash();
    } else if (year === '2018') {
      fetch2018Liquor();
      fetch2018Crash();
    } else if (year === '2019') {
      fetch2019Liquor();
      fetch2019Crash();
    }
  }, [year]);

  // useEffect(() => {
  //   fetch2017Liquor();
  //   fetch2017Crash();
  // });

  useEffect(() => {
    if (map && liquor && crash && !isDataSourceAdded &!map.getSource('Crush')) {
      // if (map.getSource("CrushLayer")) {
      //   map.removeLayer("Crush");
      //   map.removeSource("CrushLayer");
      // }
      // if (map.getSource("LiquorLayer")) {
      //   map.removeLayer("Liquor");
      //   map.removeSource("LiquorLayer");
      //   map.removeLayer("cluster-count");
      // }
        map.addSource('Crush', {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: crash,
          }
        });

        map.addLayer(
          {
            id: 'CrushLayer',
            type: 'heatmap',
            source: 'Crush',
            paint: {
              'heatmap-opacity': 0.5,
          //     'heatmap-weight': [
          //   'interpolate',
          //   ['linear'],
          //   ['get', 'mag'],
          //   0,
          //   0,
          //   6,
          //   1,
          // ],
          // // Increase the heatmap color weight weight by zoom level
          // // heatmap-intensity is a multiplier on top of heatmap-weight
          // 'heatmap-intensity': [
          //   'interpolate',
          //   ['linear'],
          //   ['zoom'],
          //   0,
          //   1,
          //   9,
          //   3,
          // ],
         
          // 'heatmap-color': [
          //   'interpolate',
          //   ['linear'],
          //   ['heatmap-density'],
          //   0,
          //   'rgba(236, 231, 242,0)',
          //   0.2,
          //   'rgb(217, 217, 217)',
          //   0.4,
          //   'rgb(189, 189, 189)',
          //   0.6,
          //   'rgb(150, 150, 150)',
          //   0.8,
          //   'rgb(115, 115, 115)',
          //   1,
          //   'rgb(82, 82, 82)',
          // ],
            },
            layout: {
              visibility: 'visible'
            },
          }
        );

        map.addSource('Liquor', {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: liquor,
          },
          cluster: true,
          clusterMinPoints:100
        });

        map.addLayer(
            {
              id: 'LiquorLayer',
              type: 'circle',
              source: 'Liquor',
              paint: {
                'circle-radius': 3,
                'circle-color':'rgba(55,148,179,1)',
                'circle-opacity': 0.6,
                'circle-radius': 
                [
                  'step',
                  ['get', 'point_count'],
                  20,
                  100,
                  30,
                  750,
                  40
                ] 
              },
              layout: {
                visibility: 'visible'
              },
            }
        );

        map.addLayer({
          id: 'cluster-count',
          type: 'symbol',
          source: 'Liquor',
          filter: ['has', 'point_count'],
          layout: {
              'text-field': '{point_count}',
              'text-font': ['Arial Unicode MS Bold'],
              'text-size': 12
          }
        });

        const popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false,
        });
  
        map.on('mouseenter', 'LiquorLayer', (e) => {
          map.getCanvas().style.cursor = 'pointer';
  
          const coordinates = e.features[0].geometry.coordinates.slice();
          console.log(coordinates);
          const name = e.features[0].properties.key;
          console.log(name);
          popup.setLngLat(coordinates).setHTML(name).addTo(map);
          
        });
  
        map.on('mouseleave', 'LiquorLayer', () => {
          map.getCanvas().style.cursor = '';
          popup.remove();
        });


        setIsDataSourceAdded(true);
    }else if (map && liquor && crash && isDataSourceAdded) {
      return;
    }
  }, [map, year, liquor, crash ,isDataSourceAdded]);


  const toggleLayerVisibility = () => {
    setIsLayerVisible(!isLayerVisible);
    if (isLayerVisible) {
      map.setLayoutProperty('LiquorLayer', 'visibility', 'none');
      map.setLayoutProperty('cluster-count', 'visibility', 'none');
    } else {
      map.setLayoutProperty('LiquorLayer', 'visibility', 'visible');
      map.setLayoutProperty('cluster-count', 'visibility', 'visible');
    }
  };

  const toggleLayerVisibility2 = () => {
    setIsLayerVisible2(!isLayerVisible2);
    if (isLayerVisible2) {
      map.setLayoutProperty('CrushLayer', 'visibility', 'none');
    } else {
      map.setLayoutProperty('CrushLayer', 'visibility', 'visible');
    }
  };
  
  return (
    <div>
      <div style={{ display: 'flex',justifyContent: 'flex-start' }}>
        <SelectYear onYearChange={setYear} />
        <button className='button1' onClick={toggleLayerVisibility}>
          {isLayerVisible ? 'Hide Liquor Point' : 'Show Liquor Point'}
        </button>
        <button className='button1' onClick={toggleLayerVisibility2}>
          {isLayerVisible2 ? 'Hide Crush Heatmap' : 'Show Crush Heatmap'}
        </button>
      </div>

      <div ref={mapContainer} className='map-container' />
    </div>
  );

};

export default MyMap;