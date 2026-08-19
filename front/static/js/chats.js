const chatContainers = document.querySelector(".chat-containers");
const messagesChat = document.getElementById("messages-chat");
let chatList = [];

async function buildChatList() {
    const userIndex = getUserIndex();
    const response = await fetch("/message/chat", {
        method: "GET",
        headers: {
            "X-User-Index": userIndex
        },
        credentials: "same-origin"
    });
    if (!response.ok) {
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
    chatsOnClickSet();
}

function displayChat(messages) {
    const chat = new Chat();
    messagesChat.innerHTML = "";
    let lastBlock = null;
    messages.forEach(message => {
        const createNewBlock = chat.appendSpread(message.user, message.content, message.hour);
        if (createNewBlock) {
            lastBlock = document.createElement("div");
            lastBlock.innerHTML = `
                <div class="absolute h-full ${(message.is_user) ? "right-3" : "left-3"} top-2">
                    <img class="w-5" src="/static/image/letters/letter-a.svg" alt="user icon">
                </div>
            `;
            messagesChat.appendChild(lastBlock);
        }
        const messageDiv = document.createElement("div");
        messageDiv.className = "pb-0.5";
        messageDiv.innerHTML = `
            <div class="flex ${(message.is_user) ? "justify-end" : "justify-start"} px-10">
                <div class="relative ${(message.is_user) ? "bg-guideline-4" : "bg-guideline-6"} max-w-[90%] sm:max-w-[80%] lg:max-w-[70%] rounded-lg">
                    <div class="flex flex-col items-center p-2">
                    ${(chat.isFirstMessageLastBlock() ? `<div class="w-full text-start font-bold text-white">
                            ${message.user}
                        </div>` : "")
            }
                        <div class="w-full text-start text-white break-words">
                            ${message.content}
                        </div>
                        <div class="w-full text-end text-white text-xs">
                            ${message.hour}
                        </div>
                    </div>
                <div>
            </div>
        `;
        lastBlock.appendChild(messageDiv);
    });
    messagesChat.scrollTop = messagesChat.scrollHeight;
}

function chatsOnClickSet() {
    chatsList = document.querySelectorAll(".chat-containers > div");
    chatsList.forEach(chat => {
        chat.querySelector("div").addEventListener("click", async e => {
            if(e.target.classList.contains("active")) {  // needed to post messages
                currentChatId = "";
            } else {
                currentChatId = chat.dataset.chatId;
            }
            handleScreenWidth(e.target);
            const userIndex = getUserIndex();
            const response = await fetch(`/message/message/${chat.dataset.chatId}`, {
                method: "GET",
                headers: {
                    "X-User-Index": userIndex
                },
                credentials: "same-origin"
            });
            if (!response.ok) {
                alert(response.body);
                return;
            }
            messages = await response.json();
            displayChat(messages);
        })
    })
}