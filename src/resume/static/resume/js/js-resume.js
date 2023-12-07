// Change text size based on its length
// Origin example: https://codepen.io/jsstrn/pen/mMMmZB

const getFontSize = (textLength) => {
    // console.log(`textLength=${textLength}`);
    const baseSize = 9
    let fontSize = 14
    if (textLength > baseSize) {
        // textLength = baseSize - textLength
        return `${fontSize - 4}px`
    }
    // const fontSize = baseSize + textLength + 5
    // console.log(`fontSize=${fontSize}`);
    return `${fontSize}px`
}

const boxes = document.querySelectorAll('.resume_wrapper .resume_right .resume_data .tag__item')

boxes.forEach(box => {
    box.style.fontSize = getFontSize(box.textContent.length)
})


const printButton = document.querySelector(".action-print");
printButton.addEventListener("click", function (event) {
    window.print();
});


function toggleSpoilerAnimated(spoilerElement, isInvertedCollapse, isInvertedExpand, duration = 300) {
    let spoilerBody = spoilerElement.querySelector('.spoiler-body');
    // let isCollapsing = spoilerElement.classList.contains('expanded');
    let isCollapsing = spoilerElement.classList.contains('expanded');
    let heightBefore = spoilerElement.offsetHeight;
    let offsetBefore = window.pageYOffset;
    spoilerElement.classList.toggle('expanded', !isCollapsing);
    let isScrollRequired = (isCollapsing && isInvertedCollapse) ||
        (!isCollapsing && isInvertedExpand);
    // let scrollFunc = (isScrollRequired)
    //   ? () => {
    //     let heightNow = spoilerElement.offsetHeight;
    //     let heightDelta = heightNow - heightBefore;
    //     window.scrollTo(0, offsetBefore + heightDelta);
    //   }
    //   : undefined;
    let scrollFunc = undefined;
    slideToggle(spoilerBody, !isCollapsing, { duration: duration, progress: scrollFunc, complete: scrollFunc });
}

for (let el of document.querySelectorAll('.spoiler-btn-top')) {
    el.addEventListener('click', e => toggleSpoilerAnimated(el.parentNode));
}
for (let el of document.querySelectorAll('.spoiler-btn-bottom')) {
    el.addEventListener('click', e => toggleSpoilerAnimated(el.parentNode, true, true));
}

function slideUp(element, options) { slideToggle(element, false, options); }
function slideDown(element, options) { slideToggle(element, true, options); }
function slideToggle(element, isOpening, options) {
    let h0 = getHeight(element);
    let duration = (options && options.duration) || 1000;
    let start = null;
    function step(timestamp) {
        if (!start) { start = timestamp; }
        // let progress = 1.0 * (timestamp - start) / duration;
        let progress = 1.9 * (timestamp - start) / duration;
        let h1 = isOpening ? (h0 * progress) : (h0 * (1 - progress));
        if (progress < 1.0) {
            element.style.height = h1 + 'px';
            if (options.progress) { options.progress(); }
            window.requestAnimationFrame(step);
        } else {
            element.style.height = '';
            element.style.overflow = '';
            if (!isOpening) { element.style.display = 'none'; }
            if (options.complete) { options.complete(); }
        }
    }
    element.style.display = 'block';
    element.style.overflow = 'hidden';
    window.requestAnimationFrame(step);
}

// https://stackoverflow.com/a/29047232/3423843
function getHeight(el) {
    let el_comp_style = window.getComputedStyle(el),
        el_display = el_comp_style.display,
        el_max_height = el_comp_style.maxHeight.replace('px', '').replace('%', ''),
        el_position = el.style.position,
        el_visibility = el.style.visibility,
        wanted_height = 0;

    if (el_display !== 'none' && el_max_height !== '0') {
        return el.offsetHeight;
    }

    el.style.position = 'absolute';
    el.style.visibility = 'hidden';
    el.style.display = 'block';

    wanted_height = el.offsetHeight;

    el.style.display = el_display;
    el.style.position = el_position;
    el.style.visibility = el_visibility;

    return wanted_height;
}


// Show / hide FULL PAGE OVERLAY
// with certificate image
// adapted from: https://code-boxx.com/simple-fullscreen-overlay-css-js/


let overlay = document.getElementById('owrap');
const certIcons = document.querySelectorAll(".img-certificate-box");
let certificateNode = document.querySelector(".resume_left .resume_bottom .resume_certificate");


function showOverlay(event) {
    let overlayWrapper = document.createElement("div")
    overlayWrapper.id = "owrap"
    let overlayBox = document.createElement("div")
    overlayBox.id = "obox"
    let certImage = document.createElement("img")
    // Get data-* attributes from parent div of img
    const imgUrl = event.currentTarget.dataset.imgUrl;
    const imgAltText = event.currentTarget.dataset.imgAlt;
    certImage.src = imgUrl;
    certImage.alt = imgAltText;
    let certImageDiv = document.createElement("div");
    certImageDiv.className = "certificate_image";
    let closeButton = document.createElement("button");
    closeButton.id = "close-overlay";
    closeButton.className = "close-button";
    closeButton.textContent = "X";
    closeButton.setAttribute("title", "Close");
    closeButton.addEventListener("click", closeOverlay);

    // Composing our overlay block and its content
    certImageDiv.appendChild(certImage);
    overlayBox.appendChild(certImageDiv);
    overlayBox.appendChild(closeButton);
    overlayWrapper.appendChild(overlayBox);

    // Add hidden overlay div in the certificates node
    certificateNode.appendChild(overlayWrapper);

    overlayWrapper.classList.add("show");
    // Disable "scrolling" by mouse wheel
    overlayWrapper.onwheel = e => e.preventDefault();
    // The following line blocks scrolling on mobile devices
    // letting to tap on the Close button
    // BUT! picture zooming also OFF, so scrolling is ON on mobile
    // overlayWrapper.ontouchmove = e => e.preventDefault();
}

certIcons.forEach(certIcon => {
    certIcon.addEventListener("click", showOverlay);
})

function closeOverlay(event) {
    let overlay = document.getElementById('owrap');
    overlay.classList.remove("show");
    // Remove overlay completely after hiding it.
    overlay.remove();
}


// RESUME INFO BOX ANIMATION and MEDIA QUERY LOGIC


const infoBox = document.getElementById("cv-info-box");
const infoCircle = document.querySelector(".circle");
const infoIcon = document.getElementById("cv-info-box-icon");
const cvInfoText = document.getElementById("cv-info-text");
let isInfoDisplayed = false;

// Show info box with animations
function showInfoBox() {
    // Remove all animation styles after hiding (folding down) the info box
    infoBox.addEventListener("animationend", listener, false);

    // Recalculate styles (without animation) twice (by repaint design)
    requestAnimationFrame((time) => {
        requestAnimationFrame((time) => {
            // Enable (toggle) animation classes for needed elements.
            infoBox.classList.toggle("anima-increasing-height");
            infoCircle.classList.toggle("anima-unfolding");
            infoIcon.classList.toggle("anima-icon-up");
            cvInfoText.classList.toggle("anima-fading-in-top");
            // Switch flag that info box was unfold
            isInfoDisplayed = true;
        });
    });
}

// Hide info box with animations
function hideInfoBox() {
    if (isInfoDisplayed) {
        // Ensure that 'unfolding' styles are present (need for correct animation)
        infoBox.classList.add("anima-increasing-height");
        infoIcon.classList.add("anima-icon-up");
        requestAnimationFrame((time) => {
            requestAnimationFrame((time) => {
                infoBox.classList.toggle("anima-decreasing-height");
                infoCircle.classList.add("anima-folding-down");
                infoIcon.classList.add("anima-icon-down");
                isInfoDisplayed = false;
            });
        });

    }
}

// Handler for "animationend" event (to clear animation styles).
const listener = (e) => {
    switch (e.animationName) {
        case "icon-down":
            infoBox.classList.remove("anima-decreasing-height");
            // infoIcon.classList.remove("anima-icon-down");
            infoIcon.removeAttribute("class");  // No other classes, now
            infoCircle.classList.remove("anima-folding-down");
            break;
    }
};

// Create the query lists.
const mediaQLmaxWidth1200 = window.matchMedia("(max-width: 1200px)");
const mediaQLmaxWidth1400 = window.matchMedia("(max-width: 1400px)");

// Define a callback function for the event listener.
function handleMaxWidth1200Change(evt) {
    if (evt.matches) {
        infoCircle.removeEventListener("click", showInfoBox);
        infoCircle.removeEventListener("click", hideInfoBox);
        infoIcon.removeEventListener("click", showInfoBox);
        infoIcon.removeEventListener("click", hideInfoBox);
    } else {
        // Add event handlers for both elements (scaling circle and (i) icon)
        infoCircle.addEventListener("click", showInfoBox, false);
        infoCircle.addEventListener("click", hideInfoBox, false);
        infoIcon.addEventListener("click", showInfoBox, false);
        infoIcon.addEventListener("click", hideInfoBox, false);
    }
}

// Edge case (hack): when info box is opened
// and user resize browser window
function handleMaxWidth1400Change(evt) {
    if (isInfoDisplayed) {
        if (evt.matches) {
            infoIcon.click();  // close info box
        }
    }
}

// Run the width change handler once.
handleMaxWidth1200Change(mediaQLmaxWidth1200);
// handleMaxWidth1400Change(mediaQLmaxWidth1400);  // no need for 1400px

// Add the callback function as a listener to the query list.
mediaQLmaxWidth1200.addEventListener("change", handleMaxWidth1200Change);
mediaQLmaxWidth1400.addEventListener("change", handleMaxWidth1400Change);
