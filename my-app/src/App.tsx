import React from 'react';
import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react';
import api from './api';


function App() {
  const [patients, setPatients] = useState<string[]>([""])
  const [patientConcepts, setPatientConcepts] = useState<string[]>(["diagnoses, medications, recommendations"])
  const [selectedPatient, setSelectedPatient] = useState<string>("")

  const [doctorDiagnoses, setDoctorDiagnoses] = useState<{ [fieldName: string]: string[] }>({})
  const [doctorRecommendations, setDoctorRecommendations] = useState<{ [fieldName: string]: string[] }>({})
  const [doctorMedications, setDoctorMedications] = useState<{ [fieldName: string]: string[] }>({})

  const [dateDiagnoses, setDateDiagnoses] = useState<{ [fieldName: string]: string[] }>({})
  const [dateRecommendations, setDateRecommendations] = useState<{ [fieldName: string]: string[] }>({})
  const [dateMedications, setDateMedications] = useState<{ [fieldName: string]: string[] }>({})

  const [filterDiagnoses, setFilterDiagnoses] = useState<{ [fieldName: string]: string[] }>({})
  const [filterRecommendations, setFilterRecommendations] = useState<{ [fieldName: string]: string[] }>({})
  const [filterMedications, setFilterMedications] = useState<{ [fieldName: string]: string[] }>({})

  const [diagnosisAttribute, setDiagnosisAttribute] = useState<string>("Date")
  const [recAttribute, setRecAttribute] = useState<string>("Date")
  const [medAttribute, setMedAttribute] = useState<string>("Date")

  let options = ["Date", "Doctor", "Specialty"]



  const populateDashboards = async function (e: React.MouseEvent<HTMLButtonElement>): Promise<void> {
    e.preventDefault()

    const response = await api.get('/notes')
    const data = response.data.Notes
    console.log(response)

    //TODO: need to build a typescript frontend client for this 
    type DoctorDiagnoses = { [dict_key: string]: string[] }
    type DoctorRecs = { [dict_key: string]: string[] }
    type DoctorMeds = { [dict_key: string]: string[] }

    type DateDiagnoses = { [dict_key: string]: string[] }
    type DateRecs = { [dict_key: string]: string[] }
    type DateMeds = { [dict_key: string]: string[] }


    let doc_diagnoses: DoctorDiagnoses = {}
    let date_diagnoses: DateDiagnoses = {}

    let doc_recs: DoctorRecs = {}
    let date_recs: DateRecs = {}

    let doc_meds: DoctorMeds = {}
    let date_meds: DateMeds = {}

    for (let key in Object.keys(data)) {
      let diagnoses_from_one_note = data[key]["diagnoses"]


      if (diagnoses_from_one_note.length !== 0) {
        let doctor = data[key]["metadata"]["doctor"]
        if (doctor in doc_diagnoses) {
          doc_diagnoses[doctor] = doc_diagnoses[doctor].concat(diagnoses_from_one_note)
        }
        else {
          doc_diagnoses[doctor] = diagnoses_from_one_note
        }
        let date = data[key]["metadata"]["date"]

        if (date in date_diagnoses) {
          date_diagnoses[date] = date_diagnoses[date].concat(diagnoses_from_one_note)
        }
        else {
          date_diagnoses[date] = diagnoses_from_one_note
        }
      }

      let recs_from_one_note = data[key]["recommendations"]

      if (recs_from_one_note.length !== 0) {
        let doctor = data[key]["metadata"]["doctor"]
        if (doctor in doc_recs) {
          doc_recs[doctor] = doc_recs[doctor].concat(recs_from_one_note)
        }
        else {
          doc_recs[doctor] = recs_from_one_note
        }
        let date = data[key]["metadata"]["date"]
        if (date in date_recs) {
          date_recs[date] = date_recs[date].concat(recs_from_one_note)
        }
        else {
          date_recs[date] = recs_from_one_note
        }
      }

      let meds_from_one_note = data[key]["medications"]

      if (meds_from_one_note.length !== 0) {
        let doctor = data[key]["metadata"]["doctor"]
        if (doctor in doc_meds) {
          doc_meds[doctor] = doc_meds[doctor].concat(meds_from_one_note)
        }
        else {
          doc_meds[doctor] = meds_from_one_note
        }
        let date = data[key]["metadata"]["date"]
        if (date in date_meds) {
          date_meds[date] = date_meds[date].concat(meds_from_one_note)
        }
        else {
          date_meds[date] = meds_from_one_note
        }
      }



    }

    setDoctorDiagnoses(doc_diagnoses)
    setDoctorMedications(doc_meds)
    setDoctorRecommendations(doc_recs)

    setDateDiagnoses(date_diagnoses)
    setDateRecommendations(date_recs)
    setDateMedications(date_meds)

  }

  useEffect(() => {

    console.log(recAttribute)

    //TODO: running after first initial render 
    if (diagnosisAttribute === "Date") {
      setFilterDiagnoses(dateDiagnoses)
    }
    else if (diagnosisAttribute === "Doctor") {
      setFilterDiagnoses(doctorDiagnoses)
    }

    if (medAttribute === "Date") {
      setFilterMedications(dateMedications)
    }
    else if (medAttribute === "Doctor") {
      setFilterMedications(doctorMedications)
    }

    console.log(dateRecommendations)
    if (recAttribute === "Date") {
      setFilterRecommendations(dateRecommendations)
    }
    else if (recAttribute === "Doctor") {
      setFilterRecommendations(doctorRecommendations)

    }
  }, [diagnosisAttribute, medAttribute, dateRecommendations, recAttribute, dateDiagnoses, filterDiagnoses, doctorDiagnoses, dateMedications, doctorMedications, doctorRecommendations]);


  const handleAttributeChange = function (e: React.ChangeEvent<HTMLSelectElement>): void {
    e.preventDefault()
    let index = e.target.selectedIndex
    let optionElement = e.target.children[index]
    let optionElementId = optionElement.getAttribute('id');


    if (optionElementId === "recs" && e.target.value === "Doctor") {
      setRecAttribute("Doctor")
      }
    else if (optionElementId === "recs" && e.target.value === "Date") {
      setRecAttribute("Date")
    }
    else if (optionElementId === "meds" && e.target.value === "Doctor") {
      setMedAttribute("Doctor")
    }
    else if (optionElementId === "meds" && e.target.value === "Date") {
      setMedAttribute("Date")
    }
    else if (optionElementId === "diagnoses" && e.target.value === "Doctor") {
      setDiagnosisAttribute("Doctor")
    }
    else if (optionElementId === "diagnoses" && e.target.value === "Date") {
      setDiagnosisAttribute("Date")
    }
    
  }

  return (
    <div className="PatientDashboard">
      <header className="App-header">
        <div className="sidebar">
          <label>
            Select a patient:
            <select name="selectedPatient" value={selectedPatient} onChange={e => setSelectedPatient(e.target.value)}>
              {patients.map((patient, idx) =>
                <option key={idx}>{patient}</option>
              )}
            </select>
          </label>
          <button onClick={populateDashboards}> Populate </button>
        </div>
        <div className="main-content">
          <div className="sections-container">
            <div className="container">
              <div className="section">
                <input className="section-title" value="Medications" readOnly></input>
                <div className="qualifier">by</div>
                <select value={medAttribute} onChange={handleAttributeChange}>
                  {options.map((option) => (<option id="medications">{option}</option>))}
                </select>
                <div className="content">{Object.keys(filterMedications).map((key, index) => (
                  <div>
                    <li key={index}>{key}</li>
                    <p>{filterMedications[key].map((val, index) => (<li key={index}>{val}</li>))}</p>
                  </div>))}
                </div>
              </div>
            </div>
            <div className="container">
              <div className="section">
                <input className="section-title" value="Recommendations" readOnly></input>
                <div className="qualifier">by</div>
                <select value={recAttribute} onChange={handleAttributeChange}>
                  {options.map((option) => (<option id="recs">{option}</option>))}
                </select>
                <div className="content">{Object.keys(filterRecommendations).map((key, index) => (
                  <div>
                    <li key={index}>{key}</li>
                    <p>{filterRecommendations[key].map((val, index) => (<li key={index}>{val}</li>))}</p>
                  </div>))}
                </div>
              </div>
            </div>
            <div className="container">
              <div className="section">
                <input className="section-title" value="Diagnoses" readOnly></input>
                <div className="qualifier">by</div>
                <select value={diagnosisAttribute} onChange={handleAttributeChange}>
                  {options.map((option) => (<option id="diagnoses">{option}</option>))}
                </select>
                <div className="content">{Object.keys(filterDiagnoses).map((key, index) => (
                  <div>
                    <li key={index}>{key}</li>
                    <p>{filterDiagnoses[key].map((val, index) => (<li key={index}>{val}</li>))}</p>
                  </div>))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </header >
    </div >

  )
}

export default App;
