const inputUsername = document.getElementById("input-username");
const inputPhone = document.getElementById("input-phone");
const iconUser = document.getElementById("icon-user");

document.getElementById("btn-homepage").addEventListener("click", () => {
    const userIndex = getUserIndex();
    window.location.href = `/u/${userIndex}/`;
})

window.addEventListener("load",async () => {
    const userIndex = getUserIndex();
    const response = await fetch("/auth/me/user", {
        method: "GET",
        headers: {
            "X-User-Index": userIndex
        },
        credentials: "same-origin"
    });

    const result = await response.json();
    if(!response.ok){
        alert(response.status, result.detail);
        // window.location.href = `/u/${userIndex}/`;
        return
    }

    inputUsername.value = result.username;
    inputPhone.value = result.phone_number;
    iconUser.src = result.url;
})