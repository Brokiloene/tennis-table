document.addEventListener("DOMContentLoaded", () => {
    let curURL = new URL(window.location.href);
    playerName = curURL.searchParams.get('filter_by_player_name');
    console.log(playerName)
    if (playerName) {
        curURL.searchParams.set("filter_by_player_name", playerName);
    } else {
        curURL.searchParams.delete("filter_by_player_name");
    }

    let prev_btn = document.getElementById("prev-page-btn")
    prev_btn.addEventListener('click', () => {
        let prev_page = prev_btn.value;
        curURL.searchParams.set('page', prev_page)
        window.location.href = curURL;
    });

    let next_btn = document.getElementById("next-page-btn")
    next_btn.addEventListener('click', () => {
        let next_page = next_btn.value;
        curURL.searchParams.set('page', next_page)
        window.location.href = curURL;
    });
});