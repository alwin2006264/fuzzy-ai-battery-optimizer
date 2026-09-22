import numpy as np
import skfuzzy as fuzz


# ============================================================
# FUZZY BATTERY OPTIMIZER
# ============================================================

class FuzzyBatteryOptimizer:

    def __init__(self):
        # ----------------------------------------------------
        # 1. INPUT VARIABLES
        # ----------------------------------------------------

        # Battery: 0 to 100%
        self.battery = np.arange(0, 101, 1)

        # App usage: 0 to 100
        self.app_usage = np.arange(0, 101, 1)

        # Screen usage: 0 to 100
        self.screen_usage = np.arange(0, 101, 1)

        # Network usage: 0 to 100
        self.network_usage = np.arange(0, 101, 1)

        # Temperature: 20 to 50°C
        self.temperature = np.arange(20, 51, 1)

        # Output: Power saving score
        self.power_saving = np.arange(0, 101, 1)

        # ----------------------------------------------------
        # 2. MEMBERSHIP FUNCTIONS
        # ----------------------------------------------------

        # Battery membership functions
        self.battery_very_low = fuzz.trapmf(
            self.battery,
            [0, 0, 10, 25]
        )

        self.battery_low = fuzz.trimf(
            self.battery,
            [10, 30, 50]
        )

        self.battery_medium = fuzz.trimf(
            self.battery,
            [30, 55, 75]
        )

        self.battery_high = fuzz.trapmf(
            self.battery,
            [60, 80, 100, 100]
        )

        # App usage membership functions
        self.app_low = fuzz.trapmf(
            self.app_usage,
            [0, 0, 20, 40]
        )

        self.app_medium = fuzz.trimf(
            self.app_usage,
            [20, 50, 80]
        )

        self.app_high = fuzz.trapmf(
            self.app_usage,
            [60, 80, 100, 100]
        )

        # Screen usage membership functions
        self.screen_low = fuzz.trapmf(
            self.screen_usage,
            [0, 0, 20, 40]
        )

        self.screen_medium = fuzz.trimf(
            self.screen_usage,
            [20, 50, 80]
        )

        self.screen_high = fuzz.trapmf(
            self.screen_usage,
            [60, 80, 100, 100]
        )

        # Network usage membership functions
        self.network_low = fuzz.trapmf(
            self.network_usage,
            [0, 0, 20, 40]
        )

        self.network_medium = fuzz.trimf(
            self.network_usage,
            [20, 50, 80]
        )

        self.network_high = fuzz.trapmf(
            self.network_usage,
            [60, 80, 100, 100]
        )

        # Temperature membership functions
        self.temperature_cool = fuzz.trapmf(
            self.temperature,
            [20, 20, 25, 30]
        )

        self.temperature_normal = fuzz.trimf(
            self.temperature,
            [25, 32, 39]
        )

        self.temperature_hot = fuzz.trapmf(
            self.temperature,
            [35, 40, 50, 50]
        )

        # ----------------------------------------------------
        # 3. OUTPUT MEMBERSHIP FUNCTIONS
        # ----------------------------------------------------

        self.saving_none = fuzz.trapmf(
            self.power_saving,
            [0, 0, 10, 20]
        )

        self.saving_low = fuzz.trimf(
            self.power_saving,
            [10, 25, 40]
        )

        self.saving_medium = fuzz.trimf(
            self.power_saving,
            [30, 50, 70]
        )

        self.saving_high = fuzz.trimf(
            self.power_saving,
            [60, 75, 90]
        )

        self.saving_extreme = fuzz.trapmf(
            self.power_saving,
            [80, 90, 100, 100]
        )

    # ========================================================
    # MEMBERSHIP CALCULATION
    # ========================================================

    def membership_values(
        self,
        battery,
        app_usage,
        screen_usage,
        network_usage,
        temperature
    ):

        battery_values = {
            "very_low": fuzz.interp_membership(
                self.battery,
                self.battery_very_low,
                battery
            ),

            "low": fuzz.interp_membership(
                self.battery,
                self.battery_low,
                battery
            ),

            "medium": fuzz.interp_membership(
                self.battery,
                self.battery_medium,
                battery
            ),

            "high": fuzz.interp_membership(
                self.battery,
                self.battery_high,
                battery
            )
        }

        app_values = {
            "low": fuzz.interp_membership(
                self.app_usage,
                self.app_low,
                app_usage
            ),

            "medium": fuzz.interp_membership(
                self.app_usage,
                self.app_medium,
                app_usage
            ),

            "high": fuzz.interp_membership(
                self.app_usage,
                self.app_high,
                app_usage
            )
        }

        screen_values = {
            "low": fuzz.interp_membership(
                self.screen_usage,
                self.screen_low,
                screen_usage
            ),

            "medium": fuzz.interp_membership(
                self.screen_usage,
                self.screen_medium,
                screen_usage
            ),

            "high": fuzz.interp_membership(
                self.screen_usage,
                self.screen_high,
                screen_usage
            )
        }

        network_values = {
            "low": fuzz.interp_membership(
                self.network_usage,
                self.network_low,
                network_usage
            ),

            "medium": fuzz.interp_membership(
                self.network_usage,
                self.network_medium,
                network_usage
            ),

            "high": fuzz.interp_membership(
                self.network_usage,
                self.network_high,
                network_usage
            )
        }

        temperature_values = {
            "cool": fuzz.interp_membership(
                self.temperature,
                self.temperature_cool,
                temperature
            ),

            "normal": fuzz.interp_membership(
                self.temperature,
                self.temperature_normal,
                temperature
            ),

            "hot": fuzz.interp_membership(
                self.temperature,
                self.temperature_hot,
                temperature
            )
        }

        return {
            "battery": battery_values,
            "app": app_values,
            "screen": screen_values,
            "network": network_values,
            "temperature": temperature_values
        }

    # ========================================================
    # FUZZY RULE ENGINE
    # ========================================================

    def calculate_power_saving(
        self,
        battery,
        app_usage,
        screen_usage,
        network_usage,
        temperature
    ):

        values = self.membership_values(
            battery,
            app_usage,
            screen_usage,
            network_usage,
            temperature
        )

        b = values["battery"]
        a = values["app"]
        s = values["screen"]
        n = values["network"]
        t = values["temperature"]

        # Output activation levels
        none_level = 0
        low_level = 0
        medium_level = 0
        high_level = 0
        extreme_level = 0

        # ----------------------------------------------------
        # RULES
        # ----------------------------------------------------

        # Rule 1
        extreme_level = max(
            extreme_level,
            min(b["very_low"], a["high"])
        )

        # Rule 2
        extreme_level = max(
            extreme_level,
            min(b["very_low"], s["high"])
        )

        # Rule 3
        extreme_level = max(
            extreme_level,
            min(b["very_low"], n["high"])
        )

        # Rule 4
        extreme_level = max(
            extreme_level,
            min(b["low"], a["high"], s["high"])
        )

        # Rule 5
        extreme_level = max(
            extreme_level,
            min(b["low"], t["hot"])
        )

        # Rule 6
        high_level = max(
            high_level,
            min(b["low"], a["high"])
        )

        # Rule 7
        high_level = max(
            high_level,
            min(b["low"], s["high"])
        )

        # Rule 8
        high_level = max(
            high_level,
            min(b["medium"], a["high"])
        )

        # Rule 9
        high_level = max(
            high_level,
            min(b["medium"], s["high"], n["high"])
        )

        # Rule 10
        high_level = max(
            high_level,
            min(b["medium"], t["hot"])
        )

        # Rule 11
        medium_level = max(
            medium_level,
            min(b["medium"], a["medium"])
        )

        # Rule 12
        medium_level = max(
            medium_level,
            min(b["medium"], s["medium"])
        )

        # Rule 13
        medium_level = max(
            medium_level,
            min(b["low"], a["medium"])
        )

        # Rule 14
        medium_level = max(
            medium_level,
            min(b["high"], a["medium"])
        )

        # Rule 15
        low_level = max(
            low_level,
            min(b["high"], a["low"])
        )

        # Rule 16
        low_level = max(
            low_level,
            min(b["high"], s["low"])
        )

        # Rule 17
        low_level = max(
            low_level,
            min(b["high"], n["low"])
        )

        # Rule 18
        low_level = max(
            low_level,
            min(b["medium"], a["low"], s["low"])
        )

        # Rule 19
        none_level = max(
            none_level,
            min(b["high"], a["low"], s["low"], n["low"])
        )

        # Rule 20
        extreme_level = max(
            extreme_level,
            min(a["high"], s["high"], t["hot"])
        )

        # ----------------------------------------------------
        # AGGREGATION
        # ----------------------------------------------------

        aggregated = np.fmax(
            none_level * self.saving_none,
            np.fmax(
                low_level * self.saving_low,
                np.fmax(
                    medium_level * self.saving_medium,
                    np.fmax(
                        high_level * self.saving_high,
                        extreme_level * self.saving_extreme
                    )
                )
            )
        )

        # ----------------------------------------------------
        # DEFUZZIFICATION
        # ----------------------------------------------------

        if np.sum(aggregated) == 0:
            score = 50.0
        else:
            score = fuzz.defuzz(
                self.power_saving,
                aggregated,
                "centroid"
            )

        return {
            "score": round(float(score), 2),
            "membership": values,
            "rule_activation": {
                "none": round(none_level, 3),
                "low": round(low_level, 3),
                "medium": round(medium_level, 3),
                "high": round(high_level, 3),
                "extreme": round(extreme_level, 3)
            }
        }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    optimizer = FuzzyBatteryOptimizer()

    scenarios = [
        {
            "name": "Critical Battery / Heavy Usage",
            "battery": 10,
            "app": 90,
            "screen": 90,
            "network": 85,
            "temperature": 42
        },
        {
            "name": "Normal Battery / Normal Usage",
            "battery": 55,
            "app": 50,
            "screen": 50,
            "network": 50,
            "temperature": 32
        },
        {
            "name": "High Battery / Light Usage",
            "battery": 90,
            "app": 15,
            "screen": 15,
            "network": 10,
            "temperature": 27
        }
    ]

    for scenario in scenarios:

        result = optimizer.calculate_power_saving(
            battery=scenario["battery"],
            app_usage=scenario["app"],
            screen_usage=scenario["screen"],
            network_usage=scenario["network"],
            temperature=scenario["temperature"]
        )

        print("\n========================================")
        print(scenario["name"])
        print("========================================")

        print(f"Battery       : {scenario['battery']}%")
        print(f"App Usage     : {scenario['app']}")
        print(f"Screen Usage  : {scenario['screen']}")
        print(f"Network Usage : {scenario['network']}")
        print(f"Temperature   : {scenario['temperature']}°C")

        print(f"\nPower Saving Score: {result['score']}/100")

        print("\nFuzzy Rule Activation:")

        for rule, value in result["rule_activation"].items():
            print(f"{rule.capitalize():10}: {value}")