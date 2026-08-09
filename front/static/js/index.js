const pills = document.querySelector(".pill-containers").querySelectorAll("div");

pills.forEach(pill => {
    pill.addEventListener("click", e => {
        pills.forEach(pill => {
            pill.classList.remove("active");
        });
        e.target.classList.add("active");
    })
})