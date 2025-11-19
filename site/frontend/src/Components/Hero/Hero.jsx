import React from "react";
import './Hero.css';

const Hero = () => {
    return(
        <div className='hero'>
            <div className="hero-left">
                <h2>Vau uusinta uutta</h2>
                <div>
                    <p>AMD</p>
                    <p>julkasi</p>
                    <p>uusia prossuja</p>
                </div>
                <div className="hero-latest-button">
                    <div>Katso heti</div>

                </div>
            </div>
            <div className="hero-right">

            </div>
        </div>
    )
}

export default Hero