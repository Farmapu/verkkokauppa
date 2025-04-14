import Header from './components/Header';
import Message from './components/Message';
import ItemList from './components/ItemList';
import { Fragment } from 'react/jsx-runtime';

function App() {
  return (
  <>
    <Header />
    <body>
      <Message />
      <ItemList />
    </body>
  </>
  )
}

export default App;