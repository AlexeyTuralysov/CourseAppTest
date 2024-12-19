import Favorite from "./Pages/Favorite"
import Index from "./Pages/Index"

import {  Routes, Route } from "react-router";
import Header from "./widjets/Header";
import './styles/global.scss'
import Login from "./Pages/Login";
function App() {


  return (
    <>
      <Header />

      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/favorite" element={<Favorite />} />
        <Route path="/login" element={<Login />} />
      </Routes>
      
    </>
  )
}

export default App
