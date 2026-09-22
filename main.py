import numpy as np

from ai_parser import parse_battery_text
from fuzzy_system import FuzzyBatteryOptimizer


# ============================================================
# CONVERT NUMPY VALUES TO NORMAL PYTHON VALUES
# ============================================================

def make_json_safe(obj):

    if isinstance(obj, dict):
        return {
            key: make_json_safe(value)
            for key, value in obj.items()
        }

    if isinstance(obj, list):
        return [
            make_json_safe(value)
            for value in obj
        ]

    if isinstance(obj, tuple):
        return [
            make_json_safe(value)
            for value in obj
        ]

    if isinstance(obj, np.generic):
        return obj.item()

    return obj


# ============================================================
# MAIN BATTERY ANALYSIS
# ============================================================

def analyze_battery(user_text: str):

    # --------------------------------------------------------
    # STEP 1: AI / LLM EXTRACTION
    # --------------------------------------------------------

    print("\n[1/2] Sending description to AI parser...")

    ai_inputs = parse_battery_text(
        user_text
    )

    print("[1/2] AI extraction complete!")

    print(
        f"Battery       : {ai_inputs.battery_level}%"
    )

    print(
        f"App Usage     : {ai_inputs.app_usage}%"
    )

    print(
        f"Screen Usage  : {ai_inputs.screen_usage}%"
    )

    print(
        f"Network Usage : {ai_inputs.network_usage}%"
    )

    print(
        f"Temperature   : {ai_inputs.temperature}°C"
    )


    # --------------------------------------------------------
    # STEP 2: FUZZY LOGIC
    # --------------------------------------------------------

    print("\n[2/2] Running fuzzy logic...")

    optimizer = FuzzyBatteryOptimizer()

    fuzzy_result = optimizer.calculate_power_saving(
        battery=ai_inputs.battery_level,
        app_usage=ai_inputs.app_usage,
        screen_usage=ai_inputs.screen_usage,
        network_usage=ai_inputs.network_usage,
        temperature=ai_inputs.temperature,
    )


    # Convert NumPy values into normal Python values
    fuzzy_result = make_json_safe(
        fuzzy_result
    )


    print("[2/2] Fuzzy analysis complete!")

    print(
        f"Power-Saving Score: "
        f"{fuzzy_result['score']} / 100"
    )


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    return {
        "ai_inputs": ai_inputs.model_dump(),
        "fuzzy_result": fuzzy_result,
    }


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    example = (
        "My battery is 18%. "
        "I've been playing games for two hours, "
        "brightness is high, mobile data is on "
        "and my phone is getting very hot."
    )

    result = analyze_battery(
        example
    )

    print("\n========================================")
    print("FINAL ANALYSIS")
    print("========================================")

    print("\nAI Inputs:")
    print(result["ai_inputs"])

    print("\nFuzzy Result:")
    print(result["fuzzy_result"])