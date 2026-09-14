import { CartProduct } from "./product";
export default function CartPage({
  cartProducts,
  total,
  onRemove,
  onIncrease,
  onDecrease,
  onCheckout,
}) {
  return (
    <div>
      <h2>Your Shopping Cart</h2>
      {cartProducts.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div>
          {cartProducts.map((item, index) => (
            <CartProduct
              key={`${item.id}-${index}`}
              item={item}
              onRemove={onRemove}
              onIncrease={onIncrease}
              onDecrease={onDecrease}
            />
          ))}
          <h3>total: {total.toFixed(2)}</h3>
          <button onClick={onCheckout}>checkout</button>
        </div>
      )}
    </div>
  );
}
