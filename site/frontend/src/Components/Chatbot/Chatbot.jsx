import React, {useState} from "react";
import './Chatbot.css';
import {useRef} from "react";

const Chatbot = () => {
    const inputRef = useRef(null);
    const [answers, setAnswer] = useState([]);

    function chat(question) {
        var answer
        fetch('http://localhost:8080/chatbot?message=' + question)
        .then(res => res.json())
        .then(data => answer = data)
        //.then(data => console.log(data));
        return answer;
    }

    function addAnswer(question){
        var response = chat(question);
        setAnswer(a => [...a, question]);
        console.log(answers)
    }

    function removeAnswer(index){
        setAnswer(answers.filter((_, i) => i !== index));
    }

    return(
        <div className='chatbot'>
            <ul>
                {answers.map((answer, index) => <li key={index}>{answer}</li>)}
            </ul>
            <form className="textbox" onSubmit={(e) => {
                e.preventDefault();
                console.log(chat(inputRef.current?.value));
                document.getElementById("chatbotti").value = "";
            }}>
                <input className="text" id="chatbotti" ref={inputRef} type="text" name="test" />
                <button type="submit">Test</button>
            </form>
            
            {/* <button onClick={() => chat('Moi, mikä on RAM?')}></button> */}
        </div>
    )
}

export default Chatbot