## Hospital Management System
1. Clone the repository  
   `git clone https://github.com/coder-singh/hospital_management_system.git`
2. Go to the root directory
   `cd hospital_management_system`
3. start up docker-compose
    `docker-compose up`

### Endpoints
{{server}} -> 127.0.0.1:5000
  
1. Get Patient GET {{server}}/v1/patient/1  
2. Search Patient GET {{server}}/v1/patients?name=satyendra  
3. Create Patient POST {{server}}/v1/patients data = {
    "name": "Satyendra",
    "age": 26,
    "gender": "m",
    "contact": "9999999990"
}  
4. Update patient PUT {{server}}/v1/patient/2 data = {
    "name": "Satyendra",
    "age": 26,
    "gender": "m",
    "contact": "9999999990"
}  
5. delete patient DEL {{server}}/v1/patient/2  


6. add medical history POST {{server}}/v1/patient/1/medical-history  
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

7. get medical history GET {{server}}/v1/patient/1/medical-history  

8. assign doctor POST {{server}}/v1/patient/1/assign-doctor  
{
    "doctor_id": 1
}  

9. create doctor POST {{server}}/v1/doctors  
{
    "name": "fjeo",
    "specialization": "fjoei",
    "contact": "328"
}

10. get doctor GET {{server}}/v1/doctor/2  

11. search doctor GET {{server}}/v1/doctors?available_on=10-03-2023&specialization=ent  

12. assign department POST {{server}}/v1/doctor/1/assign-department
{
    "department_id": 1
}  

13. create department POST {{server}}/v1/departments  
{
    "name": "Eye"
}  

14. get department GET {{server}}/v1/departments/2  

15. search department GET {{server}}/v1/departments?name=ent  


### Tests
`python3 -m unittest discover tests`
