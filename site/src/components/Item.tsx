import axios from 'axios';
import React, { useEffect, useState } from 'react'

function DisplayItem()
{
        const [count, setCount] = useState(0);
        const [array, setArray] = useState([]);
        
        async function fetchAPI() {
          try {
            const response = await axios.get('http://localhost:8080/api');
            setArray(response.data.trees);
            console.log(response.data.trees);
          }
          catch (error) {
            console.error('Error fetching fruits', error);
          }
        }

        useEffect(() => {
          fetchAPI();
        }, []);

    return (
        <>
            {
            array.map((information, index) => (
            <div key={index}>
                <p>{information}</p>
            </div>
            ))
            }
        </>
    )
}

export default DisplayItem;