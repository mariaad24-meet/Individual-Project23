document.addEventListener("DOMContentLoaded", function () {
  // Event delegation to handle "Add to Cart" button click
  document.body.addEventListener("click", function (event) {
    if (event.target.classList.contains("addToCartBtn")) {
      addToCart(event.target);
    }
  });

  // Display cart total
  updateCartTotal();
});

// Function to handle "Add to Cart" button click
function addToCart(button) {
  const productName = button.parentElement.querySelector(".productName").innerText;
  const productPrice = parseFloat(button.parentElement.querySelector(".productPrice").innerText);

  let cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
  cartItems.push({ name: productName, price: productPrice });
  localStorage.setItem("cartItems", JSON.stringify(cartItems));

  let cartTotal = parseFloat(localStorage.getItem("cartTotal"));

  if (!cartTotal) {
    cartTotal = 0.00;
  }

  cartTotal += productPrice;
  localStorage.setItem("cartTotal", cartTotal.toFixed(2));

  alert("Item added to cart!");
}

function updateCartTotal() {
  const cartTotalElement = document.getElementById("cartTotal");
  const storedCartTotal = parseFloat(localStorage.getItem("cartTotal"));

  if (storedCartTotal) {
    cartTotalElement.textContent = "$" + storedCartTotal.toFixed(2);
  } else {
    cartTotalElement.textContent = "$0.00";
  }
}

