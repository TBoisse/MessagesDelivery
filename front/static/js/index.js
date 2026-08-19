const messagesChat = document.getElementById("messages-chat");
const btnAdd = document.getElementById("btn-add");
const btnCreateChat = document.getElementById("btn-create-chat");
const btnSettings = document.getElementById("btn-settings");
const btnMessageSend = document.getElementById("btn-message-send");

function displayChat(messages){
    const chat = new Chat();
    let lastBlock = null;
    messages.forEach(message => {
        const createNewBlock = chat.appendSpread(message.user, message.content, message.hour);
        if(createNewBlock){
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
                    ${
                        (chat.isFirstMessageLastBlock() ? `<div class="w-full text-start font-bold text-white">
                            ${message.user}
                        </div>` : "")
                    }
                        <div class="w-full text-start text-white">
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

btnAdd.addEventListener("click", async () => {
    showPopup();
    showPopupType("popup-create-chat");
});

btnCreateChat.addEventListener("click", async () => {
    const userIndex = getUserIndex();
    const payload = {
        "chat_name" : document.getElementById("input-chat-name").value,
        "description" : document.getElementById("input-chat-description").value
    }
    const response = await fetch("/message/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-User-Index": userIndex
        },
        credentials: "same-origin",
        body: JSON.stringify(payload)
    });

    if (response.ok) {
        await buildChatList();
        hidePopup();
        hidePopupType("popup-create-chat");
        document.getElementById("input-chat-name").value = "";
        document.getElementById("input-chat-description").value = "";
        return;
    }
    
    alert(response.body);

});

btnMessageSend.addEventListener("click", async () => {
    let messageContent = document.getElementById("message-content").innerText.trim();
    if(messageContent.length == 0){
        return;
    }
    const userIndex = getUserIndex();
    const response = await fetch("/message/message", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-User-Index": userIndex
        },
        credentials: "same-origin",
        body: JSON.stringify({
            content : messageContent,
            chat_id : currentChatId
        })
    });

    if (response.ok) {
        document.getElementById("message-content").innerText = "";
        return;
    }

});

buildChatList();
buildPillsClick();