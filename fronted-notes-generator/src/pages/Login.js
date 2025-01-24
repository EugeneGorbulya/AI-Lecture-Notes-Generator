// src/pages/Login.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../styles/Auth.css'; // Общие стили для Login и Register

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false); // Состояние для индикатора загрузки

  const handleLogin = async (event) => {
    event.preventDefault();
    setLoading(true); // Включаем индикатор загрузки
    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      const response = await axios.post('http://127.0.0.1:8000/api/users/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      const { access_token } = response.data;

      // Получаем информацию о текущем пользователе
      const userResponse = await axios.get('http://127.0.0.1:8000/api/users/me', {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      });

      const userId = userResponse.data.id;

      // Сохраняем токен и user_id
      localStorage.setItem('user_id', userId);
      localStorage.setItem('access_token', access_token);

      console.log('Login successful:', userResponse.data);

      setError(''); // Очищаем ошибку
      navigate('/dashboard'); // Перенаправляем на dashboard
    } catch (err) {
      console.error('Login failed:', err.response?.data?.detail || err.message);
      setError(err.response?.data?.detail || 'Something went wrong');
    } finally {
      setLoading(false); // Отключаем индикатор загрузки
    }
  };

  return (
    <div className="auth-container">
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Username</label>
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)} // Обновляем username
            required
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} // Обновляем password
            required
          />
        </div>
        {error && <p className="error">{error}</p>} {/* Отображение ошибки */}
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      {loading && <div className="loading-spinner"></div>} {/* Индикатор загрузки */}
      <p>
        Don't have an account?{' '}
        <span className="link" onClick={() => navigate('/register')}>
          Register
        </span>
      </p>
    </div>
  );
}

export default Login;
