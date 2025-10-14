import axios from 'axios';
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const UpdateBook = () => {
    const location = useLocation();
    const book = location.state.book;

    const [values, setValues] = useState({
        publisher: book.publisher,
        name: book.name,
        date: book.date,
        Cost: book.cost
    });

    const navigate = useNavigate();

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.put(`http://localhost:5000/update/${book.id}`, values)
            .then(res => navigate('/'))
            .catch(err => console.log(err));
    }

    return (
        <div className='d-flex align-items-center flex-column mt-3'>
            <h2>Update Book</h2>
            <form className='wt-50' onSubmit={handleSubmit}>
                <div className="mb-3 mt-3">
                    <label htmlFor="Publisher" className="form-label">Publisher</label>
                    <input type="text"
                        className="form-control"
                        placeholder="Enter Publisher name"
                        name="publisher"
                        value={values.publisher}
                        onChange={(e) => setValues({ ...values, publisher: e.target.value })}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="Book name" className="form-label">Book name:</label>
                    <input type="text"
                        className="form-control"
                        placeholder="Enter Book name"
                        name="name"
                        value={values.name}
                        onChange={(e) => setValues({ ...values, name: e.target.value })}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="Publish date" className="form-label">Publish Date:</label>
                    <input type="date"
                        className="form-control"
                        name="date"
                        value={values.date}
                        onChange={(e) => setValues({ ...values, date: e.target.value })}
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="Cost" className="form-label">Book name:</label>
                    <input type="text"
                        className="form-control"
                        placeholder="Rupees"
                        name="Cost"
                        value={values.cost}
                        onChange={(e) => setValues({ ...values, Cost: e.target.value })}
                    />
                </div>
                <button type="submit" className="btn btn-primary">Update</button>
            </form>
        </div>
    );
}

export default UpdateBook;