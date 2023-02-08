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
    showFunctions();
    document.querySelectorAll('.sidebar .nav-link').forEach(function (element) {

        element.addEventListener('click', function (e) {
            console.log(element)
            let nextEl = element.nextElementSibling;
            let parentEl = element.parentElement;

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

