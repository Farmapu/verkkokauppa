import React from "react";
import './Offers.css'
import exclusive_image from "../Assets/RGB-Ram-Transparent.png"

const Offers = () => {
    return(
        <div className="offers">
            <div className="offersLeft">
                <h1>Henkilökohtaisia</h1>
                <h1>tarjouksia</h1>
                {/*<p>Only on best sellers</p>*/}
                <button>Katso heti</button>
            </div>
            <div className="offersRight">
                <img src={exclusive_image} className="offersRight" alt="" />
            </div>
        </div>
    )
}

export default Offers