const sideBar = document.getElementById("side-bar");
const messageContainers = document.querySelector(".messages-container");
const ghostMessageContainers = document.querySelector(".messages-container-ghost");
let chatsList = [];
let deviceWidth = window.innerWidth;

function getUserIndex() {
    const match = window.location.pathname.match(/^\/u\/(\d+)(?:\/|$)/);
    if (!match) {
        throw new Error("User index introuvable");
    }
    return match[1];
}

function handleScreenWidth(chat) {
    if (chat.classList.contains("active")) {
        chat.classList.remove("active");
        messageContainers.classList.remove("flex");
        messageContainers.classList.add("hidden");
        if (deviceWidth < 768) {
            sideBar.classList.remove("hidden");
            sideBar.classList.add("flex");
        } else {
            ghostMessageContainers.classList.add("md:flex");
            ghostMessageContainers.classList.remove("md:hidden");
        }
    } else {
        document.getElementById("chat-window-title").innerText = chat.querySelector(".chat-title").innerText;
        chatsList.forEach(chat => {
            chat.querySelector("div").classList.remove("active");
        });
        chat.classList.add("active");
        messageContainers.classList.add("flex");
        messageContainers.classList.remove("hidden");
        if (deviceWidth < 768) {
            sideBar.classList.add("hidden");
            sideBar.classList.remove("flex");
        } else {
            ghostMessageContainers.classList.remove("md:flex");
            ghostMessageContainers.classList.add("md:hidden");
        }
    }
}

window.addEventListener("resize", () => {
    deviceWidth = window.innerWidth;
});