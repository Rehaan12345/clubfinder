// ********** Flash close buttons: ********** //
window.addEventListener("DOMContentLoaded", () => {
    // Closes the flashed message on click:
    const closebutton = document.getElementById("flash");
    closebutton.addEventListener("click", () => {
        closebutton.classList.remove("show");
        closebutton.classList.add("hide");
    });
    // The button goes away after 5 seconds:
    setTimeout(() => {
        closebutton.classList.remove("show");
        closebutton.classList.add("hide");
    }, 5000)
});

// ********** Open / Close modal functions: ********** // 
// Waits for the window to be fully loaded before starting this function:
window.addEventListener("DOMContentLoaded", () => {
    // Finds the parent element of all the card/club child elements:
    const parent = document.querySelector(".maincontainer");
    // Adds an event listener to that element, calling the openModal() function once it has been clicked:
    parent.addEventListener("click", openModal); 
});

// Opens the modal:
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
        // Actually opens/shows the modal:
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
            // Closes the modal:
            modal.close();
        }); 
        // Closes the modal when clicking outside (copied from WebDevSimplified's code):
        modal.addEventListener("click", e => {
            const dialogDimensions = modal.getBoundingClientRect()
            if (
              e.clientX < dialogDimensions.left ||
              e.clientX > dialogDimensions.right ||
              e.clientY < dialogDimensions.top ||
              e.clientY > dialogDimensions.bottom
            ) {
              modal.close()
            }
          })
    };  
}; 

// ********** Join / Leave club functions: ********** //
// Waits for the window to be fully loaded before starting this function:
window.addEventListener("DOMContentLoaded", () => {
    // Finds the parent element of all the card/club child elements:
    const parent = document.querySelector(".maincontainer");
    // Adds an event listener to that element, calling the openModal() function once it has been clicked:
    parent.addEventListener("click", joinOrLeaveClub); 
});

// Joins the club function:
function joinOrLeaveClub(e) {
    // Club Id of the element that was clicked on:
    let elementClickedOnTargetID = 0;
    // Finds the clicked on element:
    const elementClickedOn = e.target;
    console.log(elementClickedOn);
    // The target of the button that was clicked:
    let elementClickedOnTarget = elementClickedOn.id;
    console.log("Elementclickontarget: " + elementClickedOnTarget);
    // Removes the last digits from the joinclubbutton id.
    for (let i = 0; i < elementClickedOnTarget.length; i++) {
        if (elementClickedOnTarget.indexOf("_") === i) {
            elementClickedOnTargetID = elementClickedOnTarget.substring(i + 1);
            console.log("ElementclickedontargetFINAL's id: " + elementClickedOnTargetID);
            elementClickedOnTarget = elementClickedOnTarget.substring(0, i);
            console.log("ElementclickedontargetFINAL: " + elementClickedOnTarget);
            break;
        }
    }

    const joinClubButton = "joinclubbutton"; 
    const leaveClubButton = "leaveclubbutton"; 

    if (elementClickedOnTarget.localeCompare(joinClubButton) === 0) {
        console.log("Join club button pressed.");

        // Reloads the page onclick:
        window.location.reload();

        const clubName = elementClickedOn.parentElement.id;
        console.log(clubName);

        $.ajax({
            url: "",
            // Sending this information to the backend Python server in a "GET" request: 
            type: "GET",
            contentType: "application/json",
            // The data to send to the backend server:
            data: {
                // Sending the name of the club the user wants to join:
                joinClub: clubName
            },
            // A success message if all goes well, also for debugging:
            success: console.log("Successfully requested to join " + clubName) // (Change this later)
        }); 
    } 
    else if (elementClickedOnTarget.localeCompare(leaveClubButton) === 0) {
        console.log("Leave club button pressed.");

        // Reloads the page onclick:
        window.location.reload();

        // // Only shows the correct club:
        // elementClickedOn.classList.remove("show");
        // elementClickedOn.classList.add("hide");

        // localStorage.removeItem("In Club");

        // if (elementClickedOnTargetID > 0) {
        //     const join = document.getElementById("joinclubbutton_" + elementClickedOnTargetID);
        //     console.log(join);
        //     join.classList.remove("hide");
        //     join.classList.add("show");
        // } else return -1;

        const clubName = elementClickedOn.parentElement.id;
        console.log(clubName);

        $.ajax({
            url: "",
            // Sending this information to the backend Python server in a "GET" request: 
            type: "GET",
            contentType: "application/json",
            // The data to send to the backend server:
            data: {
                // Sending the name of the club the user wants to join:
                leaveClub: clubName
            },
            // A success message if all goes well, also for debugging:
            success: console.log("Successfully requested to leave " + clubName) /* Change this later */
        }); 
    }
}

// ********** Color Picker JS: ********** //
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
    };
    
    colorThemes.forEach((themeOption) => {
        themeOption.addEventListener("click", () => {
            storeTheme(themeOption.id);
        });
    });
    
    // Applies the correct theme: 
    retrieveTheme();
});

// ********** Nav button functionality: ********** //
// window.addEventListener("DOMContentLoaded", () => {
//     const navElement = document.querySelector(".navlink");
//     console.log("Target: " + navElement)
//     navElement.addEventListener("click", () => {
//         navElement.classList.add("activeclick");
//     });
// });

window.addEventListener("DOMContentLoaded", ()=> {
    document.addEventListener("click", e=> {
        const isDropDownButton = e.target.matches("[data-dropdown-button]");
        if(!isDropDownButton && e.target.closest("[data-dropdown]") != null) return;

        let currentDropDown;
        if(isDropDownButton) {
            currentDropDown = e.target.closest("[data-dropdown]");
            currentDropDown.classList.toggle("active");
        }
        
        document.querySelectorAll("[data-dropdown].active").forEach(dropdown => {
            if (dropdown === currentDropDown) return;
            dropdown.classList.remove("active");
        });
    });
});

// ********** Filter By Button Functionality: **********/
window.addEventListener("DOMContentLoaded", () => {
    const filterByButtons = document.querySelectorAll(".filter");
    for (let i = 0; i < filterByButtons.length; i++) {
        let numClicked = 1;
        filterByButtons[i].addEventListener("click", (e) => {
            numClicked++;
            if ((numClicked % 2) === 0){
                const filter = e.target.id;
                console.log("User clicked on " + filter);
                $.ajax({
                    url: "",
                    type: "GET",
                    contentType: "application/json",
                    data: {
                        filterby: filter
                    },
                    success: console.log("Successfully sent " + filter + " to the backend.")
                })
            }

        });
    }
});

// ********** Connect to Club Modal & Button Functionalities: ********** //
window.addEventListener("DOMContentLoaded", () => {
    const connectToClubModal = document.getElementById("connecttoclubmodal");
    const openClubModalButton = document.getElementById("connecttoclubbutton");
    openClubModalButton.addEventListener("click", () => {
        connectToClubModal.show();
    });

    const closeButton = document.getElementById("clubclosebutton"); 
    // Waits for a click and closes that modal: 
    closeButton.addEventListener("click", () => {
        // Closes the modal:
        connectToClubModal.close();
    }); 
    
    // Fix this later:
    connectToClubModal.addEventListener("click", e => {
        const dialogDimensions = connectToClubModal.getBoundingClientRect()
        if (
          e.clientX < dialogDimensions.left ||
          e.clientX > dialogDimensions.right ||
          e.clientY < dialogDimensions.top ||
          e.clientY > dialogDimensions.bottom
        ) {
            connectToClubModal.close()
        }
    });
});

// ********** Kick Member from Club Button Functionality: ********** //
window.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", openKickModal); 
});

function openKickModal(e) {
    let targetID = -1;
    targetID = e.target.id;
    console.log("Target id = " + targetID);
    if (targetID.substring(targetID.length - 1).localeCompare("*") === 0) return;
    let clubID = -1;
    if (targetID.indexOf("_") > -1) {
        clubID = targetID.substring(targetID.indexOf("_") + 1, targetID.indexOf("-"));
    }
    console.log("Club id = " + clubID);
    let memberID = -1;
    if (targetID.indexOf("-") > -1) {
        memberID = targetID.substring(targetID.indexOf("-") + 1);
    }
    console.log("Member id = " + memberID);
    let rest = "rehaan";
    if (targetID.indexOf("_") > -1 && targetID.indexOf("-") > -1) {
        rest = targetID.substring(0, targetID.indexOf("_"));
    }
    console.log("Rest: " + rest);
    const kickButton = document.getElementById("kickbutton_" + clubID + "-" + memberID);
    console.log(kickButton);
    const kickModal = document.getElementById("kickbuttonconfirmationbutton_" + clubID + "-" + memberID);
    console.log(kickModal);
    if (rest.localeCompare("kickbutton") === 0) {
        console.log("Kick Button clicked");
        kickModal.showModal();
        const noKick = document.getElementById("notokick_" + clubID + "-" + memberID);
        noKick.addEventListener("click", () => {
            kickModal.close();
        })
        const yesKick = document.getElementById("yestokick_" + clubID + "-" + memberID);
        yesKick.addEventListener("click", () => {
            $.ajax({
                url: "",
                type: "GET",
                contentType: "application/json",
                data: {
                    removeClub: clubID,
                    removeMember: memberID
                },
                success: kickModal.close()
            })
        })
    }
}

// ********** Create a Club Required ********** //
// window.addEventListener("DOMContentLoaded", () => {
//     // const requiredSymbol = document.querySelector(".fa-star-of-life");
//     // console.log(requiredSymbol);
//     const createAClubRequiredModal = document.getElementById("createaclubrequiredmodal");
//     // console.log(createAClubRequiredModal);
//     // requiredSymbol.addEventListener("click", () => {
//     //     console.log("Opened modal");
//     //     createAClubRequiredModal.showModal();
//     // })
//     window.addEventListener("click", (e) => {
//         const clicked = e.target;
//         const clickedId = e.target.id;
//         console.log("Clickedid: " + clickedId);
//         const clickedIdId = document.querySelector(".fa-star-of-life")
//         clicked.getBoundingClientRect();
//         console.log(clicked.getBoundingClientRect());
//         createAClubRequiredModal.showModal();
//         // Make sure the correct thing has been clicked (compare to className or id):
//         // if (clicked.parentElement.localeCompare("details") === 0) {
//         //     createAClubRequiredModal.showModal();
//         // }
//     })
// })

// ********** Text Area Dynamically Expanding: ********* //
document.addEventListener("DOMContentLoaded", () => {
    const textarea = document.getElementById("inputthedescription");
    textarea.addEventListener("keyup", e => {
        textarea.style.height = "45px";
        let scHeight = e.target.scrollHeight;
        console.log(scHeight);
        textarea.style.height = `${scHeight}px`;
    })
});

// ********** Choose Club Days: ********** //
document.addEventListener("DOMContentLoaded", () => {
    const selectbutton = document.querySelector(".selectbutton");
    const items = document.querySelectorAll(".day");

    selectbutton.addEventListener("click", () => {
        selectbutton.classList.toggle("open");
    });

    let daysSelected = [];

    let buttonText = document.querySelector(".buttontext");

    items.forEach(item => {
        item.addEventListener("click", () => {
            item.classList.toggle("checked");

            function removeDuplicate(arr) { 
                // Create a Set to store unique values
                const uniqueSet = new Set(arr);
                
                // Convert the Set back to an array
                const uniqueArray = [...uniqueSet];
                
                return uniqueArray;
            }

            if (item.classList.length > 1) {
    
                daysSelected.push(item.id);
    
                daysSelected = removeDuplicate(daysSelected);
                
                console.log(daysSelected);
                if (daysSelected.length === 0) {
                    buttonText.innerHTML = "0 Selected";
                } else if (daysSelected.length === 5) {
                    buttonText.innerHTML = "Everyday";
                }
                else { buttonText.innerHTML = daysSelected; }
                $.ajax({
                    url: "",
                    type: "POST",
                    contentType: "application/json",
                    data: {
                        clubDays: daysSelected
                    },
                    success: console.log("Successfully sent " + daysSelected)
                })
            } else {
                let index = null;
                for (let j = 0; j < daysSelected.length; j++) {
                    if (daysSelected[j].localeCompare(item.id) === 0) {
                        index = j;
                        break;
                    }
                }
                daysSelected.splice(index, 1);
                console.log(daysSelected);

                if (daysSelected.length === 0) {
                    buttonText.innerHTML = "0 Selected";
                } else { buttonText.innerHTML = daysSelected; }
                
            }
        })
    })

})
