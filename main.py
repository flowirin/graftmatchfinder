import pandas as pd

# Expanded mock dataset: species, family, xylem vessel size (μm), porosity, vessel density (per mm²)
data = {
    "Species": [
        "Pistacia vera", "Juglans regia", "Corylus avellana", "Prunus dulcis", 
        "Syringa vulgaris", "Ligustrum vulgare", "Prunus avium", "Salix alba",
        "Rhus typhina", "Schinus molle"
    ],
    "Family": [
        "Anacardiaceae", "Juglandaceae", "Betulaceae", "Rosaceae", 
        "Oleaceae", "Oleaceae", "Rosaceae", "Salicaceae",
        "Anacardiaceae", "Anacardiaceae"
    ],
    "Vessel_Size_μm": [75, 150, 50, 80, 40, 45, 90, 100, 60, 70],  # Midpoints from lit
    "Porosity": [
        "ring-porous", "ring-porous", "diffuse-porous", "ring-porous", 
        "diffuse-porous", "diffuse-porous", "ring-porous", "ring-porous",
        "ring-porous", "ring-porous"
    ],
    "Vessel_Density_per_mm2": [75, 30, 100, 60, 80, 85, 50, 60, 70, 65]
}

# Create DataFrame
df = pd.DataFrame(data)
print("Dataset loaded:")
print(df)

# Compatibility scoring function
def graft_compatibility(base, candidate):
    """
    Scores grafting compatibility based on vascular 'utilities'.
    Weights: Vessel Size (60%), Porosity (30%), Density (10%).
    """
    score = 0
    
    # Xylem vessel size: ±20% tolerance
    size_diff = abs(base["Vessel_Size_μm"] - candidate["Vessel_Size_μm"]) / base["Vessel_Size_μm"]
    size_score = max(0, 1 - size_diff / 0.2) * 60  # Max 60 points
    
    # Porosity: Match = 30, mismatch = 0
    porosity_score = 30 if base["Porosity"] == candidate["Porosity"] else 0
    
    # Vessel density: ±30% tolerance
    density_diff = abs(base["Vessel_Density_per_mm2"] - candidate["Vessel_Density_per_mm2"]) / base["Vessel_Density_per_mm2"]
    density_score = max(0, 1 - density_diff / 0.3) * 10  # Max 10 points
    
    score = size_score + porosity_score + density_score
    return round(score, 2)

# Flexible baseline selection (test case: Pistacia vera)
baseline_species = "Pistacia vera"  # Change this to any species in the dataset
try:
    baseline = df[df["Species"] == baseline_species].iloc[0]
except IndexError:
    print(f"Error: '{baseline_species}' not found in dataset.")
    exit()

# Calculate compatibility for all others
results = []
for i, row in df.iterrows():
    if row["Species"] != baseline_species:
        compatibility = graft_compatibility(baseline, row)
        results.append({
            "Species": row["Species"],
            "Family": row["Family"],
            "Compatibility_Score": compatibility
        })

# Results as DataFrame, sorted by score
results_df = pd.DataFrame(results)
results_df = results_df.sort_values(by="Compatibility_Score", ascending=False)
print(f"\nGrafting compatibility with {baseline_species}:")
print(results_df)

# Optional: Save to CSV for GitHub
results_df.to_csv("graft_compatibility_results.csv", index=False)
print("\nResults saved to 'graft_compatibility_results.csv'.")