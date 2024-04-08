## Hospital Management System
1. Clone the repository  
   `git clone https://github.com/coder-singh/hospital_management_system.git`
2. Go to the root directory
   `cd hospital_management_system`
3. start up docker-compose
    `docker-compose up`

### Endpoints
{{server}} -> 127.0.0.1:5000
  
Get Patient {{server}}/v1/patient/1  
Search Patient {{server}}/v1/patients?name=satyendra  
Create Patient {{server}}/v1/patients data = {
    "name": "Satyendra",
    "age": 26,
    "gender": "m",
    "contact": "9999999990"
}  
Update patient {{server}}/v1/patient/2 data = {
    "name": "Satyendra",
    "age": 26,
    "gender": "m",
    "contact": "9999999990"
}  
delete patient {{server}}/v1/patient/2  


add medical history {{server}}/v1/patient/1/medical-history  
data = {
    "diagnoses": [
        "diagnosis 1",
        "diagnosis 2"
    ],
    "allergies": [
        "allergy 3"
    ],
    "medications": [
        "medication 4",
        "medication 5"
    ]
}  

get medical history {{server}}/v1/patient/1/medical-history  

assign doctor {{server}}/v1/patient/1/assign-doctor  
{
    "doctor_id": 1
}  


  

### Tests
`python3 -m unittest discover tests`
