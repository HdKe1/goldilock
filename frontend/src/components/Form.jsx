import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";

function Form({ route, method }) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const navigate = useNavigate();

    const name = method === "login" ? "Login" : "Register";

    const handleSubmit = async (e) => {
        setLoading(true);
        e.preventDefault();

        try {
            const res = await api.post(route, { username, password })
            if (method === "login") {
                localStorage.setItem(ACCESS_TOKEN, res.data.access);
                localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
                navigate("/")
            } else {
                navigate("/login")
            }
        } catch (error) {
            alert(error)
        } finally {
            setLoading(false)
        }
    };

    return (
        <div className="min-h-screen bg-black flex items-center justify-center p-4">
      <div className="w-full max-w-sm space-y-6">
        <form 
          onSubmit={handleSubmit} 
          className="space-y-6"
        >
        <h1 className="text-2xl font-light text-white text-center tracking-wide">
          {name}
        </h1>
        
        <div className="space-y-4">
          <input
            className="w-full px-0 py-3 bg-transparent border-0 border-b border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-white transition-colors duration-200"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
          
          <input
            className="w-full px-0 py-3 bg-transparent border-0 border-b border-gray-700 text-white placeholder-gray-500 focus:outline-none focus:border-white transition-colors duration-200"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
        </div>

        {loading && <div className="text-white text-center">Loading...</div>}
        
        <button 
          className="w-full py-3 mt-8 bg-transparent border border-gray-700 text-white font-light tracking-wide hover:bg-white hover:text-black transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed"
          type="submit"
          disabled={loading}
        >
          {loading ? 'Signing In...' : name}
        </button>
        </form>
      </div>
    </div>
    );
}

export default Form