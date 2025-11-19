import React, { useState } from 'react'
import './Navbar.css'
import karry from '../Assets/karry.png'
import { Link } from 'react-router-dom';

const Navbar = () => {

    const [menu,setMenu] = useState("Koti");

    return(
        <div className='navbar'>
            <div className='nav-log'>
                {/* <img srv={logo} alt="" /> */}
                <p>Verkkokauppa</p>
            </div>
            <ul className="nav-menu">
                <li onClick={()=>{setMenu("koti")}}><Link style={{textDecoration: 'none'}} to='/'>Koti</Link>{menu==="koti"?<hr/>:<></>}</li>
                <li onClick={()=>{setMenu("prosessorit")}}><Link style={{textDecoration: 'none'}} to='/prosessori'>Prosessori</Link>{menu==="prosessorit"?<hr/>:<></>}</li>
                <li onClick={()=>{setMenu("ram")}}><Link style={{textDecoration: 'none'}} to='/ram'>RAM</Link>{menu==="ram"?<hr/>:<></>}</li>
                <li onClick={()=>{setMenu("naytonohjain")}}><Link style={{textDecoration: 'none'}} to='/naytonohjain'>Näytönohjain</Link>{menu==="naytonohjain"?<hr/>:<></>}</li>
            </ul>
            <div className="nav-login">
                <Link to='/login'><button>Login</button></Link>
                <Link to='/cart'><img src={karry} alt=""/></Link>
                <div className="nav-login-count">0</div>
            </div>
        </div>
    )
}

export default Navbar