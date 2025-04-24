import { useEffect, useState } from "react";
import axios from "axios";

function Test(){
    const [ram, setRam] = useState([])
    useEffect(() =>{
        axios.get('https://localhost:8080/ram')
        .then(ram => setRam(ram.data))
        .catch(err => console.log(err))
    }, [])

    return (
        <>
            {
            ram.map((information, index) => (
            <div key={index}>
                <p>{information}</p>
                <br></br>
            </div>
            ))
        }
        </>
    )
}

export default Test;