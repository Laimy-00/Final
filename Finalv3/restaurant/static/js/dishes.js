<script>
    document.addEventListener("DOMContentLoaded", function() {
        var rowHeight = document.querySelector('.img-for-myrest').clientHeight;
        var images = document.querySelectorAll('.img-for-myrest');
        for (var i = 0; i < images.length; i++) {
            images[i].style.height = rowHeight + 'px';
            images[i].style.width = '100%';
            images[i].style.margin = '5px';
            images[i].style.objectFit = 'cover';
        }
    });
</script>