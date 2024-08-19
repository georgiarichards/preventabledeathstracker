from enum import Enum


class CounterType(str, Enum):
    PERCENT = "percent"
    COUNT = "count"
    ADDRESSEES = "addressees"


COUNTS_LINK = "https://preventabledeathstracker.net/database/"
ADDRESSEES_LINK = "https://preventabledeathstracker.net/reg-29-addressee-tracker-database/"
PERCENT_LINK = "https://preventabledeathstracker.net/database/responses/"

STYLE = """
<style>
    .counter-container {
        text-align: center;
        margin: 20px;
        font-family: "Alegreya Sans", sans-serif;
    }

    .button-link {
        width: 320px;
        height: 180px;
        text-decoration: none;
        color: white;
        background-color: #002147;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        padding: 5px 20px 10px;
    }

    .button-link:hover {
        background-color: #063567;
    }

    .counter {
        font-size: 2em;
        margin: 10px 0;
    }

    .counter-description {
        font-size: 1.2em;
    }
</style>

"""

PERCENT_CONTAINER = f"""
    <div class="counter-container">
        <a href="{PERCENT_LINK}" target="_blank" class="button-link">
            <div id="completedReportsCounter" class="counter">0%</div>
            <div class="counter-description" id="percent-description">Coroners reports with responses</div>
        </a>
    </div>
    """

COUNT_CONTAINER = f"""
    <div class="counter-container">
        <a href="{COUNTS_LINK}" target="_blank" class="button-link">
            <div id="totalReportsCounter" class="counter">0</div>
            <div class="counter-description" id="counter-description">Coroners reports</div>
        </a>
    </div>
"""

ADDRESSEES_CONTAINER = f"""
    <div class="counter-container">
        <a href="{ADDRESSEES_LINK}" target="_blank" class="button-link">
            <div id="AddresseesCounter" class="counter">0</div>
            <div class="counter-description" id="addressees-counter-description">Addressees who have received reports</div>
        </a>
    </div>
"""

SCRIPT = """
            let start = 0;
            let range = target - start;
            let increment = target > 100 ? Math.ceil(range / (duration / 10)) : Math.ceil(range / (duration / 100));
            let current = start;
            let stepTime = Math.abs(Math.floor(duration / range));
            let timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    clearInterval(timer);
                    current = target;
                }
"""
