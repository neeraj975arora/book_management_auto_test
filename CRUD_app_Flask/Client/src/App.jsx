import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Books from './Books';
import CreateBook from './CreateBook'; 
import UpdateBook from './UpdateBook';
import Nav from './Nav';

function App() {
  return (
    <BrowserRouter>
    <Nav />
      <Routes>
      <Route path="/" element={<Books />} />
        <Route path="/create" element={<CreateBook />} />
        <Route path="/update" element={<UpdateBook />} state={{ book: null }} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
