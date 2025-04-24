import { MouseEvent } from "react";

function ItemList() {
  const items = ["näytönohjain", "prosessori", "emolevy", "ram"];

  const handleClick = (event: MouseEvent) => console.log(event);

  return (
    <>
      <ul className="">
        {items.map((item, index) => (
          <li
            className=""
            key={item}
            onClick={handleClick}
          >
            {item}
          </li>
        ))}
      </ul>
    </>
  );
}

export default ItemList;
