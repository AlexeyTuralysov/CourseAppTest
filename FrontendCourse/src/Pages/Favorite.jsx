import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/block/block-rate.scss';

export default function Favorite() {
  const [dataFavorite, setFavorite] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NTA3NDU3LCJpYXQiOjE3MzQ1MDQ0NTcsImp0aSI6ImMxZTBkMDFhZTQ4MzQyNDc5NDgzMmFhZDFiYTEzNzFiIiwidXNlcl9pZCI6MX0.g2OYRsQVJLiEGeA3LvjhHfs3FemgGRG3lsViM_az0XQ";
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
  }, []);

  const handleRemoveFavorite = (symbol) => {
    axios.delete(`http://localhost:8000/api/removeFavorite/${symbol}/`)
      .then(() => {
       
        setFavorite(prevFavorites => ({
          ...prevFavorites,
          rates: { ...prevFavorites.rates, [symbol]: undefined }
        }));
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
      {dataFavorite && dataFavorite.rates ? (
        Object.entries(dataFavorite.rates).map(([symbol, rate]) => (
          <div className='block-rate' key={symbol}> 
            <div className='block-rate-block'>
              <h2>{symbol} за 1 EUR</h2>
              <p>Курс: {rate}</p>
              <button onClick={() => handleRemoveFavorite(symbol)}>Удалить из избранного</button>
            </div>
          </div>
        ))
      ) : (
        <p>Нет избранных валют</p>
      )}
    </>
  );
}
