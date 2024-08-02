import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './assets/login';
import Profile from './assets/profile';

const App = () => {
    const [token, setToken] = useState(localStorage.getItem('token') || '');
    const [refreshToken, setRefreshToken] = useState(localStorage.getItem('refreshToken') || '');

    const saveTokens = (accessToken, refreshToken) => {
        setToken(accessToken);
        setRefreshToken(refreshToken);
        localStorage.setItem('token', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
    };

    const clearTokens = () => {
        setToken('');
        setRefreshToken('');
        localStorage.setItem('token', '');
        localStorage.setItem('refreshToken', '');
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={<Login saveTokens={saveTokens} />} />
                <Route
                    path="/profile"
                    element={token ? (
                        <Profile
                            token={token}
                            refreshToken={refreshToken}
                            saveTokens={saveTokens}
                            clearTokens={clearTokens}
                        />
                    ) : (
                        <Navigate to="/login" />
                    )}
                />
            </Routes>
        </Router>
    );
}

export default App;
