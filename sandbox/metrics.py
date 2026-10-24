def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError('Height must be positive')
    return round(weight_kg / (height_m * height_m), 2)

def categorize_bmi(bmi: float) -> str:
    if bmi < 18.5:
        return 'UNDERWEIGHT'
    elif bmi < 25.0:
        return 'NORMAL'
    elif bmi < 30.0:
        return 'OVERWEIGHT'
    else:
        return 'OBESE'
