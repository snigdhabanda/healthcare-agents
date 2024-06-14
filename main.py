from datetime import date 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from clinical_note_parser import ClinicalNoteParser
from models import Notes
from models import Note
from models import NoteMetadata
from model_client import query_gpt
import concurrent.futures
import parse_note
import create_embeddings_for_note 
import convert_note_to_vector


app = FastAPI() 

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_headers = ["*"],
    expose_headers = ["*"]
)

#Extract patient info for all notes in record 

clinical_note_parser = ClinicalNoteParser()
parsed_notes = {}
note_diagnoses = {}
note_medications = {}
note_recommendations = {}

@app.get("/notes", response_model = Notes)
async def get_patient_info():
    note = clinical_note_parser.parse('100.xml')
    

    # executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    # futures = [executor.submit(query_gpt, note, Patient) for note in notes]
    # results = [future.result() for future in futures]

    # results = [] 
    # print(notes)
    # for note in notes:
    #   result = query_gpt(note, Note)
    #   results.append(result)

    {
        "diagnoses": ['Left ankle fracture', 'Sleep stage/arrousal dysfunction (780.56)', 'Sleep disordered breathing', 'Relative difficulties in sleep reinitiation and maintenance', 'CAD', 'DMII', 'Hypercholesterolemia', 'Bipolar disorder', 'Depression', 'RCA lesion (70-80% proximal, 90% ostial PDA)', 'VF arrest during cath', 'Afib with RVR'],
        "recommendations": ['Use a tube sock with air cast', 'Use a cane for ambulation', 'Stay in air splint with sock', 'Follow up in six weeks for review at Boxborough office', 'Initiation of PRN Zolpidem tartrate therapy, 5 mg tablets, utilizing one to two tablets p.o. q. h.s. PRN for difficulties of sleep reinitiation and maintenance', 'Take Zolpidem tartrate therapy no more than 2-3 times per week to avoid physiologic dependency', 'Consider repeat sleep study with potential trial of BIPAP therapy', 'Consider supplemental O2 therapy at night if poorly responsive to BIPAP', 'Follow up in sleep disorders clinic in approximately four months', 'Consider nonpharmacologic approaches such as hypnotherapy in the future', 'Ramp up lopressor as tolerated by BP', 'Continue plavix, lopressor, lisinopril, lipitor, ASA', 'Continue depakote and lithium', 'Continue remeron QHS', 'Follow up TSH', 'NPH insulin, regular insulin sliding scale'],
        "medications": ['ASA', 'Lipitor 20mg', 'Lopressor 50mg BID', 'Folate', 'Norvasc 5mg daily', 'Lithium 300mg BID', 'Depakote 500mg BID', 'Sonata 10mg QHS', 'Doxylamine 25mg QHS', 'Mirtazapine 45mg daily', 'Plavix', 'Lisinopril', 'Remeron QHS', 'NPH insulin', 'Regular insulin sliding scale', 'Fragmin', 'Nexium', 'Provigil 200 mg p.o. q. a.m. PRN', 'Lithium', 'Valproate', 'Glucophage 850 mg t.i.d.', 'Humulin 15 units at night', 'Folate', 'Metoprolol', 'Cardia', 'Vitamin E', 'Coated aspirin']
    }

    results = [Note(diagnoses=['Left ankle fracture'], medications=['Prozac', 'Cardizem', 'Glucophage', 'Amaryl'], recommendations=['Use a tube sock with air cast', 'Use a cane for ambulation', 'Stay in air splint with sock', 'Follow up in six weeks for review at Boxborough office'], metadata=NoteMetadata(date='2106-02-12', doctor='Habib Valenzuela, M.D.')), Note(diagnoses=['nausea', 'vomiting', 'left lower quadrant discomfort', 'intermittent chest pain', 'EKG changes', 'soft murmur', 'abdominal pain', 'non-specific ST changes on EKG', 'rule out diverticulitis', 'rule out MI'], medications=[], recommendations=['admit for rule out MI', 'get CT scan to rule out diverticulitis'], metadata=NoteMetadata(date='2008-03-14', doctor='JAY CARROLL, M.D.')), Note(diagnoses=['Sleep stage/arrousal dysfunction (780.56)', 'Sleep disordered breathing', 'Relative difficulties in sleep reinitiation and maintenance'], medications=['Provigil 200 mg p.o. q. a.m. PRN', 'Lithium', 'Valproate', 'Glucophage 850 mg t.i.d.', 'Humulin 15 units at night', 'Folate', 'Metoprolol', 'Cardia', 'Vitamin E', 'Coated aspirin'], recommendations=['Initiation of PRN Zolpidem tartrate therapy, 5 mg tablets, utilizing one to two tablets p.o. q. h.s. PRN for difficulties of sleep reinitiation and maintenance', 'Take Zolpidem tartrate therapy no more than 2-3 times per week to avoid physiologic dependency', 'Consider repeat sleep study with potential trial of BIPAP therapy', 'Consider supplemental O2 therapy at night if poorly responsive to BIPAP', 'Follow up in sleep disorders clinic in approximately four months', 'Consider nonpharmacologic approaches such as hypnotherapy in the future'], metadata=NoteMetadata(date='2109-09-14', doctor='Yovani Vergara, M.D.')), Note(diagnoses=['CAD', 'DMII', 'Hypercholesterolemia', 'Bipolar disorder', 'Depression', 'RCA lesion (70-80% proximal, 90% ostial PDA)', 'VF arrest during cath', 'Afib with RVR'], medications=['ASA', 'Lipitor 20mg', 'Lopressor 50mg BID', 'Folate', 'Norvasc 5mg daily', 'Lithium 300mg BID', 'Depakote 500mg BID', 'Sonata 10mg QHS', 'Doxylamine 25mg QHS', 'Mirtazapine 45mg daily', 'Plavix', 'Lisinopril', 'Remeron QHS', 'NPH insulin', 'Regular insulin sliding scale', 'Fragmin', 'Nexium'], recommendations=['Ramp up lopressor as tolerated by BP', 'Continue plavix, lopressor, lisinopril, lipitor, ASA', 'Continue depakote and lithium', 'Continue remeron QHS', 'Follow up TSH', 'NPH insulin, regular insulin sliding scale'], metadata=NoteMetadata(date='2111-10-10', doctor='Victor Shepard MD'))]
    
    return(Notes(Notes = results))
    
    

@app.get("/map", response_model = Notes)
async def get_summary_map(unstructured_notes: [str], file_name: str, structured_notes: Notes):
    vector = [] 
    vector_diagnoses = [] 
    vector_meds = [] 
    vector_recs = [] 

    for idx, note in enumerate(unstructured_notes):
        cleaned_note = parse_note(note)
        id = f"{file_name}_{idx}"

        cleaned_note_split = cleaned_note.split(".")
        parsed_notes[f"{id}"] = cleaned_note_split

        file = create_embeddings_for_note(cleaned_note_split, id)
        vector = convert_note_to_vector(file)
    
    for idy, note in enumerate(structured_notes):
        diagnoses = note.diagnoses 
        recs = note.recommendations 
        meds = note.medications 

        id = f"{file_name}_{idx}"

        note_diagnoses[f"{id}"] = diagnoses 
        note_recommendations[f"{id}"] = recs 
        note_medications[f"{id}"] = meds 

        file_diagnoses = create_embeddings_for_note(f"{id}_diagnoses", id)
        vector_diagnoses = convert_note_to_vector(file_diagnoses)
        
        file_meds = create_embeddings_for_note(f"{id}_meds", id)
        vector_meds = convert_note_to_vector(file_meds)
        
        file_recs = create_embeddings_for_note(f"{id}_recs", id)
        vector_recs = convert_note_to_vector(file_recs) 

 