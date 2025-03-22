import numpy as np
import pandas as pd
from math import pi

class Material:
    def __init__(self, name, rho, E, YS=0, UTS=0):
        self.name = name
        self.rho = rho  # density (g/cm^3)
        self.E = E      # Young's modulus (GPa)
        self.UTS = UTS
        self.YS = YS

# Define materials
materials = [
    Material("Aluminum 6061", 2.7, 68.9),  # https://www.matweb.com/search/DataSheet.aspx?MatGUID=626ec8cdca604f1994be4fc2bc6f7f63
    Material("Titanium", rho=4.43, E=105), # https://en.wikipedia.org/wiki/Ti-6Al-4V
    Material("PLA", 1.3, 2.35),  # https://www.matweb.com/search/QuickText.aspx?SearchText=PLA,
    Material("Alloy steel 4140", rho=7.85, E=210, YS=715),   # https://www.pcbway.com/rapid-prototyping/cnc-machining/
    Material("Mild Steel 1018", rho=7.87, E=205, YS=400), # https://www.pcbway.com/rapid-prototyping/cnc-machining/,
    Material("Carbon Fiber Plate", rho=1.6, E=200)
]

# Constants
L = 1
M = 1
c = 1
target_strain = 1
target_mass = 1

results = []

for material in materials:
    # ---- PART 1: Mass required for a given strain ----
    # Compute required I
    I_required = (M * c) / (target_strain * material.E)
    
    # Solve for radius and area
    r_required = (4 * I_required / pi) ** 0.25
    A_required = pi * r_required ** 2

    # Compute mass needed
    mass_required = material.rho * L * A_required

    # ---- PART 2: Strain for a given mass ----
    # Area from target mass
    A_from_mass = target_mass / (material.rho * L)
    r_from_mass = (A_from_mass / pi) ** 0.5
    I_from_mass = (pi / 4) * r_from_mass ** 4
    strain_from_mass = (M * c) / (I_from_mass * material.E)

    results.append({
        "Material": material.name,
        "Mass Required for Strain": mass_required,
        "Strain Achievable at Mass": strain_from_mass
    })

# Create DataFrame
df = pd.DataFrame(results).set_index("Material")

# Normalize both columns
df["Mass Ratio for Equal Strain"] = df["Mass Required for Strain"] / df["Mass Required for Strain"].min()
df["Strain Ratio for Equal Mass"] = df["Strain Achievable at Mass"] / df["Strain Achievable at Mass"].min()

# Final output
print(df[["Mass Ratio for Equal Strain", "Strain Ratio for Equal Mass"]])
