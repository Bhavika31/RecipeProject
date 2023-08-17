const ratingInputs = document.querySelectorAll('.rating input');

ratingInputs.forEach(input => {
    input.addEventListener('click', () => {
        // Clear previous checked states
        ratingInputs.forEach(input => input.checked = false);
        
        // Mark selected star as checked
        input.checked = true;
    });
});
