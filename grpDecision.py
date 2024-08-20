from flask import Flask, request, jsonify

import numpy as np

import os

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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
