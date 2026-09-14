import React from "react";
import "../styles.css";

function Product({ name, price, img, onAddToCart, onRemove, isAdmin }) {
  return (
    <div className="Product">
      <h1>{name}</h1>
      <img src={img} alt={name} style={{ width: "200px", height: "200px" }} />

      <p>price: ${price}</p>
      <div className="button-container">
        <button onClick={onAddToCart}>add to cart</button>
        {isAdmin && <button onClick={onRemove}>Delete from store</button>}
      </div>
    </div>
  );
}
function CartProduct({ item, onRemove, onIncrease, onDecrease }) {
  return (
    <div className="cartProduct">
      <h1>{item.name}</h1>
      <img
        src={item.image_url}
        alt={item.name}
        style={{ width: "200px", height: "200px" }}
      />
      <p>quantity: {item.quantity}</p>
      <button onClick={() => onIncrease(item.id)}>+</button>
      <button onClick={() => onDecrease(item.id)}>-</button>
      <p>{item.price}</p>
      <button onClick={() => onRemove(item.id)}>remove from cart</button>
    </div>
  );
}
export { Product, CartProduct };
