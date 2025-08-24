// Βρίσκει όλα τα checkboxes και προσθέτει event listener
document.querySelectorAll("input[type='checkbox']").forEach(function(checkbox) {
    // Όταν αλλάζει η κατάσταση του checkbox
    checkbox.addEventListener('change', function() {
       let id = this.dataset.id;  // Παίρνει το ID του todo από το data-id attribute
       // Ανακατευθύνει στο route για αλλαγή κατάστασης
       window.location.href = '/changestatus/' + id;
    }); 
});