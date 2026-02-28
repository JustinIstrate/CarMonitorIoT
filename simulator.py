import time
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# 1. Conexiunea
# ATENȚIE: Pune numele fișierului tău .json
cred = credentials.Certificate("carmonitoriot-firebase.json")

# ATENȚIE: Pune link-ul tău Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://carmonitoriot-3f81c-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Creăm referințele. 'my_car' pentru date, 'command' pentru butonul de oprire
ref_data = db.reference('my_car')
ref_command = db.reference('command')

def simulate_car_data():
    rpm = 800
    speed = 0
    temperature = 20.0

    # La pornirea motorului, ne asigurăm că butonul de oprire este pe False
    ref_command.set({'stop_engine': False})

    print("🚗 Motor pornit! Sistemele live și pregătite pentru comenzi...\n")
    print("-" * 60)

    try:
        while True:
            # --- COMUNICARE 2-WAY: Verificăm dacă s-a apăsat butonul pe site ---
            command = ref_command.get()
            if command and command.get('stop_engine') == True:
                print("\n🛑 ALERTĂ: OPRIRE DE URGENȚĂ INIȚIATĂ DIN DASHBOARD!")
                # Resetăm datele la zero înainte de a opri
                ref_data.set({"rpm": 0, "speed": 0, "temperature": 20.0, "error": "ENGINE KILLED"})
                break # Ieșim din bucla infinită și oprim scriptul

            # Generăm datele normale
            rpm_change = random.randint(-300, 600)
            rpm = max(800, min(6500, rpm + rpm_change))

            if rpm > 2000:
                speed = min(130, speed + random.randint(1, 4))
            elif speed > 0:
                speed = max(0, speed - random.randint(1, 3))

            if temperature < 90.0:
                temperature += random.uniform(0.5, 1.5)
            else:
                temperature += random.uniform(-0.5, 0.5)

            error_code = "NONE"
            if random.random() < 0.03:
                error_code = random.choice(["P0300 (Misfire)", "P0171 (System Too Lean)", "P0420 (Catalyst)"])

            car_data = {
                "rpm": rpm,
                "speed": speed,
                "temperature": round(temperature, 1),
                "error": error_code
            }

            ref_data.set(car_data)
            print(f"☁️ Live -> RPM: {car_data['rpm']:4d} | Viteză: {car_data['speed']:3d} km/h")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Motor oprit manual.")

if __name__ == "__main__":
    simulate_car_data()