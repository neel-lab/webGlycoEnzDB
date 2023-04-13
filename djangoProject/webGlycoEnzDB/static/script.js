function showFunctions() {
    document.getElementById("element1").style.display = "block";
    document.getElementById("element2").style.display = "none";
    document.getElementById("btnElement1").classList.add("active");
    document.getElementById("btnElement2").classList.remove("active");
}

function showPathways() {
    document.getElementById("element1").style.display = "none";
    document.getElementById("element2").style.display = "block";
    document.getElementById("btnElement1").classList.remove("active");
    document.getElementById("btnElement2").classList.add("active");
}

document.addEventListener("DOMContentLoaded", function () {
    const RIGHT_ARROW = '▶';
    const DOWN_ARROW = '▼';

    showFunctions();
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

