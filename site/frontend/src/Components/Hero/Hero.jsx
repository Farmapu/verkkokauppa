import React from "react";
import './Hero.css';

const Hero = () => {
    return(
        <div className='hero'>
            <div className="heroLeft">
                <h2>Vau uusinta uutta</h2>
                <div>
                    <p>Yritys</p>
                    <p>julkasi</p>
                    <p>uusia prossuja</p>
                </div>
                <div className="heroLatestButton">
                    <div>Katso heti</div>

                </div>
            </div>
            <div className="heroRight">

            </div>
        </div>
    )
}

export default Hero