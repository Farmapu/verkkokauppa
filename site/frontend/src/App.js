import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Navbar from './Components/Navbar/Navbar';
import Koti from './Pages/Koti';
import KotiKategoria from './Pages/KotiKategoria';
import Tuote from './Pages/Tuote';
import Cart from './Pages/Cart';
import Login from './Pages/Login';
import Chatbot from './Components/Chatbot/Chatbot';

function App() {
  return (
    <div>
      <BrowserRouter>
        <Navbar/>
        <Chatbot/>
        <Routes>
          <Route path='/' element={<Koti/>}></Route>
          <Route path='/prosessori' element={<KotiKategoria category="prosessori"/>}></Route>
          <Route path='/ram' element={<KotiKategoria category="ram"/>}></Route>
          <Route path='/naytonohjain' element={<KotiKategoria category="naytonohjain"/>}></Route>
          <Route path='/tuote' element={<Tuote/>}>
            <Route path=':productId' element={[<Tuote/>]}></Route>
          </Route>
          <Route path='/cart' element={<Cart/>}></Route>
          <Route path='/login' element={<Login/>}></Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
