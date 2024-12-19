import { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/block/block-rate.scss';
import { FaHeartBroken } from "react-icons/fa";

export default function Favorite() {
  const [dataFavorite, setFavorite] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  const fetchFavoriteData = () => {
    const token = localStorage.getItem("accessToken");

    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    axios.get("http://localhost:8000/getfavoritebysymbols/")
      .then((res) => {
        setFavorite(res.data); 
      })
      .catch((error) => {
        console.error("Ошибка при получении избранных валют:", error);
        setError("Не удалось загрузить данные.");
      })
      .finally(() => {
        setLoading(false);
      });
  };


  useEffect(() => {
    fetchFavoriteData();
    
    

  }, []);
  


  const handleRemoveFavorite = (symbol) => {
    const token = localStorage.getItem("accessToken");
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

    axios.delete(`http://localhost:8000/api/removeFavorite/${symbol}/`)
      .then(() => {
        fetchFavoriteData(); 
      })
      .catch((error) => {
        console.error("Ошибка при удалении валюты из избранного:", error);
        setError("Не удалось удалить валюту.");
      });
  };


  if (loading) {
    return <p>Загрузка...</p>;
  }


  if (error) {
    return <p>{error}</p>;
  }

  return (
    <>
      {dataFavorite && dataFavorite.rates && Object.keys(dataFavorite.rates).length > 0 ? (

        Object.entries(dataFavorite.rates).map(([symbol, rate]) => (

          <div className='block-rate' key={symbol}> 
            <div className='block-rate-block'>
              <h2>{symbol} за 1 EUR</h2>
              <p>Курс: {rate}</p>
              <span onClick={() => handleRemoveFavorite(symbol)}><FaHeartBroken /></span>
            </div>
          </div>

        ))
      ) : (
        <p>Нет избранных валют</p>
      )}
    </>
  );
}
