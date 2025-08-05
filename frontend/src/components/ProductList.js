import React, { useState, useEffect } from "react";
import API from "../services/api";
const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await API.get("/products"); // Appel API
        setProducts(response.data);
      } catch (error) {
        console.error("Erreur:", error);
      }
    };
    fetchProducts();
  }, []);

  return (
    <div>
      <h2>Produits</h2>
      <ul>
        {products.map((product) => (
          <li key={product.id}>
            {product.name} - {product.price}€
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ProductList;