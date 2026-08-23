const inputUsername = document.getElementById("input-username");
const inputPhone = document.getElementById("input-phone");

document.getElementById("btn-homepage").addEventListener("click", () => {
    const userIndex = getUserIndex();
    window.location.href = `/u/${userIndex}`;
})

window.addEventListener("load",async () => {
    const userIndex = getUserIndex();
    const response = await fetch("/users/me", {
        method: "GET",
        headers: {
            "X-User-Index": userIndex
        },
        credentials: "same-origin"
    });

    if(!response.ok){
        alert(response.status);
        // window.location.href = `/u/${userIndex}`;
        return
    }

    const result = await response.json();
    inputUsername.value = result.username;
    inputPhone.value = result.phone_number;
})