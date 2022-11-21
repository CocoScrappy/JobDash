
import "./App.css";
import react, { Component, useState, useEffect } from "react";
import axios from "axios";

function App() {
  const [applicantsList, setApplicantsList] = useState([]);
  const fetchApplicants = () => {
    axios //Axios to send and receive HTTP requests
      .get("http://localhost:8000/api/applicants/")
      .then((res) => setApplicantsList(res.data))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    fetchApplicants();
  }, []);

  const renderApplicants = () => {
    if(applicantsList.length != 0) {
    return applicantsList.map((applicant) => (
      <div key={applicant.id}>
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

  return <div className="App">{renderApplicants()}</div>;
}

export default App;
