import Favorite from "./Pages/Favorite"
import Index from "./Pages/Index"
import { BrowserRouter, Routes, Route } from "react-router";
import Header from "./widjets/Header";
import './styles/global.scss'
function App() {


  return (
    <>
      <Header />

      <Routes>
        <Route path="/" element={<Index />} />
        <Route path="/favorite" element={<Favorite />} />
      </Routes>
      
    </>
  )
}

export default App
