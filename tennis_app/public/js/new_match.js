function matchFields() {
    if (document.getElementById("name-p1").value ===
        document.getElementById("name-p2").value) {
            alert("Player names must be different!");
            return false;
    } else {
        return true;
    }
}
