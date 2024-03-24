function showFunctions() {
    document.getElementById("element1").style.display = "block";
    document.getElementById("element2").style.display = "none";
    document.getElementById("btnElement1").classList.add("active");
    document.getElementById("btnElement2").classList.remove("active");
    localStorage.setItem('searchBy', 'functions');
    localStorage.removeItem('key');
}

function showPathways() {
    document.getElementById("element1").style.display = "none";
    document.getElementById("element2").style.display = "block";
    document.getElementById("btnElement1").classList.remove("active");
    document.getElementById("btnElement2").classList.add("active");
    localStorage.setItem('searchBy', 'pathways');
    localStorage.removeItem('key');
}

function opened_submenu() {
    const searchBy = localStorage.getItem('searchBy');
    const key = localStorage.getItem('key');

    const currentUrl = window.location.href;
    const pattern = /^https?:\/\/(?:www\.)?.+?\/glycoenzdb\/human\/.+\/?$/i;

    const part = currentUrl.split("/");
    part.pop();
    const gene_name = part.pop();
    
    n_subclass = 4;
    if (searchBy == 'pathways') {
        showPathways()
        n_subclass = 6;
    } else {
        showFunctions();
        n_subclass = 4;
    }

    if (pattern.test(currentUrl) && key) {
        const key_arr = key.split("_")
        for (i = 0; i < n_subclass; i++) {
            if(key_arr[i] === "NULL"){
                break;
            }
            const id = [...key_arr].splice(0, i+1).join("_") + ("_NULL".repeat(n_subclass - i - 1));
            const element = document.getElementById(id);
            if (element) {
                setTimeout( () => {element.click();}, 10);
            }
        }
        setTimeout( () => {
            selected_gene_ele = document.getElementById(gene_name);
            if (selected_gene_ele) {
                selected_gene_ele.classList.add('fw-bold');
                selected_gene_ele.classList.add('text-primary');
            }
        }, 100);

    } else {
      localStorage.clear();
    }
}

function clear_link_styles(element) {
    const RIGHT_ARROW = '▶';
    const DOWN_ARROW = '▼';

    const childNodes = element.parentElement.querySelectorAll('a');

    const symbol_span = element.querySelector('span');
    if (symbol_span && symbol_span.innerHTML === DOWN_ARROW){
        symbol_span.innerHTML = RIGHT_ARROW;
    }
    else if (symbol_span && symbol_span.innerHTML === RIGHT_ARROW){
        symbol_span.innerHTML = DOWN_ARROW;
    }

    childNodes.forEach(childNode => {
        childNode.classList.remove('fw-bold');
        childNode.classList.remove('text-primary');

        if (element !== childNode){
            const symbol_span =  childNode.querySelector('span');
            if (symbol_span && symbol_span.innerHTML === DOWN_ARROW){
                symbol_span.innerHTML = RIGHT_ARROW;
            }

        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    const RIGHT_ARROW = '▶';
    const DOWN_ARROW = '▼';

    opened_submenu();
    document.querySelectorAll('.sidebar .nav-link').forEach(function (element) {

        element.addEventListener('click', function (e) {
            let nextEl = element.nextElementSibling;
            let parentEl = element.parentElement;

            // Styling the element - START

            //  Clear all syblings and sub links styles            
            if (parentEl && parentEl.parentElement){
            const childNodes = parentEl.parentElement.querySelectorAll('a');

            const symbol_span = element.querySelector('span');
            if (symbol_span && symbol_span.innerHTML === DOWN_ARROW){
                symbol_span.innerHTML = RIGHT_ARROW;
            }
            else if (symbol_span && symbol_span.innerHTML === RIGHT_ARROW){
                symbol_span.innerHTML = DOWN_ARROW;
            }

            childNodes.forEach(childNode => {
                childNode.classList.remove('fw-bold');
                childNode.classList.remove('text-primary');

                if (element !== childNode){
                  const symbol_span =  childNode.querySelector('span');
                    if (symbol_span && symbol_span.innerHTML === DOWN_ARROW){
                        symbol_span.innerHTML = RIGHT_ARROW;
                    }
                }
            });

        }
            // Bold the current link
            element.classList.add('fw-bold');
            element.classList.add('text-primary');

            // Styling - END

            if (nextEl) {
                e.preventDefault();
                let mycollapse = new bootstrap.Collapse(nextEl);

                if (nextEl.classList.contains('show')) {
                    mycollapse.hide();
                } else {
                    mycollapse.show();
                    // find other submenus with class=show
                    var opened_submenu = parentEl.parentElement.querySelector('.submenu.show');
                    // if it exists, then close all of them
                    if (opened_submenu) {
                        new bootstrap.Collapse(opened_submenu);
                    }
                }
            }
        }); // addEventListener
    }) // forEach
});
// DOMContentLoaded  end

// window.onload = function() {
//     const violin_iframe = document.getElementById('sc_violin_iframe');
//     // const violin_header = document.getElementById('sc_violin_header');
//     if (!violin_iframe){
//         return;
//     }
//     var currentUrl = window.location.href;
//     var segments = currentUrl.split('/');
//     var subpath = segments[segments.length - 2];
//     var newUrl = `/violinplots?gene_name=${subpath}`;
//     violin_iframe.src = newUrl;
//   }

  // Wait for the DOM content to load
document.addEventListener("DOMContentLoaded", function() {
    // Get the SVG object
    const svgObject = document.getElementById("svg-object");

    // Function to adjust SVG dimensions based on parent container's width
    function resizeSvg() {
        if (!svgObject) {
            return
        }
        const parentWidth = svgObject.parentElement.clientWidth;
        svgObject.style.width = parentWidth + "px";
        // Calculate the height to maintain the original aspect ratio
        const originalWidth = 1500; // Replace this with the original width of your SVG
        const originalHeight = svgObject.contentDocument.documentElement.getAttribute("height");
        const aspectRatio = originalHeight / originalWidth;
        const newHeight = Math.round(parentWidth * aspectRatio);
        svgObject.style.height = newHeight + "px";
    }

    // Call resize function on initial load and resize events
    resizeSvg();
    window.addEventListener("resize", resizeSvg);
});


// Gene Search

document.addEventListener("DOMContentLoaded", function() {

const searchInput = document.getElementById('searchInput');
const suggestions = document.getElementById('suggestions');


searchInput.addEventListener('input', function() {
    const userInput = this.value.toLowerCase();
    const matchedWords = Array.from(gene_search_list).filter(word => word.toLowerCase().includes(userInput));
    displaySuggestions(matchedWords);
});

function displaySuggestions(matches) {
    if (matches.length === 0) {
        suggestions.style.display = 'none';
        return;
    }

    const suggestionsHTML = matches.map(match => `<div class="suggestion"><a href="/glycoenzdb/human/${match}">${match}</a></div>`).join('');
    suggestions.innerHTML = suggestionsHTML;
    suggestions.style.display = 'block';

    const suggestionItems = document.querySelectorAll('.suggestion');
    suggestionItems.forEach(item => {
        item.addEventListener('click', function() {
            searchInput.value = this.textContent;
            suggestions.style.display = 'none';
        });
    });
}

// Hide suggestions when clicking outside the input and suggestions div
document.addEventListener('click', function(e) {
    if (e.target !== searchInput && e.target !== suggestions) {
        suggestions.style.display = 'none';
    }
});

});

var originalCoordinates = {}; // Store original coordinates

// Function to resize the area coordinates based on the image size
function resizeAreas() {
   var image = document.getElementById('resizableImage');
   if (!image) {
    return;
   }
   var map = document.getElementById('resizableMap');
   var areas = map.getElementsByTagName('area');

   // Store original coordinates if not already stored
   if (!originalCoordinates[image.src]) {
      originalCoordinates[image.src] = [];
      for (var i = 0; i < areas.length; i++) {
         originalCoordinates[image.src][i] = areas[i].getAttribute('coords').split(',').map(Number);
      }
   }

   var scaleFactorX = image.width / image.naturalWidth;
   var scaleFactorY = image.height / image.naturalHeight;

   // Loop through each area and update coordinates
   for (var i = 0; i < areas.length; i++) {
      var originalCoords = originalCoordinates[image.src][i];
      var adjustedCoords = originalCoords.map(function(coord, index) {
         return (index % 2 === 0) ? coord * scaleFactorX : coord * scaleFactorY;
      });
      areas[i].setAttribute('coords', adjustedCoords.join(','));
   }
}

// Resize areas on image load and resize
window.addEventListener('load', resizeAreas);
window.addEventListener('resize', resizeAreas);

function resetGenes() {
    localStorage.removeItem('key');
    document.getElementById("Gene_Names_list").innerHTML = "";

    const elements = document.querySelectorAll('.show');
    for(let i=0; i<elements.length; i++) {
        clear_link_styles(elements[i])
        let mycollapse = new bootstrap.Collapse(elements[i]);
        mycollapse.hide();
    }

}

function open_pathway_submenu(key) {
    resetGenes()
    showPathways();
    localStorage.setItem('key', key);

    const key_arr = key.split("_");

    for (i = 0; i < n_subclass; i++) {
        if(key_arr[i] === "NULL"){
            break;
        }
        const id = [...key_arr].splice(0, i+1).join("_") + ("_NULL".repeat(n_subclass - i - 1));
        const element = document.getElementById(id);

        if (element) {
            const DOWN_ARROW = '▼';
            let spanElement = element.querySelector('span');
            if (spanElement == null || spanElement.innerText !== DOWN_ARROW) {
                setTimeout( () => {element.click();}, 10);
            }
        }
    }
    
}

function open_submenu_and_pathway_figures(pathway_no, slide_no) {

    keys = slide_to_pathway_mapping[pathway_no]
    localStorage.setItem('pathway_slide',slide_no);
    document.getElementById("open_submenu_buttons").innerHTML = "";

    if (keys.length == 1) {
        open_pathway_submenu(keys[0])
    } else {
        var element = document.getElementById("open_submenu_buttons");
            // Loop through the list of button names
        for (let i = 0; i < keys.length; i++) {
            // Create a new button element
            var button = document.createElement("button");
            // Set the button text to the current button name
            button_text = keys[i].replaceAll('_NULL','').trim().replaceAll('_',' > ');
            button.innerHTML = "Open " + button_text;
            button.style.marginBlock = "10px";
            // Set the onclick function for the button
            button.onclick = function() {
                // Call a custom function when the button is clicked
                open_pathway_submenu(keys[i])
            };

            // Append the button to the container div
            element.appendChild(button);
        }
    }

    openOverlay()
}

// Function to open the overlay
function openOverlay() {
    setCurrentPathwayiFrames('pathway_figures_iframe');
    document.getElementById('myOverlay').style.display = 'flex';
    document.getElementById('openPathwayBtn').style.display = 'flex';
    document.getElementById('pathway_map_img').style.display = 'none';
}

// Function to close the overlay
function closeOverlay() {
    resetGenes()
    document.getElementById("open_submenu_buttons").innerHTML = "";
    document.getElementById('myOverlay').style.display = 'none';
    document.getElementById('openPathwayBtn').style.display = 'none';
    document.getElementById('pathway_map_img').style.display = 'block';
}

function setCurrentPathwayiFrames(element_id) {
    const pathway_slide = localStorage.getItem('pathway_slide');

    let element = document.getElementById(element_id);
    if (element) {
        if (slide_file_path[pathway_slide]){
            element.src = pathway_figures_location + slide_file_path[pathway_slide];
        } else {
            element.src = "";
        }
    }

}