import math
import re

def convert_frequency(freq_str):
    match = re.match(r"(\d+\.?\d*)\s*(GHz|MHz|Hz)?", freq_str, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid frequency input. Use format like '10 GHz' or '500 MHz'.")
    value, unit = match.groups()
    value = float(value)
    
    if unit is None or unit.lower() == "hz":
        return value
    elif unit.lower() == "mhz":
        return value * 1e6
    elif unit.lower() == "ghz":
        return value * 1e9
    else:
        raise ValueError("Unsupported frequency unit")

def convert_height(height_str):
    match = re.match(r"(\d+\.?\d*)\s*(mm|mil)?", height_str, re.IGNORECASE)
    if not match:
        raise ValueError("Invalid height input. Use format like '1.6 mm' or '62 mil'.")
    value, unit = match.groups()
    value = float(value)
    
    if unit is None or unit.lower() == "mm":
        return value * 1e-3  # Convert mm to meters
    elif unit.lower() == "mil":
        return value * 2.54e-5  # Convert mil to meters
    else:
        raise ValueError("Unsupported height unit")

def calculate_patch_antenna(freq, er, h):
    c = 3e8  # Speed of light in m/s
    f = freq  # Frequency in Hz (already converted)
    
    # Effective dielectric constant
    e_eff = (er + 1) / 2 + ((er - 1) / 2) * (1 / math.sqrt(1 + (12 * h)))
    
    # Patch width (W)
    W = c / (2 * f * math.sqrt((er + 1) / 2))
    
    # Effective length (Leff)
    Leff = c / (2 * f * math.sqrt(e_eff))
    
    # Length extension (delta L)
    delta_L = 0.412 * h * ((e_eff + 0.3) * (W / h + 0.264)) / ((e_eff - 0.258) * (W / h + 0.8))
    
    # Actual patch length (L)
    L = Leff - 2 * delta_L
    
    # Calculate feed point location y0
    Rin = 90  # Approximate edge resistance (this may vary)
    y0 = (L / math.pi) * math.acos(math.sqrt(50 / Rin))
    
    return W * 1000, L * 1000, y0 * 1000  # Convert to mm

def run_calculations(freq_str, er, height_str):
    freq = convert_frequency(freq_str)
    h = convert_height(height_str)
    return calculate_patch_antenna(freq, er, h)

if __name__ == "__main__":
    freq_str = input("Enter Frequency (GHz, MHz, Hz): ")
    er = float(input("Enter Dielectric Constant: "))
    height_str = input("Enter Substrate Height (mm, mil): ")
    
    width, length, feed_point = run_calculations(freq_str, er, height_str)
    
    print("\nPatch Antenna Dimensions:")
    print(f"Width: {width:.2f} mm")
    print(f"Length: {length:.2f} mm")
    print(f"Feed Point Location: {feed_point:.2f} mm")
