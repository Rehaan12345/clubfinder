// ********** Adds new club function: ********** //
// Keeps track of the number of clubs created: 
let numClubs = 0;
// Waits for the window to load before finding the id of the submit button and making sure it is not null, all before waiting for the user to click on it and call the function addNewClub():
//window.onload = function() {
    //const submitButton = document.getElementById("submit");
    //if (submitButton == null) {
        //console.log("submit button is null, returning.");
      //  return;
    //}
    //else submitButton.addEventListener("click", addNewClub);
//}
    
function addNewClub(e) {
    console.log("Function starts");
    // KEEPS THE FORM ELEMENTS ON THE PAGE!!!: WOWZERS!
    event.preventDefault();
    console.log("Prevented Default");
    // Stores the "maincontainer" div element:
    const mainContainer = document.getElementById("maincontainer");
    console.log("Main container found");
    // Finds the name of the club that the user typed in:
    const clubName = document.getElementById("nameofclub").value;
    console.log("clubName: " + clubName + " secured");
    // Checks to make sure clubName has a value, if not it returns and a club is not created:
    if (clubName.length < 1) {
        console.log("Club name too short, returned");
        return;
    }
    // ELSE, creates the new club:
    const newClub = document.createElement("div");
    console.log("div created");
    // Increments the number of clubs:
    numClubs++;
    console.log("numClubs incremented");
    // Adds the "club" class to the new element: 
    newClub.classList.add("club");
    console.log("club class added");
    // Adds the new club id to the new element:
    newClub.setAttribute("id", "club" + numClubs);
    console.log("id added");
    // Adds the new club to the "maincontainer" class in HTML: 
    mainContainer.appendChild(newClub);
    console.log("new club added to maincontainer div");
    // Calls the new club the correct name:
    newClub.innerHTML = clubName;
    console.log("club successfully added");
};
// Clear all clubs:
function clearClubs() {
    if (numClubs > 0) {
        for (let i = 0; i < numClubs; i++) {
            const club = document.querySelector(".club");
            club.remove();
        }
    }
}

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

// ********** View Club Popup Modal (Open and close functions): ********** //
function openModal() {
    const modal = document.getElementById("clubdesc");
    const parentModal = modal.parentElement.id;
    console.log("parentModal: " + parentModal);
    const overlay = document.getElementById("overlay");
    if (modal == null || overlay == null) {
        console.log("Modal or overlay is null.");
        return;
    } 
    modal.classList.add("active");
    overlay.classList.add("active");
}

function closeModal() {
    const modal = document.getElementById("clubdesc");
    const overlay = document.getElementById("overlay");
    if (modal == null || overlay == null) {
        console.log("Modal or overlay is null.");
        return;
    } 
    modal.classList.remove("active");
    overlay.classList.remove("active");
} 

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
        // const joinClubButton = document.getElementById("joinclubbutton");  jdhfjh 
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
