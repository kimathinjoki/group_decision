from flask import Flask, request, jsonify

import numpy as np

app = Flask(__name__)

@app.route('/group_decision', methods=['POST'])


def group_decision():
    data = request.get_json("data", [])

    results = {}

    for column, values in data.items():
        num_val = [float(i) for i in values if isinstance(i, (int, float))]
        if num_val:
            avg = np.mean(num_val)
            results[column] = avg
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)