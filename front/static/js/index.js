const pills = document.querySelector(".pill-containers").querySelectorAll("div");
const chats = document.querySelectorAll(".chat-containers > div");

pills.forEach(pill => {
    pill.addEventListener("click", e => {
        pills.forEach(pill => {
            pill.classList.remove("active");
        });
        e.target.classList.add("active");
    })
})

chats.forEach(chat => {
    console.log(chat)
    chat.querySelector("div").addEventListener("click", e => {
        chats.forEach(chat => {
            chat.querySelector("div").classList.remove("active");
        });
        e.target.classList.add("active");
    })
})