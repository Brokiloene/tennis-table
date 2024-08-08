document.addEventListener("DOMContentLoaded", () => {
   const buttons = [
    document.querySelectorAll(".table-btn"),
    document.querySelectorAll(".page-nav-btn"),
    document.querySelectorAll(".search-btn")
   ];

   const tableButtonsAudio = new Audio("table-btn.mp3")
   const pageNavButtonsAudio = new Audio("page-nav-btn.mp3")
   const searchButtonsAudio = new Audio("search-btn.mp3")


   buttons.forEach((btns) => {
        btns.forEach(btn => {
            console.log(btn);
            let audio = null;
            if (btn.classList.contains("table-btn")) {
                audio = tableButtonsAudio;
            } else if (btn.classList.contains("page-nav-btn")) {
                audio = pageNavButtonsAudio;
            } else if (btn.classList.contains("search-btn")) {
                audio = searchButtonsAudio;
            }
            console.log(audio);

            btn.addEventListener("click", () => {
                audio.play();
            });
        });
    });
   
    // const tableButtons = document.querySelectorAll(".table-btn");


//    tableButtons.forEach(btn => {
//         btn.addEventListener("click", () => {
//             tableButtonsAudio.play();
//         });
//    });

//    const pageNavButtons = document.querySelectorAll(".page-nav-btn"); 
//    const searchButtons = document.querySelectorAll(".search-btn"); 

});
