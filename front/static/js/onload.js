const messagePlaceholder = document.getElementById("message-placeholder");
const messageContent = document.getElementById("message-content");
const backButton = document.getElementById("back-button");

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

backButton.addEventListener("click", () => {
    sideBar.classList.remove("hidden");
    sideBar.classList.add("flex");
    messageContainers.classList.remove("flex")
    messageContainers.classList.add("hidden");
})