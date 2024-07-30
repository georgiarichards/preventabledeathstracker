from enum import Enum


class CounterType(str, Enum):
    PERCENT = "percent"
    COUNT = "count"


COUNTS_LINK = "https://preventabledeathstracker.net/database/"
PERCENT_LINK = "https://preventabledeathstracker.net/reg-29-addressee-tracker-database/"

STYLE = """
<style>
        .counter-container {
            text-align: center;
            margin: 20px;
            font-family: "Arial", helvetica, arial, sans-serif;
        }
        .counter {
            font-size: 2em;
            margin: 10px 0;
        }
        .counter-description {
            font-size: 1.2em;
        }

        .button-link {
            text-decoration: none;
            color: white;
            background-color: #002147;
            padding: 5px 20px 10px;
            border-radius: 5px;
            display: inline-block;
        }
        .button-link:hover {
            background-color: #063567;
        }
    </style>
"""

PERCENT_CONTAINER = f"""
    <div class="counter-container">
        <a href="{PERCENT_LINK}" target="_blank" class="button-link">
            <div id="completedReportsCounter" class="counter">0%</div>
            <div class="counter-description">Percentage of reports with all responses published</div>
        </a>
    </div>
    """

COUNT_CONTAINER = f"""
    <div class="counter-container">
        <a href="{COUNTS_LINK}" target="_blank" class="button-link">
            <div id="totalReportsCounter" class="counter">0</div>
            <div class="counter-description">Total number of reports</div>
        </a>
    </div>
"""

SCRIPT = """
<script>
        function animateCounter(element, target, duration) {
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
