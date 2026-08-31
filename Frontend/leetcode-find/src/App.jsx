import { useState } from 'react'
import Hero01 from "./components/originkit/hero-01"
import './App.css'
import { Routes,Route } from 'react-router-dom'
import SearchPage from "./components/SearchPage";

function App() {
 

  return (
    <>
      <Routes>
        <Route path = "/" element =  {<Hero01/>}/>
        <Route path = "/search" element = {<SearchPage/>}/>
      </Routes>
    </>
  )
}

export default App
