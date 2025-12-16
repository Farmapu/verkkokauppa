import React from "react";
import './Item.css'

const Item = (props) => {
    return(
        <div className="item">
            <img className="product" src={props.image} alt=""/>
            <p>{props.name}</p>
            <div className="itemPrices">
                <div className="itemPriceNew">
                    €{props.new_price}
                </div>
                <div className="itemPriceOld">
                    €{props.old_price}
                </div>
            </div>
        </div>
    )
}

export default Item