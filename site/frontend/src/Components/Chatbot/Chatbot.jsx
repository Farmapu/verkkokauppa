import React from "react";
import { useState } from "react";
import './Chatbot.css';
import {useRef} from "react";

function chat(question) {
    var response = fetch('http://localhost:8080/chatbot?message=' + question);
    return response;
}

const Chatbot = () => {
    const inputRef = useRef(null);    
    return(
        <div className='Chatbot'>
            <form onSubmit={(e) => {
                e.preventDefault();
                console.log(chat(inputRef.current?.value));
            }}>
                <input ref={inputRef} type="text" name="test" />
                <button type="submit">Test</button>
            </form>
            
            {/* <button onClick={() => chat('Moi, mikä on RAM?')}></button> */}
        </div>
    )
}

export default Chatbot