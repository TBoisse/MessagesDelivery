const messagePlaceholder = document.getElementById("message-placeholder");
const messageContent = document.getElementById("message-content");
const chatContainers = document.querySelector(".chat-containers");

let chatList = [];
let currentChatId = "";

messageContent.addEventListener("input", () => {
    if(messageContent.innerHTML == "<br>"){
        messagePlaceholder.classList.remove("hidden");
    }else{
        messagePlaceholder.classList.add("hidden");
    }
})

function buildPillsClick(){
    const pills = document.querySelector(".pill-containers").querySelectorAll("div");
    pills.forEach(pill => {
        pill.addEventListener("click", e => {
            pills.forEach(pill => {
                pill.classList.remove("active");
            });
            e.target.classList.add("active");
        })
    })
}

function buildChatsClick(){
    const chats = document.querySelectorAll(".chat-containers > div");
    chats.forEach(chat => {
        chat.querySelector("div").addEventListener("click", e => {
            chats.forEach(chat => {
                chat.querySelector("div").classList.remove("active");
            });
            e.target.classList.add("active");
            currentChatId = chat.dataset.chatId;
        })
    })
}

async function updateChatList(){
    const userIndex = getUserIndex();
    const response = await fetch("/message/chat", {
        method: "GET",
        headers: {
            "X-User-Index": userIndex
        },
        credentials: "same-origin"
    });
    if(! response.ok){
        alert(response.body);
        return;
    }
    chatList = await response.json();
    chatContainers.innerHTML = "";
    chatList.forEach(chat => {
        const chatDiv = document.createElement("div");
        chatDiv.dataset.chatId = chat.chat_id;
        chatDiv.innerHTML = `
            <div>
                <div>
                    <img class="w-10" src="/static/image/letters/letter-a.svg" alt="chat icon">
                    <p>${chat.chat_name}</p>
                </div>
                <div>0</div>
            </div>
        `;
        chatContainers.appendChild(chatDiv);
    });
    buildChatsClick();
}