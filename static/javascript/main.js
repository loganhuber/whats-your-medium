document.addEventListener("DOMContentLoaded", () => {
    
    openSelectedCategory()
})

function openSelectedCategory() {
    const params = new URLSearchParams(window.location.search);
    const selected = params.get("category_id");
    console.log(selected)
    const btn = document.querySelector(`.portfolio-btn[data-bs-target='#${selected}']`)
    if (!btn) return;
    if (selected) btn.click();
}