from flask import jsonify, request, Blueprint, Response, current_app as app
import uuid

wallstreet = Blueprint('wallstreet', __name__)


@wallstreet.route('/ping', methods=['GET'])
def test():
    return "pong"


@wallstreet.route('/currencies')
def fetch_all_currencies():
    tid = uuid.uuid4()
    app.logger.info(f"got new transaction with id {tid} for fetching all currencies")

    currencies = app.mongo.db.currencies.find({})

    data = []
    for currency in currencies:
        data.append({
            "currency_id": currency["currency_id"],
            "name": currency["name"]
        })

    app.logger.info(f"{tid}: got successful all currencies, return them and going to sleep")
    return jsonify(status="OK",
                   status_code=200,
                   data=data)


@wallstreet.route('/<currency_id>')
def fetch_currency_by_id(currency_id):
    tid = uuid.uuid4()
    app.logger.info(f"got new transaction with id {tid} to fetch a currency by id")

    currency_id = currency_id.upper()

    currency = app.mongo.db.currencies.find_one_or_404({"currency_id": currency_id})

    data = {
        "currency_id": currency["currency_id"],
        "name": currency["name"]
    }

    return jsonify(status="OK",
                   status_code=200,
                   data=data)

@wallstreet.errorhandler(404)
def page_not_found(e):
    return jsonify(status="ERROR",
                   status_code=404,
                   message="requested resources not found"), 404