document.addEventListener('DOMContentLoaded', function() {
    openSelectedCategory()
    loadImgs()

    document.addEventListener('click', e => openModalOnImageClick(e))

    function initMasonry(container) {
        imagesLoaded(container, function() {
            new Masonry(container, {
                percentPosition: true,
                itemSelector: '.portfolio-image-container'
            });
        });
    }

    // Initialize masonry for all containers after images load
    const masonryContainers = document.querySelectorAll('.masonry-container');
    masonryContainers.forEach(container => {
        initMasonry(container);
    });

    // Reinitialize masonry when tabs are shown
    const tabElements = document.querySelectorAll('button[data-bs-toggle="tab"]');
    tabElements.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function (event) {
            const targetId = event.target.getAttribute('data-bs-target');
            const targetContainer = document.querySelector(targetId + ' .masonry-container');
            if (targetContainer) {
                initMasonry(targetContainer);
            }
        });
    });


    const offsets = {}

    const loadBtns = document.querySelectorAll(".load-more-btn")
    loadBtns.forEach((btn) => {
        btn.addEventListener('click', async () => {
            const category_id = btn.dataset.categoryId;
            offsets[category_id] = 2
            const response = await fetch(
                `portfolio/load-more?category_id=${category_id}&offset=${offsets[category_id]}`
            )
            const data = await response.json()
            // console.log(data)
            const container = document.querySelector(`.masonry-container[data-category-id="${category_id}"]`)

            container.insertAdjacentHTML('beforeend', data.html)
            offsets[category_id] += 2
            initMasonry(container)
            loadImgs()
        })
    })
});


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

// Function to open modal when an image is clicked
function openModalOnImageClick(e) {
    // e.preventDefault();
    const modal = document.getElementById('modal-center');
    const modalImage = document.getElementById('modal-image');
    const modalTitle = document.getElementById('modal-title');

    const link = e.target.closest('.img-link');

    if (!link) return;

    const imgSrc = link.getAttribute('data-img-src');
    console.log(imgSrc)
    // const imgTitle = link.getAttribute('data-img-title');
    const description = link.getAttribute('data-img-description');
    console.log("description:", description);
    modalImage.src = imgSrc;
    // modalTitle.textContent = imgTitle;
    const modalDescription = document.getElementById('modal-description');
    modalDescription.textContent = description;

}

function openSelectedCategory() {
    const params = new URLSearchParams(window.location.search);
    const selected = params.get("category_id");
    console.log(selected)
    const btn = document.querySelector(`.portfolio-btn[data-bs-target='#cat-${selected}']`)
    if (!btn) return;
    if (selected) btn.click();
}

