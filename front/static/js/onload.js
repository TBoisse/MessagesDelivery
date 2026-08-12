const sideBar = document.getElementById("side-bar");
const messagePlaceholder = document.getElementById("message-placeholder");
const messageContent = document.getElementById("message-content");
const chatContainers = document.querySelector(".chat-containers");
const messageContainers = document.querySelector(".messages-container");
const ghostMessageContainers = document.querySelector(".messages-container-ghost");
const backButton = document.getElementById("back-button");

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
            if(e.target.classList.contains("active")){
                e.target.classList.remove("active");
                currentChatId = "";
                messageContainers.classList.remove("flex");
                messageContainers.classList.add("hidden");
                if(deviceWidth < 768){
                    sideBar.classList.remove("hidden");
                    sideBar.classList.add("flex");
                }else{
                    ghostMessageContainers.classList.add("md:flex");
                    ghostMessageContainers.classList.remove("md:hidden");
                }
            }else{
                document.getElementById("chat-window-title").innerText = e.target.querySelector(".chat-title").innerText;
                chats.forEach(chat => {
                    chat.querySelector("div").classList.remove("active");
                });
                e.target.classList.add("active");
                currentChatId = chat.dataset.chatId;
                messageContainers.classList.add("flex");
                messageContainers.classList.remove("hidden");
                if(deviceWidth < 768){
                    sideBar.classList.add("hidden");
                    sideBar.classList.remove("flex");
                }else{
                    ghostMessageContainers.classList.remove("md:flex");
                    ghostMessageContainers.classList.add("md:hidden");
                }
            }
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
                    <p class="chat-title">${chat.chat_name}</p>
                </div>
                <div>0</div>
            </div>
        `;
        chatContainers.appendChild(chatDiv);
    });
    buildChatsClick();
}

backButton.addEventListener("click", () => {
    sideBar.classList.remove("hidden");
    sideBar.classList.add("flex");
    messageContainers.classList.remove("flex")
    messageContainers.classList.add("hidden");
})