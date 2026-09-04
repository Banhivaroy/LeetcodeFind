import { useState } from 'react'
import Hero01 from "./components/originkit/hero-01"
import './App.css'
import { Routes,Route } from 'react-router-dom'
import SearchPage from "./components/SearchPage";
import ResponsePage from "./components/ResponsePage";

function App() {
 
  const [darkMode,setDarkMode] = useState(false);
  return (
    <>
      <Routes>
        <Route path = "/" element =  {<Hero01/>}/>
        <Route path = "/search" element = {
          <SearchPage
          darkMode={darkMode}
          setDarkMode={setDarkMode}
          />
          }/>
        <Route path = "/results" element = {
          <ResponsePage
          darkMode={darkMode}
          setDarkMode={setDarkMode}
        />}/>
      </Routes>
    </>
  )
}

export default App
