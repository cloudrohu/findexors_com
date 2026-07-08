document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".inline-group > h2").forEach(function (heading) {

        const inline = heading.parentElement;

        heading.classList.add("inline-title");

        const body = document.createElement("div");
        body.className = "inline-body";

        while (heading.nextSibling) {
            body.appendChild(heading.nextSibling);
        }

        inline.appendChild(body);

        heading.addEventListener("click", function () {
            inline.classList.toggle("open");
        });

    });

});