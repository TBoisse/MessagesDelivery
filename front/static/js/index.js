const pills = document.querySelector(".pill-containers").querySelectorAll("div");
const chats = document.querySelectorAll(".chat-containers > div");

const messagePlaceholder = document.getElementById("message-placeholder");
const messageContent = document.getElementById("message-content");

pills.forEach(pill => {
    pill.addEventListener("click", e => {
        pills.forEach(pill => {
            pill.classList.remove("active");
        });
        e.target.classList.add("active");
    })
})

chats.forEach(chat => {
    chat.querySelector("div").addEventListener("click", e => {
        chats.forEach(chat => {
            chat.querySelector("div").classList.remove("active");
        });
        e.target.classList.add("active");
    })
})

messageContent.addEventListener("input", () => {
    if(messageContent.innerHTML == "<br>"){
        messagePlaceholder.classList.remove("hidden");
    }else{
        messagePlaceholder.classList.add("hidden");
    }
})