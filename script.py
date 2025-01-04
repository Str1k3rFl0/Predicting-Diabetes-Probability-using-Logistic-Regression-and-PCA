import pandas as pd
import random

class Age:
    def __init__(self, age=None):
        self.age = age if age is not None else random.randint(18, 90)

    def get_age(self):
        return self.age

class Gender:
    def __init__(self, gender=None):
        self.gender = gender if gender is not None else random.randint(0, 1)

    def get_gender(self):
        return 'Female' if self.gender == 0 else 'Male'

class BMI:
    def __init__(self, kg=None, height=None):
        self.kg = kg if kg is not None else random.randint(40, 90)
        self.height = height if height is not None else random.uniform(1.3, 1.9)

    def convert_BMI(self):
        bmi = self.kg / (self.height ** 2)
        return bmi

    def interpretare_BMI(self, bmi):
        if bmi < 18.5:
            return 'Underweight'
        elif 18.5 <= bmi <= 24.9:
            return 'Normal weight'
        elif 25.0 <= bmi <= 29.9:
            return 'Overweight'
        else:
            return 'Obesity'

class BloodPressure:
    def __init__(self, age, gender, bmi):
        self.age = age
        self.gender = gender
        self.bmi = bmi
        self.systolic = random.randint(90, 100)
        self.diastolic = random.randint(60, 120)

    def calculate_blood_pressure(self):
        systolic_adjustment = 0
        diastolic_adjustment = 0

        # Age - at older ages, the tension may be higher
        if self.age > 40:
            systolic_adjustment += (self.age - 40) * 0.2
            diastolic_adjustment += (self.age - 40) * 0.1

        # BMI - people with a high BMI may have higher blood pressure
        bmi = self.bmi.convert_BMI()
        if bmi >= 25:
            systolic_adjustment += 10
            diastolic_adjustment += 5

        # Gender - adjustments based on gender (male vs female)
        if self.gender == 1:  # Male
            systolic_adjustment += 5
            diastolic_adjustment += 2
        # Female has no adjustment in this case

        self.systolic += systolic_adjustment
        self.diastolic += diastolic_adjustment

    def interpret_blood_pressure(self):
        if self.systolic < 120 and self.diastolic < 80:
            return "Normal"
        elif 120 <= self.systolic < 130 and self.diastolic < 80:
            return "Elevated"
        elif 130 <= self.systolic < 140 or 80 <= self.diastolic < 90:
            return "Hypertension Stage 1"
        elif self.systolic >= 140 or self.diastolic >= 90:
            return "Hypertension Stage 2"
        elif self.systolic > 180 or self.diastolic > 120:
            return "Hypertensive Crisis (Medical Emergency)"
        else:
            return "Unknown"

class Cholesterol:
    def __init__(self, bmi, age):
        self.bmi = bmi
        self.age = age
        self.cholesterol = self.adjust_cholesterol()

    def adjust_cholesterol(self):
        cholesterol_base = random.randint(150, 250)

        bmi = self.bmi.convert_BMI()
        if bmi >= 30:
            cholesterol_base += random.randint(30, 50)
        elif bmi >= 25:
            cholesterol_base += random.randint(10, 30)

        if self.age > 45:
            cholesterol_base += random.randint(10, 30)

        return min(cholesterol_base, 300)

    def interpret_cholesterol(self):
        if self.cholesterol < 200:
            return "Normal"
        elif 200 <= self.cholesterol < 240:
            return "Borderline high"
        else:
            return "High"

class Glucose:
    def __init__(self, bmi, age, systolic, diastolic):
        self.bmi = bmi
        self.age = age
        self.systolic = systolic
        self.diastolic = diastolic
        self.glucose = self.adjust_glucose()

    def adjust_glucose(self):
        glucose_base = random.randint(70, 130)

        bmi = self.bmi.convert_BMI()
        if bmi >= 30:
            glucose_base += random.randint(10, 20)
        elif bmi >= 25:
            glucose_base += random.randint(5, 10)

        if self.age > 45:
            glucose_base += random.randint(10, 20)

        if self.systolic >= 140 or self.diastolic >= 90:
            glucose_base += random.randint(5, 15)

        return min(glucose_base, 200)

class DiabetesRisk:
    def __init__(self, age, bmi, systolic, diastolic, cholesterol, glucose):
        self.age = age
        self.bmi = bmi
        self.systolic = systolic
        self.diastolic = diastolic
        self.cholesterol = cholesterol
        self.glucose = glucose

    def calculate_diabetes_probability(self):
        probability = 0

        # Age Factor
        if self.age > 45:
            probability += 0.15

        # BMI Factor
        bmi = self.bmi.convert_BMI()
        if bmi >= 30:
            probability += 0.2
        elif bmi >= 25:
            probability += 0.1

        # Blood pressure factor
        if self.systolic >= 140 or self.diastolic >= 90:
            probability += 0.15

        # Glucose Factor
        if self.glucose >= 126:
            probability += 0.3
        elif self.glucose >= 100:
            probability += 0.15

        # Cholesterol Factor
        if self.cholesterol >= 240:
            probability += 0.1

        return min(probability, 1.0)

class Patient:
    def __init__(self, age=None, gender=None, kg=None, height=None):
        self.age = Age(age)
        self.gender = Gender(gender)
        self.bmi = BMI(kg, height)
        self.blood_pressure = BloodPressure(self.age.get_age(), self.gender.get_gender(), self.bmi)
        self.cholesterol = Cholesterol(self.bmi, self.age.get_age())
        self.glucose = Glucose(self.bmi, self.age.get_age(), self.blood_pressure.systolic, self.blood_pressure.diastolic)
        self.diabetes_risk = DiabetesRisk(self.age.get_age(), self.bmi, self.blood_pressure.systolic, self.blood_pressure.diastolic, self.cholesterol.cholesterol, self.glucose.glucose)

    def save_to_csv(self, filename='diabetes_data.csv'):
        data = pd.DataFrame([{
            'age': self.age.get_age(),
            'gender': self.gender.get_gender(),
            'bmi': round(self.bmi.convert_BMI(), 2),
            'bmi_category': self.bmi.interpretare_BMI(self.bmi.convert_BMI()),
            'systolic': self.blood_pressure.systolic,
            'diastolic': self.blood_pressure.diastolic,
            'blood_pressure_category': self.blood_pressure.interpret_blood_pressure(),
            'cholesterol': self.cholesterol.cholesterol,
            'cholesterol_category': self.cholesterol.interpret_cholesterol(),
            'glucose': self.glucose.glucose,
            'diabetes_probability': round(self.diabetes_risk.calculate_diabetes_probability(), 2)
        }])

        try:
            existing_data = pd.read_csv(filename)
            data = pd.concat([existing_data, data], ignore_index=True)
        except FileNotFoundError:
            pass

        data.to_csv(filename, index=False)

def generate_multiple_records(num_records=10000, filename='diabetes_data.csv'):
    for _ in range(num_records):
        patient = Patient()
        patient.blood_pressure.calculate_blood_pressure()
        patient.save_to_csv(filename)
    print("Data saved successfully")

generate_multiple_records(10000)
