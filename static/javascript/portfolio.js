// this script handles all the image stuff on portfolio.html

// elements
const modal = document.getElementById('modal-center');
const modalImage = document.getElementById('modal-image');
const modalTitle = document.getElementById('modal-title');
const container = document.querySelector('.masonry-container')
const loadBtn = document.querySelector('.load-more-btn');
const portfolioTabs = document.querySelector('.portfolio-tabs')

// paired with getMoreImages to choose how many more pictures to grab
const offsets = {} // example {current_id:10}

// grabs the image and description for the modal
function handleModal(e) {
    const link = e.target.closest(".img-link")
    if (!link) return;
    const imgSrc = link.getAttribute('data-img-src');
    const description = link.getAttribute('data-img-description');
    console.log("description:", description);
    modalImage.src = imgSrc;
    const modalDescription = document.getElementById('modal-description');
    modalDescription.textContent = description;
}

// handles the bootstrap masonry layout
function initMasonry(container) {
    setTimeout(() => {

      imagesLoaded(container, function() {
          new Masonry(container, {
              percentPosition: true,
              itemSelector: '.portfolio-image-container'
          });
      });
    }, 30)
}

// page starts with low rez placeholders
// after page loads this swaps for the real image
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

// aka -- load more button
async function getMoreImages() {
    const categoryId = loadBtn.dataset.categoryId;

    if (!offsets[categoryId]) {
        offsets[categoryId] = 10;
    }

    const response = await fetch(
        `portfolio/load-more?category_id=${categoryId}&offset=${offsets[categoryId]}`
    );
    const data = await response.json();
    const container = document.querySelector(`.masonry-container[data-category-id="${categoryId}"]`);

    container.insertAdjacentHTML('beforeend', data.html);
    if (offsets[categoryId] >= data.count) loadBtn.style.display = 'none';
    offsets[categoryId] += 5;

    initMasonry(container);
    loadImgs();
};

function activateTab() {
  const targetId = portfolioTabs.dataset.targetId

  const tabBtns = document.querySelectorAll('.portfolio-btn')
  tabBtns.forEach((btn) => {
    if (btn.dataset.categoryId == targetId) {
      btn.classList.add('active')
    }
  })
}

// event listeners 
loadBtn.addEventListener('click', getMoreImages);
// heads up for future you:
// the bootstrap navbar doesn't like when you e.target.closest to many things
document.addEventListener("DOMContentLoaded", () => {
  document.addEventListener('click', handleModal)
  loadImgs()
  initMasonry(container)
  activateTab()
});
