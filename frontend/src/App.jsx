import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import Home from "./pages/Home"
import Model from "./pages/Model"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/model/:query" element={<Model />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
