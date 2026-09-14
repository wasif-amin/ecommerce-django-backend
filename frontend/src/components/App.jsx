import React, { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Product } from "./product";
import CreateProduct from "./CreateProduct";
import CartPage from "./CartPage";
import Navbar from "./Navbar";
import Login from "./Login";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5001";

function App() {
  const [isAdmin, setIsAdmin] = useState(false);
  const [products, setProducts] = useState(null);
  const [cartProducts, setCartProducts] = useState([]);
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    img_url: "",
  });

  function handleChange(event) {
    const { name, value } = event.target;
    setNewProduct((prevproduct) => {
      return {
        ...prevproduct,
        [name]: value,
      };
    });
  }

  const getSessionId = () => {
    let sessionId = localStorage.getItem("cart_session_id");
    if (!sessionId) {
      sessionId = crypto.randomUUID();
      localStorage.setItem("cart_session_id", sessionId);
    }
    return sessionId;
  };

  function handleAddToStore(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append("name", newProduct.name);
    formData.append("price", newProduct.price);
    formData.append("image", newProduct.image);
    fetch(`${API_BASE_URL}/api/add-product`, {
      method: "POST",
      body: formData,
      credentials: "include",
    })
      .then(() => {
        return fetch(`${API_BASE_URL}/api/products`);
      })
      .then((res) => res.json())
      .then((data) => {
        setProducts(data);
        setNewProduct({ name: "", price: "", image: null });
      })
      .catch((err) => console.error("Error:", err));
  }

  async function handleAddToCart(event, productID) {
    event.preventDefault();
    const sessionId = getSessionId();
    try {
      const response = await fetch(`${API_BASE_URL}/api/add/cart`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          product_id: productID,
        }),
      });
      if (response.ok) {
        const cartResponse = await fetch(
          `${API_BASE_URL}/api/cart-products?session_id=${sessionId}`
        );
        const cartData = await cartResponse.json();
        setCartProducts(cartData);
      }
    } catch (err) {
      console.error("Error:", err);
    }
  }

  async function handleRemoveFromCart(productId) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/remove-from-cart/${productId}`,
        {
          method: "DELETE",
        }
      );
      if (response.ok) {
        setCartProducts((prevProducts) =>
          prevProducts.filter((item) => item.id !== productId)
        );
      }
    } catch (err) {
      console.error("Error removing item:", err);
    }
  }

  async function handleRemoveFromStore(productId) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/remove-from-store/${productId}`,
        {
          method: "DELETE",
          credentials: "include",
        }
      );
      if (response.ok) {
        setProducts((prevProducts) =>
          prevProducts.filter((p) => p.id !== productId)
        );
      }
    } catch (err) {
      console.error("Error removing item:", err);
    }
  }

  async function handleIncrease(id) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/update-cart-item/${id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ change: 1 }),
        }
      );
      if (response.ok) {
        setCartProducts((prevCart) =>
          prevCart.map((item) =>
            item.id === id ? { ...item, quantity: item.quantity + 1 } : item
          )
        );
      }
    } catch (err) {
      console.error("Error increasing quantity:", err);
    }
  }

  async function handleDecrease(id) {
    try {
      const response = await fetch(
        `${API_BASE_URL}/api/update-cart-item/${id}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ change: -1 }),
        }
      );

      if (response.ok) {
        setCartProducts((prevCart) =>
          prevCart.map((item) =>
            item.id === id ? { ...item, quantity: item.quantity - 1 } : item
          )
        );
      }
    } catch (err) {
      console.error("Error decreasing quantity:", err);
    }
  }

  async function handleLogin(password) {
    try {
      const response = await fetch(`${API_BASE_URL}/api/wasif-login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
        credentials: "include",
      });

      if (response.ok) {
        setIsAdmin(true);
        return true;
      } else {
        alert("Incorrect password!");
        return false;
      }
    } catch (err) {
      console.error("Login failed:", err);
      return false;
    }
  }

  async function handleLogout() {
    setIsAdmin(false);
  }

  async function handleCheckout() {
    try {
      const sessionId = getSessionId();
      const response = await fetch(`${API_BASE_URL}/api/checkout-session`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          items: cartProducts,
          session_id: sessionId,
        }),
      });

      const data = await response.json();

      if (data.url) {
        window.location.href = data.url;
      } else {
        console.error("Failed to create checkout session");
      }
    } catch (error) {
      console.error("Error during checkout:", error);
    }
  }

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/products`)
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch((err) => console.error("Error fetching products:", err));
  }, []);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/check-auth`, { credentials: "include" })
      .then((res) => res.json())
      .then((data) => {
        setIsAdmin(data.isAdmin);
      })
      .catch((err) => console.error("Error checking auth:", err));
  }, []);

  useEffect(() => {
    const sessionId = getSessionId();

    fetch(`${API_BASE_URL}/api/cart-products?session_id=${sessionId}`)
      .then((res) => res.json())
      .then((data) => {
        if (!data.error && Array.isArray(data)) {
          setCartProducts(data);
        } else {
          setCartProducts([]);
        }
      })
      .catch((err) => console.error("Error loading cart:", err));
  }, []);

  const cartTotal = cartProducts.reduce(
    (sum, item) => sum + item.price * (item.quantity || 1),
    0
  );

  if (!products) {
    return <p>Loading product...</p>;
  }

  return (
    <BrowserRouter>
      <Navbar />

      <Routes>
        <Route
          path="/"
          element={
            <div>
              {isAdmin && (
                <>
                  <button onClick={handleLogout}>logout</button>
                  <CreateProduct
                    onChange={handleChange}
                    onSubmit={handleAddToStore}
                    newProduct={newProduct}
                  />
                </>
              )}
              {products.map((product, index) => (
                <Product
                  key={index}
                  name={product.name}
                  price={product.price}
                  img={product.image_url}
                  isAdmin={isAdmin}
                  onAddToCart={(event) => handleAddToCart(event, product.id)}
                  onRemove={() => handleRemoveFromStore(product.id)}
                />
              ))}
            </div>
          }
        />
        <Route path="/Login" element={<Login handleLogin={handleLogin} />} />
        <Route
          path="/CartPage"
          element={
            <CartPage
              cartProducts={cartProducts}
              total={cartTotal}
              onRemove={handleRemoveFromCart}
              onIncrease={handleIncrease}
              onDecrease={handleDecrease}
              onCheckout={handleCheckout}
            />
          }
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
