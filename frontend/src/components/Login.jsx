import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login({ handleLogin }) {
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    const success = await handleLogin(password);
    if (success) {
      navigate("/");
    }
  };

  return (
    <div className="Product">
      <h1>enter password to login, Wasif</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="password"
          placeholder="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default Login;
