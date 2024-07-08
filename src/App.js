import './App.css';

import Gall from './components/Gall';
import Navbar from './components/Navbar';
import Login from './components/Login';
import Signup from './components/Signup';
import Alert from './components/Alert';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  const imageUrls = [
    "https://picsum.photos/200/300",
    "https://picsum.photos/200/200",
    "https://picsum.photos/600/200",
    "https://picsum.photos/400/600",
    "https://picsum.photos/300/200",
    "https://picsum.photos/500/400"
  ];

  const [alert, setAlert] = useState(null);

  const showAlert = (message, type) => {
    setAlert({
      msg: message,
      type: type,
    });
    setTimeout(() => {
      setAlert(null);
    }, 1500);
  };

  return (
    <Router>
      <div className="App">
        <Navbar />
        <Alert alert={alert} />
        <Routes>
          <Route exact path="/" element={<Gall photos={imageUrls} showAlert={showAlert} />} />
          <Route exact path="/login" element={<Login showAlert={showAlert} />} />
          <Route exact path="/signup" element={<Signup showAlert={showAlert} />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
