import streamlit as st
import hashlib

# Initialize an empty hospital ledger (a dictionary where keys are patient names)
hospital_ledger_advanced = {}

# Function to generate a hash for the visit
def generate_hash(patient_name, treatment, cost, date_of_visit):
    data = f"{patient_name}{treatment}{cost}{date_of_visit}"
    return hashlib.sha256(data.encode()).hexdigest()

# Function to add or update patient visits (optimized)
def add_patient_visit_advanced(patient_name, treatment, cost, date_of_visit):
    # Check if the patient already exists
    if patient_name in hospital_ledger_advanced:
        st.write(f"Updating visit record for {patient_name}.")
    else:
        st.write(f"Adding new visit record for {patient_name}.")

    # Generate a hash for this visit record
    visit_hash = generate_hash(patient_name, treatment, cost, date_of_visit)

    # Create a dictionary for the visit with the hash
    visit = {
        "treatment": treatment,
        "cost": cost,
        "date_of_visit": date_of_visit,
        "visit_hash": visit_hash  # Store the hash to verify data integrity
    }

    # Add the visit to the patient's list of visits (using a dictionary)
    if patient_name not in hospital_ledger_advanced:
        hospital_ledger_advanced[patient_name] = []

    hospital_ledger_advanced[patient_name].append(visit)
    st.write(f"Visit added for {patient_name} on {date_of_visit} for treatment {treatment} costing ${cost}.")
    st.write(f"Visit hash: {visit_hash}")

# Streamlit UI
st.title("Hospital Ledger")

# Sidebar for user input
st.sidebar.header("Add New Patient Visit")
patient_name = st.sidebar.text_input("Patient Name")
treatment = st.sidebar.text_input("Treatment Received")
cost = st.sidebar.number_input("Cost of Treatment ($)", min_value=0.0, step=0.1)
date_of_visit = st.sidebar.date_input("Date of Visit")

# Button to add visit
if st.sidebar.button("Add Visit"):
    if patient_name and treatment and cost and date_of_visit:
        add_patient_visit_advanced(patient_name, treatment, cost, date_of_visit)
    else:
        st.error("Please fill in all fields to add the visit.")

# Search for patient visits
st.sidebar.header("Search Patient Visit Records")
search_patient = st.sidebar.text_input("Enter Patient Name to Search")

if search_patient:
    if search_patient in hospital_ledger_advanced:
        st.subheader(f"Visit records for {search_patient}:")
        for visit in hospital_ledger_advanced[search_patient]:
            st.write(f"  - Treatment: {visit['treatment']}, Cost: ${visit['cost']}, Date: {visit['date_of_visit']}, Hash: {visit['visit_hash']}")
    else:
        st.warning(f"Patient {search_patient} not found in the ledger.")

# Display the hospital ledger
if st.checkbox("Show full hospital ledger"):
    st.write(hospital_ledger_advanced)
