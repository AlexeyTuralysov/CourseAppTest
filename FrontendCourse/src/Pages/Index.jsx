import React, { useEffect } from 'react'
import axios from "axios";
import '../styles/block/block-rate.scss'

import { useState } from 'react'
export default function Index() {
    const [data, setData] = useState([]);

    useEffect(() => {
    const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NTA1MjI5LCJpYXQiOjE3MzQ1MDIyMjksImp0aSI6IjRmN2I1MzIxZTg5ODQzOTA4NDcwMDc4YWVhZTRlODI4IiwidXNlcl9pZCI6MX0.UJacHyIOG9Kft-axQ6FM3nYEldnmmxaUOc6pGj_Sa3E"
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
        axios.get("http://localhost:8000/currency-rates/")

            .then((res) => {

                setData(res.data);
                console.log("данные", data);
            });

    }, []);


    const handleAddFavoryte = (name) => {

        console.log(name);

        const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM0NTA1MjI5LCJpYXQiOjE3MzQ1MDIyMjksImp0aSI6IjRmN2I1MzIxZTg5ODQzOTA4NDcwMDc4YWVhZTRlODI4IiwidXNlcl9pZCI6MX0.UJacHyIOG9Kft-axQ6FM3nYEldnmmxaUOc6pGj_Sa3E"
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`

        axios.post("http://localhost:8000/course-add/", {
            "currency": `${name}`
        })

        .then((res) => {
            console.log("добавлено");
        })




    };

    return (
        <>

            <h1>Валюты</h1>
            {data && data.map((item) => (
                    <div className='block-rate'>

                        <div className='block-rate-block'>

                            <h1>{item.code}</h1>
                            <h2>{item.course} за 1 EUR'о</h2>
                            <button onClick={() => handleAddFavoryte(item.name)}>в избранное</button>

                        </div>
                    </div>
                ))}


        </>
    )
}
