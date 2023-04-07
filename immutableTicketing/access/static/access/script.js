// Add scroll event to the window to make the menu fixed when scrolling
window.addEventListener('scroll', function() {
    var header = document.querySelector('header');
    header.classList.toggle('sticky', window.scrollY > 0);
    });

    // checkout
// Initialize the quantity and price variables
let quantity = 1;
const price = 55;

// Select the necessary HTML elements
const quantityEl = document.getElementById('quantity');
const totalEl = document.getElementById('total');

// Update the quantity and total when the +/- buttons are clicked
function updateQuantity(change) {
  // Only update the quantity if it is within the range of 1 to 10
  if (quantity + change >= 1 && quantity + change <= 10) {
    quantity += change;
    quantityEl.innerHTML = quantity;
    totalEl.innerHTML = (quantity * price).toFixed(2) + " SAR";
  }
}

// Add event listeners to the +/- buttons
document.getElementById('minus').addEventListener('click', () => updateQuantity(-1));
document.getElementById('plus').addEventListener('click', () => updateQuantity(1));
