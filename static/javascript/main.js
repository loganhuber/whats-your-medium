document.addEventListener("DOMContentLoaded", () => {
    loadImgs()
    openSelectedCategory()
    openModalOnImageClick()
})

// Function to open modal when an image is clicked
function openModalOnImageClick() {
    const modal = document.getElementById('modal-center');
    const modalImage = document.getElementById('modal-image');
    const modalTitle = document.getElementById('modal-title');

    document.querySelectorAll('.img-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const imgSrc = link.getAttribute('data-img-src');
            // const imgTitle = link.getAttribute('data-img-title');
            const description = link.getAttribute('data-img-description');
            console.log("description:", description);
            modalImage.src = imgSrc;
            // modalTitle.textContent = imgTitle;
            const modalDescription = document.getElementById('modal-description');
            modalDescription.textContent = description;
        });
    });
}

function openSelectedCategory() {
    const params = new URLSearchParams(window.location.search);
    const selected = params.get("category_id");
    console.log(selected)
    const btn = document.querySelector(`.portfolio-btn[data-bs-target='#cat-${selected}']`)
    if (!btn) return;
    if (selected) btn.click();
}


function loadImgs() {
  const imgs = document.querySelectorAll('.portfolio-image');

  imgs.forEach((img) => {
    const show = () => {
      requestAnimationFrame(() => {
        img.classList.add('visible');
      });
    };

    if (img.complete) {
      show();
    } else {
      img.onload = show;
    }
  });
}