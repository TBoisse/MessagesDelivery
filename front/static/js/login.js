document.getElementById("login-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("form-username").value;
    const phoneNumber = document.getElementById("form-phone").value;

    const response = await fetch("/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            username : username,
            phone_number: phoneNumber,
        })
    });

    if (response.ok) {
        const result = await response.json();
        window.location.href = `/u/${result["user_index"]}/`;
        return;
    }

    alert(response.body);
})