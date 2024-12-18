from flask import Flask, jsonify
from data_generator.modified_atmosphere_packaging_machine import r_50

app = Flask(__name__)

@app.route('/simulated_data', methods=['GET'])
def get_simulated_data():
    """
    Direct endpoint for retrieving simulated `r_50` data.
    """
    return jsonify(r_50()), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8481)
