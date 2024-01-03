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
            symbol_span.innerHTML = RIGHT_ARROW;

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

window.onload = function() {
    const ele = document.getElementById('sc_violin_iframe');
    if (!ele){
        return;
    }
    var currentUrl = window.location.href;
    var segments = currentUrl.split('/');
    var subpath = segments[segments.length - 2];
    console.log(subpath)
    var newUrl = `/violinplots?gene_name=${subpath}`;
    ele.src = newUrl;
  }

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