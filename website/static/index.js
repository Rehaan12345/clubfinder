// ********** Flash close buttons: ********** //
// Close Buttons automatically after 5 seconds: 
setTimeout(function(){
    $(".alert").removeClass("show");
    $(".alert").addClass("hide");
}, 5000);

setTimeout(function(){
    $(".success").removeClass("show");
    $(".success").addClass("hide");
}, 5000);

// Waits for the window to be fully loaded before starting this function:
window.addEventListener("DOMContentLoaded", () => {
    // Finds the parent element of all the card/club child elements:
    const parent = document.querySelector(".maincontainer");
    // Adds an event listener to that element, calling the openModal() function once it has been clicked:
    parent.addEventListener("click", openModal); 
});

function openModal(e) {
    // Finds the clicked element:
    const elementClickedOn = e.target;
    console.log(elementClickedOn);
    // The target of the button that was clicked: 
    let elementClickedOnTarget = elementClickedOn.formTarget;
    console.log(elementClickedOnTarget);
    // Makes sure the clicked on element is the correct element: 
    if (elementClickedOnTarget && elementClickedOnTarget.length) {
        // Removes the hash ("#") from the value of the id: 
        for (let i = 0; i < elementClickedOnTarget.length; i++) {
            if (elementClickedOnTarget.indexOf("#") === i) {
                elementClickedOnTarget = elementClickedOnTarget.substring(i + 1);
                console.log("New: " + elementClickedOnTarget);
            }
        }
        // Finds the correct modal with the new and correct id:
        const modal = document.getElementById(elementClickedOnTarget);
        console.log(modal);
        // Shows the modal:
        modal.showModal();
        // The id number of the club that was selected: ("club.id"):
        let idNum = -1;
        // Finds the id number of the clud (The last digits after the underscore ("_")):
        for (let i = 0; i < elementClickedOnTarget.length; i++) {
            if (elementClickedOnTarget.indexOf("_") === i) {
                idNum = elementClickedOnTarget.substring(i + 1);
                console.log(idNum);
            }
        }
        // Finds the correct close club button with the correct id number:
        const closeButton = document.getElementById("clubclosebutton_" + idNum); 
        console.log(closeButton.parentElement.parentElement.id);
        // Waits for a click and closes that modal: 
        closeButton.addEventListener("click", () => {
            modal.close();
        });
    }  
};

// ********** Join club, leave club button functions: ********** // 
/*function joinClub() {
    const joinClubButton = document.querySelector("#joinclubbutton");
    const jCBparentNode = joinClubButton.parentNode; 
    console.log(jCBparentNode.joinClubButton);
    //jCBparentNode.joinClubButton.classList.add("active");
};*/

function joinClub() {
    const parentdiv = document.getElementById("maincontainer");
    console.log("parentDiv: " + parentdiv.id);
    const joinButton = document.getElementById("joinclubbutton");
    console.log("JCB id: " + joinButton.id);
    const joinButtonParent = joinButton.parentElement;
    console.log("joinButtonParent id: " + joinButtonParent.id);
    console.log("Description: " + document.getElementById("clubdescdesc" + joinButton));
    // An array of all the child elements of the parentdiv, as shown above. 
    const clubs = parentdiv.querySelectorAll(".clubdesc"); 
    console.log(clubs);
    const pDfirstChild = parentdiv.firstElementChild.id;
    console.log(pDfirstChild); 

    const buttonParentNode = joinButton.parentNode.id;
    console.log("Elements found");
        console.log("Second function starts");
        // const joinClubButton = document.getElementById("joinclubbutton");  
        joinButton.classList.add("active");
        const clubName = document.getElementById(buttonParentNode + "1").textContent;
        // Sends to the python server which club the user has just joined (w/ AJAX):
        $.ajax({
            url: "",
            // Sending this information to the backend Python server in a "GET" request: 
            type: "GET",
            contentType: "application/json",
            // The data to send to the backend server:
            data: {
                // Sending the name of the club the user wants to join:
                nameOfClub: clubName
            },
            // A success message if all goes well, also for debugging:
            success: console.log("Successfully requested to join " + clubName /* Change this later */)
        });
    }

function leaveClub() {
    const joinClubButton = document.querySelector("#joinclubbutton");
    joinClubButton.classList.remove("active");
}

// Leave club function:
//function leaveClub(clubID) {
    
//};

//******************** Color Picker JS: ********************/
// Stores all of the themes:
window.addEventListener("DOMContentLoaded", () => {
    const colorThemes = document.querySelectorAll(".theme");

    // Stores the theme in the localStorage:
    const storeTheme = function (theme) {
        localStorage.setItem("theme", theme);
    };

    const retrieveTheme = function() {
        const activeTheme = localStorage.getItem("theme");
        colorThemes.forEach((themeOption) => {
            if (themeOption.id === activeTheme) {
                themeOption.checked = true;
            }
        })
    }
    
    colorThemes.forEach((themeOption) => {
        themeOption.addEventListener("click", () => {
            storeTheme(themeOption.id);
        });
    });
    
    // Applies the correct theme: 
    retrieveTheme();
});