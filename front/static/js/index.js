const messagesChat = document.getElementById("messages-chat");
const btnAdd = document.getElementById("btn-add");
const btnSettings = document.getElementById("btn-settings");
const user = "Jack";
const messages = [
    {
        "user" : "Max",
        "content" : "Hi ! How are you all ?",
        "hour" : "16:08"
    },
    {
        "user" : "Max",
        "content" : "When will you be available ?",
        "hour" : "16:09"
    },
    {
        "user" : "Eve",
        "content" : "Oh Max it's been a long time ! I am in town for two days next week.",
        "hour" : "16:10"
    },
    {
        "user" : "Jack",
        "content" : "No way ! We will all be at the same place at the same time.",
        "hour" : "16:13"
    },
    {
        "user" : "Jack",
        "content" : "So coool!",
        "hour" : "16:13"
    },
    {
        "user" : "Max",
        "content" : "Eager to do it.",
        "hour" : "16:14"
    },
]

const chat = new Chat();

function initChat(initialMessages){
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

function updateChat(){

}

btnAdd.addEventListener("click", async () => {
    const match = window.location.pathname.match(/^\/u\/(\d+)(?:\/|$)/);
    if (!match) {
    throw new Error("User index introuvable");
    }
    const userIndex = match[1];
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
        const result = await response.json();
        return;
    }

    alert(response.body);

});

initChat(messages);