import { useState } from "react";

function CreateProduct(props) {
  const [newProduct, setNewProduct] = useState({
    name: "",
    price: "",
    img_url: "",
  });
  return (
    <form onSubmit={props.onSubmit} className="newProduct">
      <h2>new product</h2>
      <input
        type="text"
        name="name"
        placeholder="product name"
        value={props.newProduct.name}
        onChange={props.onChange}
      />
      <input
        type="number"
        placeholder="price"
        name="price"
        value={props.newProduct.price}
        onChange={props.onChange}
      />
      <input
  type="file"
  name="image"
  accept="image/*"
  onChange={(e) =>
    props.onChange({
      target: {
        name: "image",
        value: e.target.files[0], 
      },
    })
  }
/>
      <button type="submit">Add Product</button>
    </form>
  );
}

export default CreateProduct;
