const allCheckbox = document.getElementById("selected-all");

allCheckbox.addEventListener('change', (e) => {
    const rowCheckboxes = document.getElementsByClassName("selected-row");

    for (let i = 0; i < rowCheckboxes.length; i++) {
       rowCheckboxes[i].checked = e.target.checked;
    }
});
