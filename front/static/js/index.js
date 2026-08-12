const messagesChat = document.getElementById("messages-chat");
const btnAdd = document.getElementById("btn-add");
const btnSettings = document.getElementById("btn-settings");

// const chat = new Chat();

function initChat(initialMessages, user){
    let lastBlock = null;
    messages.forEach(message => {
        const createNewBlock = chat.appendSpread(message.user, message.content, message.hour);
        const isUser = message.user == user;
        if(createNewBlock){
            lastBlock = document.createElement("div");
            lastBlock.innerHTML = `
                <div class="absolute h-full ${(isUser) ? "right-3" : "left-3"} top-2">
                    <img class="w-5" src="/static/image/letters/letter-a.svg" alt="user icon">
                </div>
            `;
            messagesChat.appendChild(lastBlock);
        }
        const messageDiv = document.createElement("div");
        messageDiv.className = "pb-0.5";
        messageDiv.innerHTML = `
            <div class="flex ${(isUser) ? "justify-end" : "justify-start"} px-10">
                <div class="relative ${(isUser) ? "bg-guideline-4" : "bg-guideline-6"} max-w-[90%] sm:max-w-[80%] lg:max-w-[70%] rounded-lg">
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
    const userIndex = getUserIndex();
    const payload = {
        "chat_name" : "Wow !",
        "description" : "Test ?"
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
        await updateChatList();
        return;
    }

    alert(response.body);

});

updateChatList();
buildPillsClick();