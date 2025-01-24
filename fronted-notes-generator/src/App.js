import React from 'react'; // Добавьте этот импорт для исправления ошибки "React must be in scope"
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'; // Импортируйте роутер и маршруты
import Home from './pages/Home'; // Убедитесь, что путь к Home корректен
import Login from './pages/Login'; // Убедитесь, что путь к Login корректен
import Register from './pages/Register'; // Убедитесь, что путь к Register корректен
import UserDashboard from './pages/UserDashboard'; // Убедитесь, что путь к UserDashboard корректен

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={<UserDashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
