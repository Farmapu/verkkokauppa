function ItemList() {
    const items = [
        'näytönohjain',
        'prosessori',
        'emolevy',
        'ram'
    ]

    return (
        <>
            <ul className="">
                {items.map(item => <li>{item}</li>)}
            </ul>
        </>
    )

}

export default ItemList;