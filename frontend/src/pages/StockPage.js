import React,{useState,useEffect,useRef} from 'react';
import { createChart,CrosshairMode } from 'lightweight-charts';
import 'react-date-range/dist/styles.css'; // main css file
import 'react-date-range/dist/theme/default.css'; // theme css file

import TextField from '@mui/material/TextField';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import MenuItem from '@mui/material/MenuItem';
import Select, { SelectChangeEvent } from '@mui/material/Select';



import "bootstrap/dist/css/bootstrap.min.css";
import './styles.css';


const StockPage = () => {
    //const symbolId = useParams().symbol;    
    const [fromDate, setFromDate] = useState(null);
    const [toDate, setToDate] = useState(null);
    const [symbolId, setSymbol] = useState("SBIN")
    const [stocks, setStocks] = useState([]);
    const chartContainerRef = useRef();
    const chart = useRef();
    const resizeObserver = useRef();
    const candleSeriesRef = useRef();
  
    let getStock = async () => {
      const response = await fetch(`/api/stock/NSE:${symbolId}-EQ`);
      const data = await response.json();      
      setStocks(data);     
      console.log(symbolId) 
    }    
    useEffect(() => {getStock()},[symbolId]);
    

    useEffect(() => {      
      chart.current = createChart(chartContainerRef.current, {
        width: chartContainerRef.current.clientWidth,
        height: 300,        
        layout: {
          backgroundColor: '#253248',
          textColor: 'rgba(255, 255, 255, 0.9)',
        },
        grid: {
          vertLines: {
            color: '#334158',
          },
          horzLines: {
            color: '#334158',
          },
        },
        crosshair: {
          mode: CrosshairMode.Normal,
        },
        priceScale: {
          borderColor: '#485c7b',
        },
        timeScale: {
          borderColor: '#485c7b',
        },        
      });  
      candleSeriesRef.current = chart.current.addCandlestickSeries({
        upColor: '#4bffb5',
        downColor: '#ff4976',
        borderDownColor: '#ff4976',
        borderUpColor: '#4bffb5',
        wickDownColor: '#838ca1',
        wickUpColor: '#838ca1',
      });   
  
      // const volumeSeries = chart.current.addHistogramSeries({
      //   color: '#182233',
      //   lineWidth: 2,
      //   priceFormat: {
      //     type: 'volume',
      //   },
      //   overlay: true,
      //   scaleMargins: {
      //     top: 0.8,
      //     bottom: 0,
      //   },
      // });
  
      // volumeSeries.setData(volumeData);
    }, []);

    useEffect(() => {      
      
      console.log("Chart",stocks)   
      candleSeriesRef.current.setData(stocks);

    },[stocks])

    function handleSelect(){console.log("Date Found!")}         
    
    // const render = stocks.map((item,index) => {return <p key={index}> {item.time}, {item.high}, {item.low}</p>;});

    // Resize chart on container resizes.
    useEffect(() => {
    resizeObserver.current = new ResizeObserver(entries => {
      const { width, height } = entries[0].contentRect;
      chart.current.applyOptions({ width, height });
      setTimeout(() => {
        chart.current.timeScale().fitContent();
      }, 0);
    });

    resizeObserver.current.observe(chartContainerRef.current);

    return () => resizeObserver.current.disconnect();
    }, []);

      
    return (  
      <div>        
        <div className='stock'>
      <div className='stock-header'>
        {/* <h3>{symbolId}</h3>
        <input type="date"  name="from"/>
        <input type="date"  name="to"/>
        <select onChange={(e)=> {setSymbol(e.target.value)}}>
        <option value="TCS">TCS</option>
        <option value="SBIN">SBIN</option>
        </select> */}
        <Box sx={{ minWidth: 120 }}>
        <Select
          labelId="demo-simple-select-label"
          id="symbol"          
          label="Symbol"
          value={symbolId}
          onChange={(e)=> {setSymbol(e.target.value)}}          
        >
          <MenuItem value="SBIN">SBI</MenuItem>
          <MenuItem value="TCS">TCS</MenuItem>
          <MenuItem value="WIPRO">WIPRO</MenuItem>
        </Select>
      <LocalizationProvider dateAdapter={AdapterDateFns}>
      <DatePicker
        label="From"
        value={fromDate}
        onChange={(newValue) => {
          setFromDate(newValue);
          console.log(fromDate);
        }}
        renderInput={(params) => <TextField {...params} />}
      />
      <DatePicker
        label="To"
        value={toDate}
        onChange={(newValue) => {
          setToDate(newValue);
        }}
        renderInput={(params) => <TextField {...params} />}
      />
    </LocalizationProvider>
    <Select
          labelId="demo-simple-select-label"
          id="interval"          
          label="Symbol"
          value="D"          
        >
          <MenuItem value="D">DAILY</MenuItem>
          <MenuItem value="W">WEEKLY</MenuItem>          
        </Select>
    <Button variant="contained">Submit</Button>
    </Box>
      </div> 
      </div> 
      <div className="AppBox">
        <div ref={chartContainerRef} className="chart-container" />
        </div>           
    </div>
    )
}

export default StockPage