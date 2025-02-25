// главная

const tabs = document.querySelectorAll('.tab');
const panes = document.querySelectorAll('.tab-pane');
let currentTab = 0;
const intervals = [0, 4000, 4000];

const images = document.querySelectorAll('.image-container img');
images[0].classList.add('active');
let currentImage = 0;

setInterval(() => {
  images[currentImage].classList.remove('active');
  currentImage = (currentImage + 1) % images.length;
  images[currentImage].classList.add('active');
}, 3000);



tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const activeTab = document.querySelector('.tab.active');
    activeTab.classList.remove('active');
    tab.classList.add('active');
    const paneId = tab.getAttribute('data-pane');
    panes.forEach((pane) => {
      if (pane.getAttribute('data-pane') === paneId) {
        pane.style.display = 'block';
      } else {
        pane.style.display = 'none';
      }
    });
    const activePane = document.querySelector('.tab-pane[data-pane="' + paneId + '"]');
    const images = activePane.querySelectorAll('img');
    images.forEach((image) => {
      image.style.display = 'block';
    });
  });
});



const reviewsContainer = document.querySelector('.reviews-container');
const reviews = document.querySelectorAll('.review');
const prevButton = document.querySelector('.prev-button');
const nextButton = document.querySelector('.next-button');
let currentReview = 0;
let canScroll = true;
reviewsContainer.style.width = `${reviews.length * 30}%`;

prevButton.addEventListener('click', () => {
  currentReview--;
  if (currentReview < 0) {
    currentReview = reviews.length - 1;
  }
  reviewsContainer.style.transform = `translateX(${-currentReview * 30}%)`;
});

nextButton.addEventListener('click', () => {
  if (canScroll) {
    currentReview++;
    if (currentReview >= reviews.length) {
      currentReview = 0;
    }
    reviewsContainer.style.transform = `translateX(${-currentReview * 30}%)`;
    if (currentReview * 30 >= 70) {
      canScroll = false;
    }
  }
});

$(document).ready(function() {
  $('.tab').on('click', function() {
    var pane = $(this).attr('data-pane');
    $('.tab').removeClass('active');
    $(this).addClass('active');
    $('.tab-pane').hide();
    $('.tab-pane[data-pane="' + pane + '"]').show();
  });

  const firstTab = document.querySelector('.tab');
  firstTab.classList.add('active');
  const firstPane = document.querySelector('.tab-pane');
  firstPane.classList.add('active');
  const firstPaneImages = firstPane.querySelectorAll('img');
  firstPaneImages[0].classList.add('active');
});



