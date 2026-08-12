const popUp = document.getElementById("popup");
const popupCloseBtn = document.getElementById("popup-close-button");
const btnChatDelete = document.getElementById("btn-chat-delete");

function hidePopup(){
    popUp.classList.remove("flex");
    popUp.classList.add("hidden");
}

function showPopup(){
    popUp.classList.add("flex");
    popUp.classList.remove("hidden");
}

document.getElementById("chat-settings").addEventListener("click", () => {
    showPopup();
})


popUp.addEventListener("click", e => {
    if(e.target != popUp){
        return;
    }
    hidePopup();
})

popupCloseBtn.addEventListener("click", () => {
    hidePopup();
})

btnChatDelete.addEventListener("click", async () => {
    const userIndex = getUserIndex();
    console.log(currentChatId);
    const response = await fetch("/message/chat", {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "X-User-Index": userIndex
        },
        credentials: "same-origin",
        body: JSON.stringify({
            chat_id : currentChatId
        })
    });

    if (response.ok) {
        await updateChatList();
        hidePopup();
        currentChatId = "";
        return;
    }

    alert(response.body);
})