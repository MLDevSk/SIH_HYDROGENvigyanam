import serial
import tkinter as tk

# Arduino connection
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=1)

# Get voltage and current from user input
voltage = float(input("Enter the voltage (V): "))
current = float(input("Enter the current (A): "))

# GUI setup
root = tk.Tk()
root.title("Hydrogen Concentration Monitor")
root.geometry("1920x1080")
root.configure(bg="skyblue")

# Labels for PPM and info
label = tk.Label(root, text="JALASH", font=("Arial", 32), bg="skyblue")
label.pack(pady=32)

ppm_frame = tk.Frame(root, bd=4, relief='solid')
ppm_frame.place(x=347, y=285, height=85, width=280)
ppm_value = tk.StringVar()
ppm_display = tk.Label(ppm_frame, textvariable=ppm_value, font=("Arial", 29), fg="green")
ppm_display.pack()

info_value = tk.StringVar()
info_display = tk.Label(root, textvariable=info_value, font=("Arial", 16), fg="black", bg="skyblue")
info_display.place(x=762, y=388, height=85, width=685)

# Frame and labels for hydrogen production rate
rate_frame = tk.Frame(root, bd=4, relief='solid')
rate_frame.place(x=347, y=420, height=85, width=280)
rate_label = tk.Label(rate_frame, text="Hydrogen Rate(g/hour):-", font=("Arial", 18))
rate_label.pack()
rate_value = tk.StringVar()
rate_display = tk.Label(rate_frame, textvariable=rate_value, font=("Arial", 24), fg="blue")
rate_display.pack()

# Frame and labels for power consumption
power_frame = tk.Frame(root, bd=4, relief='solid')
power_frame.place(x=347, y=555, height=85, width=280)
power_label = tk.Label(power_frame, text="Power Used(W/hour):-", font=("Arial", 18))
power_label.pack()
power_value = tk.StringVar()
power_display = tk.Label(power_frame, textvariable=power_value, font=("Arial", 24), fg="red")
power_display.pack()

def interpret_ppm(ppm):
    """Interpret safety levels of PPM."""
    try:
        ppm = float(ppm)
        if ppm < 20:
            return "Safe: Hydrogen levels are within normal limits."
        elif ppm < 100:
            return "Caution: Low hydrogen concentration detected."
        elif ppm < 550:
            return "Warning: Hydrogen concentration is elevated.Ensure proper ventilation."
        elif ppm < 1000:
            return "Danger: High hydrogen concentration!."
        else:
            return "Critical Danger: Extremely high hydrogen concentration! Evacuate immediately."
    except:
        return "Error: Unable to interpret data."

def calculate_hydrogen_production_rate(ppm):
    """Calculate hydrogen production rate in grams/hour."""
    try:
        ppm = float(ppm)  # Convert ppm to float
        bottle_volume = 0.55  # Volume of the bottle in liters (550 mL)
        molar_mass_h2 = 2      # Molar mass of hydrogen in grams/mol
        molar_volume = 22.4    # Molar volume at STP in liters/mol
        # Calculate hydrogen mass in grams per hour
        mass_per_hour = (ppm * bottle_volume * molar_mass_h2) / (10**6 * molar_volume)
        return round(mass_per_hour, 6)  # Return the value rounded to 6 decimals
    except:
        return 0  # Default to 0 in case of an error

def calculate_power(voltage, current):
    """Calculate power consumption in watt-hours."""
    return round(voltage * current, 2)

def update_display():
    """Update the GUI with PPM, safety info, hydrogen production rate, and power usage."""
    if arduino.in_waiting > 0:
        try:
            data = arduino.readline().decode('utf-8').strip()  # Read data from Arduino
            ppm_value.set(f"{data} PPM")  # Update PPM value
            info_value.set(interpret_ppm(data))  # Update safety info

            # Calculate hydrogen production rate
            hydrogen_rate = calculate_hydrogen_production_rate(data)
            rate_value.set(f"{hydrogen_rate} g/hour")  # Update production rate

            # Calculate power usage
            power = calculate_power(voltage, current)
            power_value.set(f"{power} W/hour")  # Update power usage
        except:
            ppm_value.set("Error")
            info_value.set("Error reading data from sensor.")
            rate_value.set("Error")
            power_value.set("Error")
    root.after(1000, update_display)  
    
update_display()
root.mainloop()
