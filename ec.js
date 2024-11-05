window.getElectoralCollegeData = function() {
    const ecData = [];
    
    // Process ".state_info" elements
    const stateEls = document.querySelectorAll(".state_info");
    for (let i = 0; i < stateEls.length; i++) {
        const stateEl = stateEls[i].querySelectorAll("span");
        if (stateEl.length == 2) {
            const stateName = stateEl[0].innerHTML.trim();
            const electoralVotes = stateEl[1].innerHTML.trim();
            ecData.push({ state: stateName, electoralVotes: electoralVotes });
        }
    }
    
    // Process ".special-states" elements
    const special = document.querySelector(".special-states");
    if (special) {
        const data = special.querySelectorAll("td");
        for (let i = 0; i < data.length; i += 2) {
            const stateName = data[i].innerText.trim();
            const electoralVotes = data[i + 1].innerText.trim();
            ecData.push({ state: stateName, electoralVotes: electoralVotes });
        }
    }

    return ecData;
}

window.getPathData = function() {
    const paths = document.querySelectorAll("path");
    const pathData = {};

    paths.forEach(path => {
        const id = path.id;
        
        // Only proceed if id is a valid FIPS code (numeric and at least 2 characters)
        if (!isNaN(id) && id.length >= 2 && id != '72') {
            const fill = path.getAttribute("fill");

            // Initialize the object for this FIPS code if it doesn't exist
            if (!pathData[id]) {
                pathData[id] = { Democrat: 0, Republican: 0 };
            }

            // Check the color and update Democrat or Republican vote
            if (fill === '#244999') {         // Blue color for Democrat
                pathData[id].Democrat += 1;
            } else if (fill === '#D22532') {  // Red color for Republican
                pathData[id].Republican += 1;
            }
        }
    });

    return pathData;
}


window.getSpecial = function(){
    const districts = document.querySelectorAll(".special-states")[1];
    const ME = districts.querySelectorAll("tr")[2];
    const NE = districts.querySelectorAll("tr")[3];
    
    // Function to categorize based on color
    function getPartyFromColor(style) {
        if (style.includes("rgb(36, 73, 153)")) {
            return "Democrat";
        } else if (style.includes("rgb(210, 37, 50)")) {
            return "Republican";
        }
        return "Unknown";
    }
    
    // Maine data processing
    const maineData = ME.querySelectorAll("td");
    const maineResults = { "Democrat": 0, "Republican": 0 };
    
    for (let i = 1; i < maineData.length - 1; i++) {
        const dat = maineData[i].querySelectorAll("span");
        const votes = parseInt(dat[0].innerText, 10);  // Get votes as integer
        const partyStyle = maineData[i].querySelector("div").getAttribute("style");
        const party = getPartyFromColor(partyStyle);
    
        // Add votes to the correct party
        if (party === "Democrat" || party === "Republican") {
            maineResults[party] += votes;
        }
    }
    
    // Nebraska data processing
    const nebraskaData = NE.querySelectorAll("td");
    const nebraskaResults = { "Democrat": 0, "Republican": 0 };
    
    for (let i = 1; i < nebraskaData.length; i++) {
        const dat = nebraskaData[i].querySelectorAll("span");
        const votes = parseInt(dat[0].innerText, 10);  // Get votes as integer
        const partyStyle = nebraskaData[i].querySelector("div").getAttribute("style");
        const party = getPartyFromColor(partyStyle);
    
        // Add votes to the correct party
        if (party === "Democrat" || party === "Republican") {
            nebraskaResults[party] += votes;
        }
    }
    
    // Combine into final result
    const votes = {
        "ME": maineResults,
        "NE": nebraskaResults
    };

    console.log(votes);
    return(votes)
}