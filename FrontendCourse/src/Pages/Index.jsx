import { useEffect, useState } from 'react';
import axios from 'axios';
import '../styles/block/block-rate.scss';
import { FaHeart } from 'react-icons/fa';

export default function Index() {
    const [currentData, setCurrentData] = useState([]);
    const [isLoading, setIsLoading] = useState(true);  

    const token = localStorage.getItem("accessToken");

    useEffect(() => {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

        setIsLoading(true);
        axios.get("http://localhost:8000/currency-rates/")
            .then((res) => {
                setCurrentData(res.data);
                setIsLoading(false);  
            })

            .catch((error) => {
                console.error("Ошибка при загрузке данных:", error);
                setIsLoading(false);  
            });
    }, [token]);

    const handleAddFavorite = (name) => {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        axios.
        post("http://localhost:8000/course-add/", { "currency": `${name}` })
            
        .then((res) => {
                console.log("добавлено", res);
            });
    };

    return (
        <>
            <h1>Валюты</h1>
            {isLoading ? ( 
                <p>Загрузка...</p>
            ) : (
                currentData && currentData.map((item) => {
                    return (
                        <div className='block-rate' key={item.id}>
                            <div className='block-rate-block'>
                                <h1>{item.code}</h1>
                                <h2>{item.course} за 1 EUR</h2>
                                <button onClick={() => handleAddFavorite(item.name)}><FaHeart /></button>
                            </div>
                        </div>
                    );
                })
            )}
        </>
    );
}
