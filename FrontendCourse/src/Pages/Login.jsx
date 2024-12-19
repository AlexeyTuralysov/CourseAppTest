import axios from 'axios';
import { useState } from 'react'

import { useNavigate } from "react-router";

export default function Login() {

    const [username, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();


    const handle = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post("http://localhost:8000/api/token/", {
                username,
                password,
            });


            const { access, refresh } = res.data;

            localStorage.setItem('accessToken', access);
            localStorage.setItem('refreshToken', refresh);

            
            navigate('/');

        } catch (err) {
            setError('Ошибка');
            console.log(err);
        }

    };
    return (
        <>
            <h2>Войти</h2>
            {error && <p style={{ color: 'red' }}>{error}</p>}

            <form onSubmit={handle}>
                <input
                    type="text"
                    value={username}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="имя"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="пароль"
                />
                <button type="submit">Войти</button>
            </form>

        </>
    )
}
