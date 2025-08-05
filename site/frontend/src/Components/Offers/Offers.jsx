import React from "react";
import './Offers.css'
import exclusive_image from "../Assets/herkullista-joulua-kaikille-montako-laitetaan.webp"

const Offers = () => {
    return(
        <div className="offers">
            <div className="offers-left">
                <h1>Henkilökohtaisia</h1>
                <h1>tarjouksia</h1>
                {/*<p>Only on best sellers</p>*/}
                <button>Katso heti</button>
            </div>
            <div className="offers-right">
                <img src={exclusive_image} alt="" />
            </div>
        </div>
    )
}

export default Offers