const errorMessage = document.getElementById("error-message");
const passwordInput = document.getElementById("form-password");
const passwordReq = document.querySelector("#form-password + p");

passwordInput.addEventListener("input", e => {
    if(passwordInput.value.length < 8){
        passwordReq.style.color = "#f00";
    }else{
        passwordReq.style.color = "rgb(0, 255, 0)";
    }
})

document.getElementById("redirect-login").addEventListener("click", () => {
    window.location.href = "/user/login";
})

document.getElementById("signin-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("form-username").value;
    const phoneNumber = document.getElementById("form-phone").value;
    const password = passwordInput.value;

    const response = await fetch("/auth/signin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            username : username,
            phone_number: phoneNumber,
            password: password,
        })
    });

    const result = await response.json();
    if (!response.ok) {
        errorMessage.innerText = result.detail;
        errorMessage.classList.remove("hidden");
        errorMessage.classList.add("block");
        return;
    }

    window.location.href = `/u/${result["user_index"]}/`;
})