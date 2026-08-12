let deviceWidth = window.innerWidth;

function getUserIndex(){
    const match = window.location.pathname.match(/^\/u\/(\d+)(?:\/|$)/);
    if (!match) {
        throw new Error("User index introuvable");
    }
    return match[1];
}

window.addEventListener("resize", () => {
    deviceWidth = window.innerWidth;
});