from flask import Flask, render_template, request
import re

app = Flask(__name__)

def analyze_code(code):
    lines = code.split('\n')

    loop_depth = 0
    max_depth = 0
    loop_count = 0
    recursion = False
    sorting = False

    function_name = None

    for line in lines:
        line = line.strip()

        if line.startswith("def"):
            function_name = line.split()[1].split('(')[0]

        if function_name and function_name in line and "def" not in line:
            recursion = True

        if re.search(r'\bfor\b|\bwhile\b', line):
            loop_count += 1
            loop_depth += 1
            max_depth = max(max_depth, loop_depth)

        if line == "" or "}" in line:
            loop_depth = max(0, loop_depth - 1)

        if "sort" in line.lower():
            sorting = True

    if recursion:
        complexity = "O(2^n) or recursive"
    elif sorting:
        complexity = "O(n log n)"
    elif max_depth == 0:
        complexity = "O(1)"
    elif max_depth == 1:
        complexity = "O(n)"
    elif max_depth == 2:
        complexity = "O(n²)"
    else:
        complexity = f"O(n^{max_depth})"

    insights = []

    if recursion:
        insights.append("Recursion detected → may lead to exponential complexity")

    if max_depth >= 2:
        insights.append("Nested loops detected → higher time complexity")

    if sorting:
        insights.append("Sorting operation found → expected O(n log n)")

    if loop_count == 0:
        insights.append("No loops → constant time operation")

    if loop_count > 3:
        insights.append("Multiple loops detected → consider optimization")

    return complexity, insights, loop_count, max_depth, recursion, sorting


@app.route('/', methods=['GET', 'POST'])
def index():
    complexity = None
    insights = []
    loop_count = 0
    max_depth = 0
    recursion = False
    sorting = False
    code_input = ""

    if request.method == 'POST':
        code_input = request.form['code']

        if code_input.strip() != "":
            complexity, insights, loop_count, max_depth, recursion, sorting = analyze_code(code_input)

    return render_template('index.html',
                           complexity=complexity,
                           insights=insights,
                           loop_count=loop_count,
                           max_depth=max_depth,
                           recursion=recursion,
                           sorting=sorting,
                           code_input=code_input)


if __name__ == '__main__':
    app.run(debug=True)