document.getElementById("signin-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const username = document.getElementById("form-username").value;
    const phoneNumber = document.getElementById("form-phone").value;
    const email = document.getElementById("form-email").value;

    const response = await fetch("/auth/signin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        credentials: "same-origin",
        body: JSON.stringify({
            username : username,
            phone_number: phoneNumber,
            email: email,
        })
    });

    if (response.ok) {
        window.location.href = "/";
        return;
    }

    alert(response.body);
})