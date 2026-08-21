const btnAdd = document.getElementById("btn-add");
const btnCreateChat = document.getElementById("btn-create-chat");
const btnSettings = document.getElementById("btn-settings");
const btnMessageSend = document.getElementById("btn-message-send");
const btnAddMember = document.getElementById("btn-add-member");

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

btnAddMember.addEventListener("click", async () => {
    const contactPhone = document.getElementById("add-member").value;
    const userIndex = getUserIndex();
    const response = await fetch("/message/chat/members", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-User-Index": userIndex
        },
        credentials: "same-origin",
        body: JSON.stringify({
            chat_id : currentChatId,
            contact_phone : contactPhone
        })
    });
})

buildChatList();
buildPillsClick();