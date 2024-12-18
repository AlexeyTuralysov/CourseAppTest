import React from 'react'
import {Link } from "react-router";
import "../styles/widjets/Header.scss"



export default function Header() {
  return (
    <div className='header'>
        <Link to="/">главная</Link>
        <Link to="/favorite">избранное</Link>
    </div>
  )
}
