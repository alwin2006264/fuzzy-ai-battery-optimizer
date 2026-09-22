import os
import json
import re

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


# ============================================================
# BATTERY INPUT MODEL
# ============================================================

class BatteryInputs(BaseModel):
    battery_level: float = Field(ge=0, le=100)
    app_usage: float = Field(ge=0, le=100)
    screen_usage: float = Field(ge=0, le=100)
    network_usage: float = Field(ge=0, le=100)
    temperature: float = Field(ge=20, le=50)


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

llm = None

if api_key:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            google_api_key=api_key,
            timeout=30,
            max_retries=1,
        )

        print("Gemini AI parser initialized.")

    except Exception as error:
        print("Gemini initialization failed:")
        print(error)
        print("The local fallback parser will be used.")

else:
    print("GEMINI_API_KEY not found.")
    print("Gemini is unavailable.")
    print("The local fallback parser will be used.")


# ============================================================
# LOCAL FALLBACK PARSER
# ============================================================

def local_parse_battery_text(user_text: str) -> BatteryInputs:
    """
    Local fallback parser.

    This parser is used when Gemini is unavailable,
    including quota/rate-limit/server errors.

    It extracts useful battery information from
    natural-language descriptions using rules.
    """

    text = user_text.lower()


    # --------------------------------------------------------
    # BATTERY LEVEL
    # --------------------------------------------------------

    battery_level = 50.0

    battery_match = re.search(
        r"(?:battery|charge|charged)\D{0,20}(\d{1,3})\s*%",
        text
    )

    if battery_match:

        battery_level = float(
            battery_match.group(1)
        )

    else:

        battery_match = re.search(
            r"battery\D{0,10}(\d{1,3})",
            text
        )

        if battery_match:

            battery_level = float(
                battery_match.group(1)
            )

    battery_level = max(
        0,
        min(100, battery_level)
    )


    # --------------------------------------------------------
    # APPLICATION / CPU USAGE
    # --------------------------------------------------------

    app_usage = 35.0

    heavy_apps = [
        "gaming",
        "game",
        "games",
        "pubg",
        "bgmi",
        "cod",
        "call of duty",
        "genshin",
        "fortnite",
        "video editing",
        "3d",
        "rendering",
        "streaming"
    ]

    medium_apps = [
        "youtube",
        "netflix",
        "video",
        "music",
        "instagram",
        "facebook",
        "browser",
        "chrome"
    ]

    light_apps = [
        "messaging",
        "message",
        "whatsapp",
        "reading",
        "calculator",
        "email",
        "notes"
    ]


    if any(
        word in text
        for word in heavy_apps
    ):

        app_usage = 90.0

    elif any(
        word in text
        for word in medium_apps
    ):

        app_usage = 65.0

    elif any(
        word in text
        for word in light_apps
    ):

        app_usage = 30.0


    # --------------------------------------------------------
    # SCREEN USAGE
    # --------------------------------------------------------

    screen_usage = 40.0

    if any(
        word in text
        for word in [
            "high brightness",
            "maximum brightness",
            "full brightness",
            "bright screen"
        ]
    ):

        screen_usage = 90.0

    elif any(
        word in text
        for word in [
            "medium brightness",
            "normal brightness"
        ]
    ):

        screen_usage = 60.0

    elif any(
        word in text
        for word in [
            "low brightness",
            "dim screen"
        ]
    ):

        screen_usage = 25.0

    elif any(
        word in text
        for word in [
            "gaming",
            "game",
            "games",
            "video",
            "youtube",
            "netflix"
        ]
    ):

        screen_usage = 75.0


    # --------------------------------------------------------
    # NETWORK USAGE
    # --------------------------------------------------------

    network_usage = 35.0

    if any(
        word in text
        for word in [
            "hotspot",
            "mobile data",
            "5g",
            "5g data",
            "download",
            "downloads",
            "streaming",
            "online gaming"
        ]
    ):

        network_usage = 80.0

    elif any(
        word in text
        for word in [
            "wifi",
            "wi-fi",
            "internet"
        ]
    ):

        network_usage = 50.0

    elif any(
        word in text
        for word in [
            "airplane mode",
            "offline",
            "no internet"
        ]
    ):

        network_usage = 10.0


    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    temperature = 32.0

    if any(
        word in text
        for word in [
            "very hot",
            "extremely hot",
            "overheating",
            "overheated"
        ]
    ):

        temperature = 45.0

    elif any(
        word in text
        for word in [
            "hot",
            "heating up"
        ]
    ):

        temperature = 42.0

    elif "warm" in text:

        temperature = 37.0

    elif any(
        word in text
        for word in [
            "cool",
            "cold"
        ]
    ):

        temperature = 28.0


    # --------------------------------------------------------
    # ADDITIONAL ADJUSTMENTS
    # --------------------------------------------------------

    # Long gaming sessions increase
    # application and screen load.

    if any(
        word in text
        for word in [
            "two hours",
            "3 hours",
            "three hours",
            "four hours",
            "long gaming",
            "for hours"
        ]
    ):

        app_usage = max(
            app_usage,
            90.0
        )

        screen_usage = max(
            screen_usage,
            80.0
        )


    # Gaming + mobile data is particularly intensive.

    if (
        any(
            word in text
            for word in [
                "gaming",
                "game",
                "games"
            ]
        )
        and
        any(
            word in text
            for word in [
                "mobile data",
                "5g",
                "hotspot"
            ]
        )
    ):

        network_usage = max(
            network_usage,
            80.0
        )


    # Heavy load usually means
    # higher temperature.

    if (
        app_usage >= 80
        and
        screen_usage >= 75
        and
        temperature < 40
    ):

        temperature = 40.0


    # --------------------------------------------------------
    # VALIDATED RESULT
    # --------------------------------------------------------

    result = BatteryInputs(
        battery_level=battery_level,
        app_usage=app_usage,
        screen_usage=screen_usage,
        network_usage=network_usage,
        temperature=temperature,
    )

    return result


# ============================================================
# GEMINI AI PARSER
# ============================================================

def parse_with_gemini(
    user_text: str
) -> BatteryInputs:

    if llm is None:

        raise RuntimeError(
            "Gemini AI is not currently available."
        )


    # --------------------------------------------------------
    # AI PROMPT
    # --------------------------------------------------------

    prompt = f"""
You are an AI component of a smartphone
battery optimization system.

Analyze the user's smartphone usage description.

Return ONLY valid JSON.

Do not return Markdown.

Do not use ```json.

Do not add explanations.

The JSON must contain exactly these fields:

{{
    "battery_level": number,
    "app_usage": number,
    "screen_usage": number,
    "network_usage": number,
    "temperature": number
}}

Rules:

1. battery_level

   Battery percentage from 0 to 100.

   If the user explicitly gives the battery
   percentage, use that exact value.


2. app_usage

   Estimate application/CPU usage from 0 to 100.

   Heavy gaming, video editing and 3D applications
   should normally be considered high usage.

   Messaging, reading, calculator and other
   light applications should normally be considered
   low usage.


3. screen_usage

   Estimate screen usage intensity from 0 to 100.

   High brightness, long screen-on time,
   video and gaming should normally produce
   high screen usage.

   Short or light screen use should normally
   produce lower screen usage.


4. network_usage

   Estimate network usage from 0 to 100.

   Hotspot, mobile data, 5G, streaming and
   downloads should normally produce high
   network usage.

   Light Wi-Fi or occasional internet use
   should normally produce low or medium
   network usage.


5. temperature

   Estimate phone temperature in Celsius.

   "Hot" means approximately 40-45 C.

   "Warm" means approximately 35-40 C.

   Normal conditions are approximately 28-34 C.

   Keep the temperature between 20 and 50 C.


6. All usage values must be between 0 and 100.


7. If some information is not explicitly stated,
   make a reasonable estimate.


User description:

{user_text}
"""


    # --------------------------------------------------------
    # SEND REQUEST
    # --------------------------------------------------------

    print("\nSending request to Gemini...")

    response = llm.invoke(prompt)

    print("Gemini response received.")


    # --------------------------------------------------------
    # EXTRACT RESPONSE CONTENT
    # --------------------------------------------------------

    content = response.content


    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:

                    text_parts.append(
                        str(item["text"])
                    )

            elif isinstance(item, str):

                text_parts.append(item)


        content = "".join(
            text_parts
        )


    content = str(content).strip()


    # --------------------------------------------------------
    # REMOVE MARKDOWN CODE BLOCKS IF PRESENT
    # --------------------------------------------------------

    if content.startswith("```json"):

        content = content[7:]

    elif content.startswith("```"):

        content = content[3:]


    if content.endswith("```"):

        content = content[:-3]


    content = content.strip()


    # --------------------------------------------------------
    # PARSE JSON
    # --------------------------------------------------------

    try:

        data = json.loads(content)

    except json.JSONDecodeError as error:

        print(
            "\nGemini returned invalid JSON:"
        )

        print(content)

        raise ValueError(
            f"Gemini returned invalid JSON: {error}"
        )


    # --------------------------------------------------------
    # VALIDATE AI OUTPUT
    # --------------------------------------------------------

    try:

        result = BatteryInputs(
            **data
        )

    except Exception as error:

        print(
            "\nInvalid battery data returned by Gemini:"
        )

        print(data)

        raise ValueError(
            f"AI output failed validation: {error}"
        )


    return result


# ============================================================
# MAIN PARSER WITH AUTOMATIC FALLBACK
# ============================================================

def parse_battery_text(
    user_text: str
) -> BatteryInputs:

    # --------------------------------------------------------
    # Try Gemini first
    # --------------------------------------------------------

    try:

        result = parse_with_gemini(
            user_text
        )

        print(
            "\nUsing Gemini AI parser."
        )

        return result


    except Exception as error:

        error_text = str(error)


        # ----------------------------------------------------
        # Gemini unavailable / quota / rate limit
        # ----------------------------------------------------

        if (
            "429" in error_text
            or
            "RESOURCE_EXHAUSTED"
            in error_text
            or
            "quota"
            in error_text.lower()
            or
            "rate limit"
            in error_text.lower()
        ):

            print(
                "\nGemini quota or rate limit "
                "is unavailable."
            )

        else:

            print(
                "\nGemini parser failed:"
            )

            print(error)


        # ----------------------------------------------------
        # Use local fallback
        # ----------------------------------------------------

        print(
            "\nSwitching to local fallback parser..."
        )

        result = local_parse_battery_text(
            user_text
        )

        print(
            "\nLocal fallback extraction complete:"
        )

        print(
            f"battery_level={result.battery_level}"
        )

        print(
            f"app_usage={result.app_usage}"
        )

        print(
            f"screen_usage={result.screen_usage}"
        )

        print(
            f"network_usage={result.network_usage}"
        )

        print(
            f"temperature={result.temperature}"
        )

        return result