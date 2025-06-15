import React from "react";
import { Routes, Route, BrowserRouter, Navigate } from "react-router-dom";
import ResultScreen from "./pages/ResultScreen";
import Home from "./pages/Home";
import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute"
import Register from "./pages/Register";
import Navbar from "./components/Navbar"; // Import your Navbar

function Logout() {
  localStorage.clear()
  return <Navigate to="/" />
}

function RegisterAndLogout() {
  localStorage.clear()
  return <Register />
}

const App = () => {
  return (
    <BrowserRouter>
      <Navbar /> 
      <Routes>
        <Route path="/" element={<Home />} /> 
        <Route path="/logout" element={<Logout />} />
        <Route path="/results" element={<ProtectedRoute><ResultScreen /></ProtectedRoute>} /> 
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<RegisterAndLogout />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;