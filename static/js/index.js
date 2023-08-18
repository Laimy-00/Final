<script>
    document.addEventListener("DOMContentLoaded", function() {
        var newsFeed = document.getElementById("newsFeed");
        var toggleButton = document.getElementById("toggleButton");

        toggleButton.addEventListener("click", function() {
            if (newsFeed.style.display === "none") {
                newsFeed.style.display = "block";
            } else {
                newsFeed.style.display = "none";
            }
        });
    });
</script>