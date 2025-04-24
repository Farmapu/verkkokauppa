import Header from './components/Header';
//import ItemList from './components/ItemList';
import DisplayItem from './components/item';
import ApiTest from './components/ApiTest';
import { Fragment } from 'react/jsx-runtime';

function App() {

  return (
  <>
    <Header />
    <body>
      <DisplayItem />
      <ApiTest />
    </body>
  </>
  )
}

export default App;