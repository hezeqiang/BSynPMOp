def generate_three_phases(coil_number):
    """
    Generate a phases dictionary for a three-phase winding.

    Args:
        coil_number (int): Total number of coils (e.g., 12, 15, 21).

    Returns:
        list: A list of dictionaries representing the phases.
    """
    # Ensure coil_number is divisible by 3
    if coil_number % 3 != 0:
        raise ValueError("The coil number must be divisible by 3 for a balanced three-phase system.")
    
    # Calculate coils per phase
    coils_per_phase = coil_number // 3

    # Generate phase data
    Phases = [
        {
            "name": f"Phase_A",
            "current": "ImA",
            "group": [f"A_{i+1}" for i in range(coils_per_phase)]
        },
        {
            "name": f"Phase_B",
            "current": "ImB",
            "group": [f"B_{i+1}" for i in range(coils_per_phase)]
        },
        {
            "name": f"Phase_C",
            "current": "ImC",
            "group": [f"C_{i+1}" for i in range(coils_per_phase)]
        }
    ]
    return Phases

def generate_two_phases(coil_number):
    """
    Generate a dictionary for two-phase (a and b) winding.

    Args:
        coil_number (int): Total number of coils (e.g., 12, 18, 24).

    Returns:
        list: A list of dictionaries representing Phase a and Phase b.
    """
    # Ensure coil_number is divisible by 2
    if coil_number % 2 != 0:
        raise ValueError("The coil number must be divisible by 2 for a balanced two-phase system.")
    
    # Calculate coils per phase
    coils_per_phase = coil_number // 2

    # Generate phase data for a and b
    Phases = [
        {
            "name": "Phase_sa",
            "current": "Is_a",
            "group": [f"sa_{i+1}" for i in range(coils_per_phase)]
        },
        {
            "name": "Phase_sb",
            "current": "Is_b",
            "group": [f"sb_{i+1}" for i in range(coils_per_phase)]
        }
    ]
    return Phases


# # Example Usage
if __name__ == '__main__':
     
    SuspensionPhases = generate_two_phases(12)
    print(SuspensionPhases)