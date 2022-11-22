import "./App.css";
import  { useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [applicantsList, setApplicantsList] = useState([]);
  const fetchApplicants = async () => {
    await axios //Axios to send and receive HTTP requests
      .get("http://localhost:8000/api/users/default/")
      .then((res) =>{
        console.log(res.data);
       setApplicantsList(res.data)})
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchApplicants();
  }, []);

  const updateUser = (id) => {
    const data = {
      first_name: "Elie[edited]",
      last_name: "Mambou",
      email: "elie@gmail.com",
      summary: "worst teacher ever",
      password: "hunter",
      role: "user",
    };
    axios //Axios to send and receive HTTP requests
      .put(`http://localhost:8000/api/users/default/${id}/`, data)
      .then((res) => fetchApplicants())
      .catch((err) => console.log(err));
  };

  const deleteUser = (id) => {
    axios //Axios to send and receive HTTP requests
      .delete(`http://localhost:8000/api/users/default/${id}/`)
      .then((res) => fetchApplicants())
      .catch((err) => console.log(err));
  };

  const postUser = (id) => {
    const data = {
      first_name: "Post",
      last_name: "Person",
      email: "post2@RESTframework.com",
      summary: "a test for post from frontend",
      password: "hunter",
      role: "user",
    };
    axios //Axios to send and receive HTTP requests
      .post(`http://localhost:8000/api/users/default/`, data)
      .then((res) => fetchApplicants())
      .catch((err) => console.log(err));
  };

  const renderUsers = () => {
    if (applicantsList.length !== 0) {
      return applicantsList.map((applicant) => (
        <div key={applicant.id}>
         <p>
            <strong>Id: </strong> {applicant.id}
          </p>
          <p>
            <strong>First Name: </strong> {applicant.first_name}
          </p>
          <p>
            <strong>Last Name: </strong> {applicant.last_name}
          </p>
          <p>
            <strong>Email: </strong> {applicant.email}
          </p>
          <br></br>
        </div>
      ));
    }
  };

  return <div className="App">
  <div>
  {renderUsers()}
  </div>
  <div>
    <button onClick={() => {updateUser(1)}}>Update</button>
  </div>
  <div>
    <button onClick={() => {deleteUser(4)}}>Delete</button>
  </div>
  <div>
    <button onClick={() => {postUser()}}>Post</button>
  </div>
  </div>;
}

export default App;
