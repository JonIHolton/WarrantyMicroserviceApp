import enum
import logging

from waitress import serve

import requests
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)
CORS(app)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

app.wsgi_app = DispatcherMiddleware(
    Response("Not Found", status=404), {"/api/v1/resale_orchestrator": app.wsgi_app}
)


class ResaleStatus(enum.Enum):
    LISTED = "listed"
    SOLD = "sold"
    CANCELLED = "cancelled"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


# Healthcheck
@app.route("/healthcheck", methods=["GET"])
def healthcheck():
    app.logger.info("Healthcheck endpoint reached.")
    return jsonify({"code": 200, "message": "Purchase resale ticket service is running!"})


# List tickets for resale
@app.route("/purchase_listing", methods=["POST"])
def create_listing():
    app.logger.info("Purchase listing endpoint reached.")
    data = request.get_json()
    try:
        listing_id = data["listing_id"]
        user_id = data["user_id"]
        app.logger.debug("Extracted request params")
    except:
        app.logger.debug("Failed before step 1")
        return (
            jsonify(
                {
                    "code": 422,
                    "message": "`listing_id` field or `user_id` field is not set.",
                }
            ),
            422,
        )

    app.logger.debug("Starting step 1")
    response = requests.get(
        f"http://resale-service:5000/api/v1/resale/get_listing/{listing_id}"
    )

    if response.status_code < 200 or response.status_code >= 300:
        app.logger.debug("Failed step 1")
        return (
            jsonify(
                {
                    "code": response.status_code,
                    "message": response.json().get(
                        "message",
                        "Error occurred while processing response from /get_listing!",
                    ),
                }
            ),
            response.status_code,
        )

    try:
        app.logger.debug("Extracting data from step 1")
        payment_amount = response.json()["data"]["listing_amount"]
    except:
        app.logger.debug("Failed extracting data from step 1")
        return (
            jsonify(  # Update to continue process from step 4.
                {
                    "code": 500,
                    "message": response.json().get(
                        "data",
                        "Error occurred while processing response from /get_listing!",
                    ),
                }
            ),
            500,
        )

    # simulate get stripe account
    # response = requests.get(f"http://payment-service:5002/api/v1/payment/get_stripe_account/buy/{user_id}")
    response.status_code = 200  # TODO: Remove line to get actual data

    if response.status_code < 200 or response.status_code >= 300:
        return (
            jsonify(
                {
                    "code": response.status_code,
                    "message": response.json().get(
                        "message",
                        "Error occurred while processing response from /get_listing!",
                    ),
                }
            ),
            response.status_code,
        )

    try:
        # stripe_account = response.json()["data"]["stripe_account"]
        stripe_account = 12341234
    except:
        return (
            jsonify(
                {
                    "code": 418,
                    "message": response.json().get(
                        "data",
                        "Error occurred while processing response from /get_stripe_account!",
                    ),
                }
            ),
            500,
        )
    # end simulate stripe account

    # simulate payment
    data = {
        "user_id": user_id,
        "payment_amount": payment_amount,
        "stripe_account": stripe_account,
    }
    # response = requests.post(f"http://payment-service:5002/api/v1/payment/make_payment", data=data)
    response.status_code = 200  # TODO: Remove line to get actual data

    if (
        response.status_code < 200 or response.status_code >= 300
    ):  # Check what stripe returns for payment failed
        return (
            jsonify(
                {
                    "code": response.status_code,
                    "message": response.json().get("message", "Payment failed!"),
                }
            ),
            response.status_code,
        )
    # end simulate payment

    # step 7
    data = {"listing_id": listing_id, "resale_status": ResaleStatus.SOLD.value}

    app.logger.debug("Starting step 7a")
    app.logger.debug(data)
    response = requests.patch(
        f"http://resale-service:5000/api/v1/resale/update_resale_status", json=data
    )
    app.logger.debug("Received data from step 7a")

    if (
        response.status_code < 200 or response.status_code >= 300
    ):  # Check what stripe returns for payment failed
        app.logger.debug("Response code from step 7a is not 2XX")
        return (
            jsonify(
                {
                    "code": response.status_code,
                    "message": response.json().get(
                        "message", "Resale status update failed!"
                    ),
                }
            ),
            response.status_code,
        )

    data = {"listing_id": listing_id, "payment_status": PaymentStatus.COMPLETED.value}

    app.logger.debug("Starting step 7b")
    response = requests.patch(
        "http://resale-service:5000/api/v1/resale/update_payment_status", json=data
    )
    app.logger.debug("Received data from step 7b")

    if (
        response.status_code < 200 or response.status_code >= 300
    ):  # Check what stripe returns for payment failed
        app.logger.debug("Response code from step 7b is not 2XX")
        return (
            jsonify(
                {
                    "code": response.status_code,
                    "message": response.json().get(
                        "message", "Payment status update failed!"
                    ),
                }
            ),
            response.status_code,
        )

    # continue from step 6: TODO: Confirm usage of AMQP
    data = {"user_id": user_id}

    app.logger.debug("Starting step 7c")
    # requests.post(f"http://notification-service:5003/notification/payment", json=data)
    response.status_code = 200
    app.logger.debug("Sent step 7c")

    if (
        response.status_code < 200 or response.status_code >= 300
    ):  # Check what stripe returns for payment failed
        app.logger.debug("Response code from step 7c is not 2XX")
        return (
            jsonify(
                {
                    "code": response.status_code,
                    "message": response.json().get("message", "Notification error!"),
                }
            ),
            response.status_code,
        )

    # step 8: TODO: Implement update ticket owner
    app.logger.debug("Starting step 8")
    return (
        jsonify(
            {
                "code": 200,
                "message": "Resale purchase completed and ticket ownership has been transferred!",
            }
        ),
        200,
    )


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000)
