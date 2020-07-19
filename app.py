import json

from flask import Flask, request
from typing import List, Tuple, Dict, Optional

from csp import CSP
from min_conflict import MinConflict
from queen_arc_constraint import QueenArcConstraint
from state import State
from queen_genetic import solve
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app = Flask(__name__)


@app.route('/min-conflict', methods=['POST'])
@cross_origin()
def min_conflict_solve():
    req_data = request.get_json()
    k: int = req_data['k']
    init_state: List[int] = req_data['initState']
    iteration: int = req_data['iteration']
    columns: List[int] = list(range(k))
    rows: Dict[int, List[int]] = {}
    for column in columns:
        rows[column] = list(range(k))
    csp: CSP[int, int] = CSP(columns, rows)
    for i in range(len(columns) - 1):
        for j in range(i + 1, len(columns)):
            csp.add_constraint(QueenArcConstraint(i, j))
    min_conflict: MinConflict[int, int] = MinConflict(csp, State[int, int]({i: x for i, x in enumerate(init_state)}),
                                                      iteration)
    solution, steps, time = min_conflict.solve()
    response = app.response_class(
        response=json.dumps({"steps": steps, "time": time}),
        status=200,
        mimetype='application/json'
    )
    return response


@app.route('/genetic-algorithm', methods=['POST'])
@cross_origin()
def ga():
    req_data = request.get_json()
    k = req_data['k']
    generations, time, isHalt = solve(k)
    if not isHalt:
        response = app.response_class(
            response="Server TimeOut",
            status=500
        )
    else:
        response = app.response_class(
            response=json.dumps({"generations": generations, "time": time}),
            status=200,
            mimetype='application/json'
        )
    return response
