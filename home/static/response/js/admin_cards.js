document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".change-list .results table tbody tr").forEach(row => {
        let statusCell = row.querySelector("td:nth-child(2) select"); // 2nd column = status select
        if (statusCell) {
            function applyColor(value) {
                row.classList.remove("card-completed", "card-pending", "card-rejected");

                value = value.toLowerCase();
                if (value.includes("meeting")) {
                    row.classList.add("card-completed");
                } else if (value.includes("pending")) {
                    row.classList.add("card-pending");
                } else if (value.includes("rejected")) {
                    row.classList.add("card-rejected");
                }
            }

            // Initial load
            applyColor(statusCell.value);

            // On change
            statusCell.addEventListener("change", function() {
                applyColor(this.value);
            });
        }
    });
});
