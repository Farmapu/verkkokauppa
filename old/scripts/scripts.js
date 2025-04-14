document.getElementById("chatbotButton").addEventListener("click", function() {
    document.getElementById("chatbotWindow").style.visibility = "visible";
    document.getElementById("chatbotButton").style.visibility = "hidden";
});

document.getElementById("closechatbot").addEventListener("click", function() {
    document.getElementById("chatbotWindow").style.visibility = "hidden";
    document.getElementById("chatbotButton").style.visibility = "visible";
});