const errorMessage = document.getElementById("error-message");

document.getElementById("redirect-signin").addEventListener("click", () => {
    window.location.href = "/user/signin";
})

document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    // hide error message
    errorMessage.classList.add("hidden");
    errorMessage.classList.remove("block");

    const phoneNumber = document.getElementById("form-phone").value;
    const password = document.getElementById("form-password").value;

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            phone_number: phoneNumber,
            password : password,
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