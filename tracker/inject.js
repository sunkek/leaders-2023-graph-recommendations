// Укажите электронную почту пользователя, за которого нужно сохранить действия на сайте
const userEmail = "your@email.com";
// Если в консоли браузера есть строки "Activity sent", то всё работает отлично

const apiURL = "https://api.recommender.suncake.xyz";
const offerTypes = ["event", "excursion", "hotel", "place", "restaurant", "route", "tour", "track"];

async function sendActivity(offerID, offerType, type) {
    console.log(JSON.stringify({
        user_email: userEmail, 
        offer_id: offerID, 
        offer_type: offerType, 
        type: type
    }))
    fetch(apiURL+"/activity", {
        method: "post",
        headers: { "Content-Type": "application/json; charset=utf-8" },
        body: JSON.stringify({
            user_email: userEmail, 
            offer_id: offerID, 
            offer_type: offerType, 
            type: type
        })
    })
        .then(resp => {
            if (resp.status === 200) {
                console.log("Activity sent");
            } else {
                resp.json()
                .then(data => {
                    console.log("Activity not sent, response:", data);
                })
                .catch(err => {
                    console.log("Activity not sent, error:", err);
                })
            }
        })
        .catch(err => {
            console.log("Activity not sent, error:", err)
        });
};

function parseLink(link) {
    link = link.split("/");
    return [link[link.length - 1].split("?")[0], link[link.length - 2]];
};

function isSmallFavoriteButton(e) {
    return e.classList.contains("button") && 
        e.classList.contains("button--on-image") &&
        e.querySelector(".favorite--not-active");
};

function isBigFavoriteButton(e) {
    return e.textContent.includes("В Избранное");
};

function isCard(e) {
    return e.classList.contains("hotel-showcase__link") || 
        e.classList.contains("main-activity-card-new__link") || 
        e.classList.contains("main-activity-card__link");
};

function isCardImage(e) {
    return e.tagName === "IMG" && isCard(
        e.parentNode.parentNode
        .parentNode.parentNode
        .parentNode.parentNode.children[0]
    )
};

function isHotelImage(e) {
    return e.tagName === "IMG" &&
        e.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .classList.contains("hotel-showcase");
};

function isMapPin(e) {
    return e.tagName === "YMAPS" &&
        offerTypes.some(v => window.location.href.includes(v));
};

document.addEventListener('click', async function(e) {
    if ( isSmallFavoriteButton(e.target) ) {
        console.log("Small favorite click");
        let link = e.target.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .children[0].href;
        let [id, type] = parseLink(link);
        await sendActivity(id, type, "favorite");
    } else if ( isBigFavoriteButton(e.target) ) {
        console.log("Big favorite click");
        let [id, type] = parseLink(window.location.href);
        await sendActivity(id, type, "favorite");
    } else if ( isCard(e.target) ) {
        console.log("Card click");
        let [id, type] = parseLink(e.target.href);
        await sendActivity(id, type, "view");
    } else if ( isCardImage(e.target) ) {
        console.log("Card image click");
        let link = e.target.parentNode.parentNode
            .parentNode.parentNode
            .parentNode.parentNode
            .children[0].href
        let [id, type] = parseLink(link);
        await sendActivity(id, type, "view");
    } else if ( isHotelImage(e.target) ) {
        console.log("Hotel image click");
        let link = e.target.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .parentNode.parentNode.parentNode
            .children[0].href
        let [id, type] = parseLink(link);
        await sendActivity(id, type, "view");
    }
}, true);


document.addEventListener('click', async function(e) {
    if ( isMapPin(e.target) ) {
        console.log("Map pin click");
        let [id, type] = parseLink(window.location.href);
        await sendActivity(id, type, "view");
    }
}, false);

console.log("Tracking script loaded for", userEmail)
