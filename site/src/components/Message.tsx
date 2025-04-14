function Message(){
    const text = 'tekstiä';
    if(text){
        return <p>{text}</p>
    }
    return <p>Hello</p>
}

export default Message;