from flask import Flask, jsonify, Blueprint, abort
from app import mainData, mainFunction, mainErrorHandler
app_bp = Blueprint('app_bp',__name__)

# GET ROUTE
@app_bp.route('/get/<cat>', methods=['GET'])
def get_route(cat):
    if cat in mainData:
        category = mainData[cat]
        return mainFunction(False, category)
    else:
        abort(404)
    
# COUNT ROUTE
@app_bp.route('/count/<cat>', methods=['GET'])
def count_route(cat):
    if cat in mainData:
        category = mainData[cat]
        return mainFunction(True, category)
    else:
        abort(404)

@app_bp.app_errorhandler(mainErrorHandler) 
def handle_main_error(error):
    response = error.to_dict()
    return jsonify(response), error.status_code

@app_bp.app_errorhandler(404)
def handle_404(error):
    response = {}
    response['error'] = 'NotFound'
    response['message'] = 'Page not found.'
    response['statusCode'] = 404
    return jsonify(response), 404