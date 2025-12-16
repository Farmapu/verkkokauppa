import React, {useState} from "react";
import './Chatbot.css';
import {useRef} from "react";

const answer = {result: "default"};

const Chatbot = () => {
    const inputRef = useRef(null);
    const [answers, setAnswer] = useState([]);
    const [isDisabled, setIsDisabled] = useState(false);

    async function chat(question) {
        setIsDisabled(!isDisabled);
        addQuestion(question);
        try{
            const response = await fetch('http://localhost:8080/chatbot?message=' + question);
            if(!response.ok) {
                setIsDisabled(isDisabled);
                throw new Error(response.status);
            } else {
                setIsDisabled(isDisabled);
                const result = await response.json();
                console.log(result);
                addAnswer(result.result);
            }
        } catch (error) {
            console.error(error.message);
        }
    }

    function addQuestion(question){
        setAnswer(a => [...a, question]);
    }

    function addAnswer(answer){
        setAnswer(a => [...a, answer]);
    }

    function removeAnswer(index){
        setAnswer(answers.filter((_, i) => i !== index));
    }

    return(
        <div className='chatbot'>
            <div className='chatbotTextbox'>
                <ul>
                    {answers.map((answer, index) => <li key={index}>{answer}</li>)}
                </ul>
            </div>
            <form className="textbox" onSubmit={(e) => {
                e.preventDefault();
                console.log(chat(inputRef.current?.value));
                document.getElementById("chatbotti").value = "";
            }}>
                <input className="text" id="chatbotti" ref={inputRef} type="text" name="test" />
                <button disabled={isDisabled} type="submit">Kysy chatbotilta</button>
            </form>
        </div>
    )
}

export default Chatbot