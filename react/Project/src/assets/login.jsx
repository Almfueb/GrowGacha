import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
const Login = ({ saveTokens }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const login = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5000/login', {username, password});
            saveTokens(response.data.access_token, response.data.refresh_token);
            navigate('/profile');
        } catch (error) {
            setMessage('Login Failed');
        }
    };

    return (
        <div>
            <h1>Login</h1>
            <input 
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            />
            <input 
            type="text"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            />

            <button onClick={login}>Login</button>
            <p>{message}</p>
            
        </div>
    );
};

export default Login;