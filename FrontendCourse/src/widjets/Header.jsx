import { Link } from 'react-router'; 


import '../styles/block/sidebar.scss'
import '../styles/widjets/Header.scss'

export default function Header() {

  return (
    <>
      <div className="header">
        <Link to="/">Главная</Link>
        <Link to="/favorite">Избранное</Link>
       
      </div>

     
    </>
  );
}
