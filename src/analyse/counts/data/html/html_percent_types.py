import os
from enum import Enum


class StatusCounter(str, Enum):
    PENDING = "pending"
    OVERDUE = "overdue"
    COMPLETED = "completed"
    PARTIAL = "partial"


status_map = {
    StatusCounter.COMPLETED: ("#248024FF", "PFDs have all responses published (i.e. completed)"),
    StatusCounter.PARTIAL: ("#DCAF1DFF", "PFDs have some but not all required responses published (i.e. partial)"),
    StatusCounter.OVERDUE: ("#B10707FF", "PFDs have no responses published (i.e. are overdue)"),
    StatusCounter.PENDING: ("#0749ACFF", "don’t yet have a response due (i.e. pending – it’s within 56 days of the date of report)")
}


def get_status_html_counter(value_num: int, value_percent: float, _type: StatusCounter) -> None:
    map_res = status_map[_type]

    BLOCK = f"""
    <style>
            .counter-container {{
                text-align: center;
                margin: 20px;
                font-family: "Alegreya Sans", sans-serif;
            }}
            .counter {{
                font-size: 2em;
                margin: 10px 0;
            }}
            .counter-description {{
                font-size: 1.2em;
            }}

            .block-{_type.value} {{
                width: 350px;
                height: 200px;
                text-decoration: none;
                color: white;
                background-color: {map_res[0]};
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column; 
                padding: 5px 20px 10px;
    }}
        </style>
        <div class="counter-container">
            <div class="block-{_type.value}">
                <div id="{_type.value}-percent" class="counter">0%</div>
                <div class="counter-description" id="{_type.value}-percent-description"><b>{value_num}</b> {map_res[1]}</div>
        </div>
        
        <script>
    function animateCounterWithPercent(element, target, duration) {{
            let start = 0;
            let range = target - start;
            let increment = target > 100 ? Math.ceil(range / (duration / 10)) : Math.ceil(range / (duration / 100));
            let current = start;
            let stepTime = Math.abs(Math.floor(duration / range));
            let timer = setInterval(() => {{
                current += increment;
                if (current >= target) {{
                    clearInterval(timer);
                    current = target;
                }}
                    element.textContent = target === 0 ? current : current + '%';
        }}, stepTime);
    }}
    let {_type.value}Counter = document.getElementById('{_type.value}-percent');

     setTimeout(() => {{
    animateCounterWithPercent({_type.value}Counter, {value_percent}, 2000);}}, 500);
        </script>
        """

    PATH = os.path.dirname(__file__)
    file_path = os.path.abspath(f"{PATH}/counters/statuses/{_type.value}.html")
    with open(file_path, "w") as f:
        f.write(BLOCK)
