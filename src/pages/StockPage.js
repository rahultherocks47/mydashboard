import React,{useState,useEffect} from 'react'
import {useParams} from 'react-router-dom'

const StockPage = () => {    
    const symbolId = useParams().symbol
    const [stock, setStock] = useState(null)

    useEffect(() => {getStock()},[symbolId])

    let getStock = async () => {        
        const response = await fetch(`http://127.0.0.1:8000/api/stock/${symbolId}`)
        const data = await response.json()
        console.log(data)
        setStock(data)
    }
    

    return (
      <div>
        <div className='stock'>
      <div className='stock-header'>
        <h3>        
        STOCK NAME
        </h3>        
      </div>
      <div id="tvchart">{stock}</div></div>  
    </div>
    )
}

export default StockPage