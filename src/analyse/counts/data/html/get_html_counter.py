import os

from src.analyse.counts.data.html.elements import CounterType, STYLE, PERCENT_CONTAINER, COUNT_CONTAINER, SCRIPT, \
    ADDRESSEES_CONTAINER

type_map = {
    CounterType.ADDRESSEES: ADDRESSEES_CONTAINER,
    CounterType.PERCENT: PERCENT_CONTAINER,
    CounterType.COUNT: COUNT_CONTAINER,
}


def generate_script(value: str, _type: CounterType) -> str:
    if _type == CounterType.PERCENT:
        script_template = f"""
                        element.textContent = target === 0 ? current : current + '%';
            }}, stepTime);
        }}
        let completedReportsCounter = document.getElementById('completedReportsCounter');

         setTimeout(() => {{
        animateCounterWithPercent(completedReportsCounter, {value}, 2000);}}, 500);
            </script>
        """
        return """<script>
        function animateCounterWithPercent(element, target, duration) {""" + SCRIPT + script_template

    elif _type == CounterType.COUNT:
        script_template = f"""
                                element.textContent = target === 0 ? current : current;
            }}, stepTime);
        }}
                let totalReportsCounter = document.getElementById('totalReportsCounter');

            setTimeout(() => {{
                animateCounter(totalReportsCounter, {value}, 1500);
            }}, 500);
        </script>
            """
        return """<script>
        function animateCounter(element, target, duration) {""" + SCRIPT + script_template
    elif _type == CounterType.ADDRESSEES:
        script_template = f"""
                                element.textContent = target === 0 ? current : current;
            }}, stepTime);
        }}
                let AddresseesCounter = document.getElementById('AddresseesCounter');

            setTimeout(() => {{
                animateCounter(AddresseesCounter, {value}, 1500);
            }}, 500);
        </script>
            """
        return """<script>
                function animateCounter(element, target, duration) {""" + SCRIPT + script_template


def get_html_counter(value, _type: CounterType):
    PATH = os.path.dirname(__file__)
    file_path = os.path.abspath(f"{PATH}/counters/{_type.value}.html")
    html = STYLE
    html += type_map[_type]
    html += generate_script(value, _type)
    with open(file_path, "w") as f:
        f.write(html)
