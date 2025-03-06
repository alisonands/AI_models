
function checkPassword() {
    var password = prompt("Enter the password:");
    if (password === "secret123") {
        document.getElementById("protected-content").style.display = "block";
        document.getElementById("login").style.display = "none";
    } else {
        alert("Incorrect password!");
    }
}
