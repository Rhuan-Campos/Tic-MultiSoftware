document.addEventListener("DOMContentLoaded", () => {
    const colorPicker = document.getElementById("colorPicker");
    const colorDisplay = document.getElementById("colorDisplay");

    colorDisplay.addEventListener("click", () => {
        colorPicker.click(); 
    });

    colorPicker.addEventListener("input", () => {
        const selectedColor = colorPicker.value;
        colorDisplay.style.backgroundColor = selectedColor;
    });
});