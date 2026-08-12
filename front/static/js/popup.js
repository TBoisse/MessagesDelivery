const popUp = document.getElementById("popup");
const popupCloseBtns = document.querySelectorAll(".popup-close-button");
const btnChatDelete = document.getElementById("btn-chat-delete");
const chatSettings = document.getElementById("chat-settings");

function hidePopup(){
    popUp.classList.remove("flex");
    popUp.classList.add("hidden");
}

function showPopup(){
    popUp.classList.add("flex");
    popUp.classList.remove("hidden");
}

function showPopupType(type){
    document.getElementById(type).classList.add("flex");
    document.getElementById(type).classList.remove("hidden");
}

function hidePopupType(type){
    document.getElementById(type).classList.remove("flex");
    document.getElementById(type).classList.add("hidden");
}

chatSettings.addEventListener("click", () => {
    showPopup();
    showPopupType("popup-settings-chat");
})


popUp.addEventListener("click", e => {
    if(e.target != popUp){
        return;
    }
    hidePopup();
    Array.from(popUp.children).forEach(child => {
        hidePopupType(child.id);
    });
})

popupCloseBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        hidePopup();
        hidePopupType(btn.parentElement.id);
    })
})

btnChatDelete.addEventListener("click", async () => {
    const userIndex = getUserIndex();
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
        if(deviceWidth < 768){
            sideBar.classList.remove("hidden");
            sideBar.classList.add("flex");
            messageContainers.classList.remove("flex")
            messageContainers.classList.add("hidden");
        }else{
            messageContainers.classList.remove("flex")
            messageContainers.classList.add("hidden");
            ghostMessageContainers.classList.remove("md:hidden");
            ghostMessageContainers.classList.add("md:flex");
        }
        await updateChatList();
        hidePopup();
        currentChatId = "";
        return;
    }

    alert(response.body);
})