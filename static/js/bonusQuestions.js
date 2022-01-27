// you receive an array of objects which you must sort in the by the key "sortField" in the "sortDirection"
function getSortedItems(items, sortField, sortDirection) {
    console.log(items)
    console.log(sortField)
    console.log(sortDirection)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    if (sortDirection === "asc") {
        const firstItem = items.shift()
        if (firstItem) {
            items.push(firstItem)
        }
    } else {
        const lastItem = items.pop()
        if (lastItem) {
            items.push(lastItem)
        }
    }

    return items
}

// you receive an array of objects which you must filter by all it's keys to have a value matching "filterValue"
function getFilteredItems(items, filterValue) {

    // console.log(items)
    // console.log(filterValue)

    // === SAMPLE CODE ===
    // if you have not changed the original html uncomment the code below to have an idea of the
    // effect this function has on the table
    //
    let searchResult = [];
    console.log(filterValue.substr(1,filterValue.length));
    for (let i=0; i<items.length; i++) {
        console.log(items[i]);
        if (filterValue[0] !== '!') {
            if (items[i]["Description"].includes(filterValue.substr("description:".length, filterValue.length))
        && filterValue.includes("Description:")) {
                searchResult.push(items[i]);
            }
            else if (items[i]["Title"].includes(filterValue)) {
                searchResult.push(items[i]);
            }
        }
        else {
            if (filterValue.includes("Description")) {
                if (!(items[i]["Description"].includes(filterValue.substr("!Description:".length, filterValue.length)))) {
                    searchResult.push(items[i]);
                }
        }
        else if (!(items[i]["Title"].includes(filterValue.substr(1,filterValue.length))))
            {
                searchResult.push(items[i]);
            }
        }
    }

    return searchResult;
}

function toggleTheme() {
    console.log("toggle theme")
}

function increaseFont() {
//     for (const text of document.querySelectorAll('.fontsize')) {
//         text.style.fontSize++;
//     }
// }

//      let tableContent = document.getElementById("doNotModifyThisId_QuestionsTableBody");
//      let style = window.getComputedStyle(tableContent, null).getPropertyValue('font-size');
//      let currentSize = parseFloat(style);
//      tableContent.style.fontSize = (currentSize++) + 'px';
// }
//
//
//
// {
//     let fontSize = document.getElementById("increase-font-button").style.fontSize;
//     // if (fontSize < 15) {
//         ++fontSize;
//     // }
    console.log("increaseFont")
}

function decreaseFont() {
    let fontSize = document.getElementById("increase-font-button").style.fontSize;
    if (fontSize > 3) {
        --fontSize;
    }

    console.log("decreaseFont")
}