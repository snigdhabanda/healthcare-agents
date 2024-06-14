import instructor
from anthropic import Anthropic
import voyageai
import numpy as np 
from models import Note
import os 


claude_key = os.getenv("CLAUDE_API_KEY")
claude_client = instructor.from_anthropic(Anthropic(api_key=claude_key))


def get_structured_note(note, response_model):

    patient: response_model = claude_client.messages.create(
    model="claude-3-opus-20240229",
    messages=[
        {
            "role": "user",
            "content": f"Extract information from {note}",
        }
    ],
    response_model=response_model,
    )
     
    return patient

def parse_note(note):
    response = claude_client.messages.create(
        model="claude-3-opus-20240229",
        messages=[{"role": "user", "content": f"Please parse this fake medical note {note}. It has many extraneous characters, dates, addresses, etc. I would like the output in full sentences and only alphanumeric characters. Please preserve all text from the core medical encounter."}
  ])
    return response.content[0].text 


vo = voyageai.claude_client(api_key="pa-ZW5I8CfStTVOhLTwSJZXbctIg5hoUC8HXc2EqasISqM")

#Goal: link a diagnosis/rec/medication back to the relevant sentence in the note
# process XML files by feeding to an ai model 
# TODO: migrate XML files to a document store 
# generate embeddings for each diagnosis, med, rec and for the processed note
# save the embeddings for each note and for each d/m/r in each note. each d/m/r in a note receives its own file. save locally for now and migrate to vector db later
# compute dot product of each d/m/r and each note 
# store the d/m/r as a key and the sentence that resulted in the largest dot product ie. {"diagnosis": sentence from the note where this diagnosis originated. } 

# TODO: clean up hardcoded text below and replace with API calls  

texts = ['Left ankle fracture', 'Sleep stage/arrousal dysfunction (780.56)', 'Sleep disordered breathing', 'Relative difficulties in sleep reinitiation and maintenance', 'CAD', 'DMII', 'Hypercholesterolemia', 'Bipolar disorder', 'Depression', 'RCA lesion (70-80% proximal, 90% ostial PDA)', 'VF arrest during cath', 'Afib with RVR', 'Sleep stage/arrousal dysfunction (780.56)', 'Sleep disordered breathing', 'Relative difficulties in sleep reinitiation and maintenance', 'CAD', 'DMII', 'Hypercholesterolemia', 'Bipolar disorder', 'Depression', 'RCA lesion (70-80% proximal, 90% ostial PDA)', 'VF arrest during cath', 'Afib with RVR']

note_1 = "Har is a 43 year old 6' 214 pound gentleman who is referred for consultation by Dr. Harlan Oneil.  About a week ago he slipped on the driveway at home and sustained an injury to his left ankle. He was seen at Tri-City Hospital and was told he had a fracture.  He was placed in an air splint and advised to be partial weight bearing, and he is using a cane.  He is here for routine follow-up. Past medical history is notable for no ankle injuries previously. He has a history of diabetes and sleep apnea.  He takes Prozac, Cardizem, Glucophage and Amaryl.  He is also followed by Dr. Harold Nutter for an arrhythmia.  He does not smoke.  He drinks minimally.  He is a set designer at Columbia Pictures. On examination today he has slight tenderness of the left ankle about four fingerbreadths above the malleolus. The malleolus is non-tender medially or laterally with no ligamentous tenderness either.  Dorsal flexion and plantar flexion is without pain. There is no significant swelling.  There are no some skin changes with some small abrasions proximally.  There is no fibular tenderness proximally.  No anterior pain is noted.  No hindfoot, midfoot or forefoot tenderness is noted. I would like him to use a tube sock with his air cast.  He is using a cane for ambulation.  His x-rays do not show a notable fracture pattern today, and we will await the Radiology opinion. I would like him to stay in the air splint with the sock.  I will see him back in six weeks for review at the Boxborough office. Diagnosis:  Left ankle fracture."

note_2 = "The patient was seen and examined in the emergency department.  The patient was seen by the Emergency Medicine resident.  I have discussed the management with the resident.  I have also seen the patient primarily and reviewed the medical record.  This is a brief addendum to the medical record. HISTORY OF PRESENTING COMPLAINT:  Briefly, this is a 45-year-old male who complains of several days of nausea, vomiting, and left lower quadrant discomfort.  He also describes intermittent chest pain, which he has had for a number of months without significant change.  He was sent in from his primary care doctor today with this pain and was also noted to have some EKG changes.  The patient has no chest pain at the time of evaluation in the emergency department and no shortness of breath.REVIEW OF SYSTEMS:  As indicated and otherwise negative. PAST MEDICAL HISTORY:  As indicated in the chart. SOCIAL HISTORY AND FAMILY HISTORY:  As indicated in the chart. PHYSICAL EXAMINATION:  On physical examination, the patient is very well-appearing, a smiling, very pleasant gentleman in no acute distress.  The blood pressure is 119/90, the pulse 82, and the temperature 97.9 degrees.  Normocephalic and atraumatic.  The chest is clear to auscultation.  The heart has a regular rate and rhythm. The abdomen is soft.  He has left lower quadrant tenderness.  He also, of note on cardiovascular examination, has a soft murmur which he says he has had since childhood.  The extremities are normal.  The neurologic examination is non-focal. THERAPY RENDERED/COURSE IN ED:  This is a gentleman with abdominal pain who will receive a CAT scan to rule out diverticulitis.  He has also had some non-specific ST changes on his EKG.  He is pain-free at this time.  He does not describe a classic exertional pattern for his chest pain, but given that he is a diabetic and with EKG changes, he will also be admitted for rule out MI.  A CT is pending at the time of this dictation.DISPOSITION (including condition upon discharge):  As above.  The patient's condition is currently stable."

note_3 = "Thank you in advance for allowing me to share in the medical care of Mr. Harlan B. Valdez, a 46-year-old male patient with prior polysomnographic evidence of sleep disordered breathing, as well as a history of difficulty in sleep, reinitiation and maintenance and increased early morning awakenings, as well as mixed systemic medical conditions.  HISTORY OF PRESENT ILLNESS: As you already know, Mr. Valdez who demonstrates a history of difficulties of sleep reinitiation and maintenance, as well as increased early morning awakenings, has noted an exacerbation of these sleep difficulties, occurring in temporal association with his loss of his wife from pancreatic cancer last year. He is now placed in the unfortunate situation of being a single parent to a 15-year-old son and a 10-year-old daughter and describes a modification of his current employment duties of a set designer. In particular, Mr. Valdez describes undergoing on frequent international travelling which has bee markedly curtailed as he is tending to his family situation closer to home. He described a history of intermittent snoring symptomatology but is unaware of specific nocturnal respiratory pauses. He is unaware of a 'restless' lower limb sensory complaints which may impact on his ability to initiate or reinitiate sleep. He denies a history of a 'night owl' personality or circadian rhythm dysfunction which may have played a role with respect to nocturnal sleep disruptions or sleep difficulties. He denies a history of paroxysmal abnormal disturbances or associated narcoleptic symptoms. Mr. Valdez underwent an initial formal polysomnographic evaluation at the center for sleep diagnostics at Holy Cross on 11/26/05, during which time he was noted to demonstrate a respiratory disturbance index of 81/hour, particularly exacerbated in the supine position and characterized predominantly by hypopneas, with equal distribution during non-REM and stage REM sleep and with associated O2 desaturation Nadir of 88% The respiratory disturbances were predominantly obstructive or mixed hypopneas. In addition, loud snoring was noted. There was evidence of a sleep efficiency of 88% and a short sleep onset latency of 4 minutes. There was a predominance of 'light' non-REM stages I-II sleep, and a concomitant inability to achieve significant 'slow-wave' or stage REM sleep. There was also 'alpha intrusions and alpha delta sleep' evident during the initial sleep study. In addition premature ventricular contractions were noted. The patient underwent a CPAP titration on 01/15/06, also at the Tenacre Foundation Nursing Home in Boxborough, during which time there was a marked reduction in the frequency of hypopneas (respiratory disturbance index equals 2/hour) with CPAP titrations between 4-6 cm. Sleep efficiency improved to 91%, a short sleep onset latency was also noted (3 minutes). There was once again an increased predominance of 'light' non-REM stage I-II sleep, with concomitant inability to achieve sustained 'slow wave sleep'. Since his initial trial of nocturnal CPAP titration (at 6 cm of water pressure) and with various CPAP mask modifications (including CPAP nasal face mask and a Mallinckrodt 'Breeze' supportive head gear with 'nasal pillows'. The patient describes associated claustrophobic symptomatology, relative difficulties with sustained nocturnal home CPAP use, and difficulties with regards to CPAP to being and complications by the bulkiness of the CPAP machine in general. As a result, he has not utilized nocturnal CPAP therapy for a period of time, although he still maintains the CPAP equipment in his house. Of particular note, and exacerbation of the past year, the patient demonstrates increased early morning awakenings (averaging 2-4 in number) with typical awakenings occurring approximately two hours after sleep initiation at 9:30 p.m. (the patient describes one awakening at 11:30 p.m. and the second awakening at 11:45 a.m., of unclear causative etiology). The patient then might awaken at 3 a.m. and be 'ready for the day'.  If he is able to reinitiate sleep thereafter, the patient may demonstrate additional two early morning awakenings after a final awakening at 6 a.m. The patient is noted to have a history of mixed systemic conditions including diabetes, coronary artery disease, depressive disorder, as well as a relatively stable gastrointestinal condition, with no upper GI evidence of gastroparesis. ALLERGIES/ADVERSE REACTIONS: The patient describes an enhancement to suicidal tendencies in association with prior Prozac usage. SOCIAL HISTORY: The patient denies active tobacco or alcoholic beverage usage. He has lost 15-20 pounds over the past several years. His current weight is 195 pounds. He is desirous of losing some additional weight with regards to more regular exercise, but his hectic social situation makes this somewhat difficult at the present time. On examination, the patient demonstrates a blood pressure of 146/88, (seated, left arm), respiratory rate 16. HEENT EXAMINATION: Borderline small posterior oropharyngeal aperture, with slightly increased redundant tissue evident posteriorly and a slightly elongated uvula noted. The patient appears awake, alert, with speech clear and fluent and receptive language function essentially intact. He is presently wearing dental braces. No obvious cranial nerve deficits are appreciated. No focal, sensory, motor or neurologic deficits are noted. No significant appendicular dystaxias or dysmetrias are currently in evidence. The routine gait appears to be normal based, without evidence of significant gait dystaxias.  No current clinical ictal manifestations are present. No acute evidence of 'micro-sleeps' are noted. IMPRESSION:  1. Sleep stage/arrousal dysfunction (780.56): Manifested by subjective complaints of nonrestorative sleep, increased daytime fatigue and alternating hypersomnia, and recurrent polysomnographic evidence of 'lightened' sleep pattern, with increased predominance of non-REM stages 1-2 sleep, and with the presence of 'alpha' intrusions and 'alpha delta' component to deeper sleep. These latter EEG findings have been described in association with subjective complaints of nonrestorative sleep, as well as clinical setting of chronic pain related complaints, depressive or anxiety disorder or intercurrent psychotropics agents used (but more usually associated with benzodiazepine or barbituate usage). 2. Sleep disordered breathing: As evidenced during prior polysomnographic evaluations, mostly of obstructive and or mixed hypopnea. The patient appears largely refractory to a trial of CPAP therapy, particularly in so far as he demonstrates associated claustrophobic symptoms in association with it's usage, despite relatively modest CPAP water pressures (6 cm). In addition, he has tried various nasal CPAP face mask, including the Mallinckrodt 'Breeze' supportive head gear with 'nasal pillows' and with limited success. One might consider repeating a polysomnographic evaluation in the future, and if so, utilizing a potential trial of BIPAP titration, which may help to improve claustrophobic symptoms, but the patient will still be left with the issues referable to 'tangled tubing at night' and issues referable to nasal face mask usage, as noted above.  3. Relative difficulties in sleep reinitiation and maintenance:  The patient describes at least 2-4 early morning awakenings with difficulty in sleep reinitiation and maintenance, thereby compounding his current sleep problem. While there would logically be a relationship between his current sleep exacerbations and the recent death of his wife from pancreatic cancer last year, there may also be evidence of other nocturnal sleep disturbances for which a repeat polysomnographic evaluation; i.e. in particular looking for the presence of increased spontaneous arousals or limb associated arousals or periodic limb movements of sleep may be of a special clinical benefit. PLAN: 1. In the short course, in so far as the patient describes himself as being exceedingly tired, and unable to perform the routine daily tasks of work and managing a family in the absence of his deceased wife, I have suggested initiation of PRN Zolpidem tartrate therapy, 5 mg tablets, utilizing one to two tablets p.o.  q. h.s. PRN for difficulties of sleep reinitiation and maintenance. 2. The patient is advised to take Zolpidem tartrate therapy no more than 2-3 times per week, in an effort to avoid any issues of physiologic dependency. 3. The patient was advised against potential adverse behavioral and or systemic side effects of Zolpidem tartrate therapy including  hypersomnolence, gastric upset, loose stools, diarrhea, and or cardiac palpitations. Pending his clinical response of his Zolpidem tartrate therapy, I then might seek direct treatment for his sleep disordered breathing issues which may include a repeat sleep study with potential trial of BIPAP therapy (in an effort to modify or attenuate claustrophobic symptoms). If he proves poorly responsive to trial of BIPAP therapy however, I might consider supplemental O2 therapy at night and, with this in mind a follow up sleep study should have associated end-tidal CO2 monitoring as well. 4. In the meantime, the patient was advised to contact the sleep disorders clinic for any acute sleep related concerns in the interim. 5. The patient may also benefit from nonpharmacologic approaches with regards to sleep reinitiation such as hypnotherapy, but I will hold off on these strategies pending follow up sleep disorders clinic evaluation (in approximately four months time). Once again, thank you again for allowing me to share in the medical care of Mr. Harlan Valdez. I hope this letter finds you well."

note_4 = "History of Present Illness (obtained on admission):  Pt is a 48 yo male with h/o DMII, hypercholesterolemia, Bipolar d/o, and depression who began to have sub-sternal day prior to admission in car and pre-syncope + profound weakness.  This CP was minimal, but the weakness made him pull over.  He had a repeat of these symptoms day of admission.  His EKG c/w 2/2107 showed flattened T-wave in V2 and TWI in V3 and flattened T-waves in I, aVL. His trop was negative, but MB index was elevated.  Due to T-wave flattening, history and elevated index it was decided to start on heparin and ASA and take to cath lab. Cath showed right dominant system with prox Cx 40%, LAD clear, RCA prox 70-80% lesion and ostial PDA 90%.  During final dye injection, pt had VF arrest and 2 shocks.  Pt regained puls and was in AF (new) with RVR. Pt was started on amio.  Pt then began to experience discomfort in the RVR and it was decided to intervene.  POBA was done to ostial PDA.  A first no-eluting stent was placed in prox RCA and pt had dissection and thus 2cd stent was placed.  On admission to CCU, pt still in AF with RVR (120's).  He was on amio drip, BB, loaded on plavix, ASA, lipitor, integrilin and was placed on Avandia study.  His complaint of some mild chest pain (not same as anginal pain day before) thought to be from defibrillation. Past Medical History: DMII, hyperchol, bipolar,HTN, depression (s/p ECT) Medications on admission: ASA, Lipitor 20, lopressor 50 bid, folate, norvasc 5 qd; lithium, 300 bid; depakote 500 bid; sonata 10 mg qhs, doxylamine 25 qhs, mirtazapine 45 qd Meds on Transfer: please see green sheets Medications: ASA, Lipitor 20, lopressor 50 bid, folate, norvasc 5 qd; lithium, 300 bid; depakote 500 bid; sonata 10 mg qhs, doxylamine 25 qhs, mirtazapine 45 qd Allergies:  NKDA Family History:  family h/o CAD Social History: No EtOH, no tob, no illicits Review of Systems:  per HPI Allergies:  NKDA Family History:  family h/o CAD Social History: No EtOH, no tob, no illicits Review of Systems:  per HPI CCU course + plan: 1)	Cards a.	Rhythm - on night of admission patient was started on an esmolol drip as well as amio bloused and rhythm converted to NSR.  Esmolol drip as well as amio was stopped and BB was escalated and patient has remained in NSR.i.	Ramp up lopressor as tolerated by BP b.	Pump - patient has remained euvolemic and had a Echo with EF 84% and aortic stenosis c.	Ischemia - was stented x 2 to the prox RCA lesion and was on integrilin x 24hrs prior.  He was started on plavix. i.	Cont plavix, lopressor, lisinopril, lipitor, ASA 2)	Psych - patient with long history of bipolar disorder + depression.  He was on depakote, lithium and remeron as outpt.  He was seen by psychiatry here. a.	Continue depakote and lithium (had subthereapeutic level that psych thought was likely  due to non-compliance. b.	Continue remeron qhs c.	F/u TSH 3)	DM - Blood sugars were originally elevated as amio drip he was originally on for AF contained dextrose. He has remained on NPH with RISS. a.	NPH, RISS 4)	Prophy - Fragmin nexium LABS + PE - see today's progress note EKG - AFIB with RVR, diffuse t-wave flattening Impression:  48 yo male with h/o DMII, hypercholesterolemia, Bipolar d/o, and depression and CAD p/w CP and pre-sycope found to have RCA prox 70-80% lesion and ostial PDA 90% (stents to RCA and POBA to PDA).  Cath c/b VF arrest after dye load and resultant afib with RVR. Plan:  As outlined in CCU course."

def create_embeddings_for_note(note: str, id: str):
    note_split = note.split(".")
    result = vo.embed(note_split, model="voyage-2", input_type="document")
    file_write = open(f"{id}", "w")
    file_write.write(f"{result.embeddings}")
    file_write.close()

    return file 

def create_embeddings_for_structured_note(note: Note, id: str):
    diagnoses = note.diagnoses
    recommendations = note.recommendations
    medications = note.medications

    types = {"diagnoses": diagnoses, "meds": medications, "recs": recommendations}

    for key in types.keys:
        result = vo.embed(key, model="voyage-2", input_type="document")
        file_write = open(f"{id}_{key}", "w")
        file_write.write(f"{result.embeddings}")
        file_write.close()

    return file 

def convert_note_to_vector(file) -> [float]:
    final_vector = []
    vector = [] 
    idx = 2

    while idx < len(file):
        num = ""
        idy = idx 
        while (file[idy] != "," and file[idy] != "]"):
            num += file[idy]
            idy += 1
        vector.append(float(num))
        
        if (file[idy] == "]"):
            final_vector.append(vector) 
            vector = []
            idx = idy + 4
        else:
            idx = idy + 2
    
    return final_vector

def convert_structured_note_to_vector(file) -> [float]:
    vector = []
    idx = 2
    while idx < len(file):
        num = ""
        idy = idx 
        while (file_read[idy] != "," and file_read[idy] != "]"):
            num += file_read[idy]
            idy += 1
        if (file_read[idy] == "]"):
            vector.append(float(num))
            break 
        # print(num)
        vector.append(float(num))
        idx = idy + 2
    
    return vector 


def compute_dot_product(vectors_a: [[float]], vectors_b: [[float]]) -> tuple:

    for vector_a in vectors_a:
        dot_products = []
        for vector_b in vectors_b: 
            max_length = max(len(vector_a), len(vector_b))

            # Pad both vectors to the maximum length
            padded_a = np.pad(vector_a, (0, max_length - len(vector_a)), mode='constant')
            padded_b = np.pad(vector_b, (0, max_length - len(vector_b)), mode='constant')

            # Compute and return the dot product
            dot = np.dot(padded_a, padded_b)
            dot_products.append(dot)

    max_val = max(dot_products)
    idx = dot_products.index(max_val)
        
    return (max_val, idx)
