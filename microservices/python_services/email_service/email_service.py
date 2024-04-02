from postmarker.core import PostmarkClient
import amqp_connection
import json
import pika

e_queue_name = 'Email'        # queue to be subscribed by Email microservice
OA_queue_name = 'OfferAlternative'
shipping_queue_name = "Shipping"
client = PostmarkClient(server_token='5200ad5e-6357-4739-9c62-36bf526301fc')

from_email = 'darrell.tan.2022@scis.smu.edu.sg'
to_email = ''
subject = 'Graphic Card Warranty Update'
body = 'This is a test email sent using Postmark.'


def queues(channel1,channel2,channel3):
    try:
        # set up a consumer and start to wait for coming messages
        channel1.basic_consume(queue=e_queue_name, on_message_callback=callback, auto_ack=True)
        channel2.basic_consume(queue=OA_queue_name, on_message_callback=callback2, auto_ack=True)
        # channel3.basic_consume(queue=shipping_queue_name, on_message_callback=callback3, auto_ack=True)
        print('Email microservice: Consuming from queue:', e_queue_name)
        channel1.start_consuming()
        print('Email microservice: Consuming from queue:', OA_queue_name)
        channel2.start_consuming() # an implicit loop waiting to receive messages; 
        # print('Email microservice: Consuming from queue:', shipping_queue_name)
        # channel3.start_consuming() # an implicit loop waiting to receive messages; 
        #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

    except pika.exceptions.AMQPError as e:
        print(f"error microservice: Failed to connect: {e}") 

    except KeyboardInterrupt:
        print("error microservice: Program interrupted by user.")


def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nSending Email......")
    print("==============================")
    print(body)
    print("==============================")
    # sendEmail(json.loads(body))
    print()

def callback2(channel, method, properties, body): # required signature for the callback; no return
    print("\nSending Email......from service update")
    sendOfferAlternative(json.loads(body))
    print()

def callback3(channel, method, properties, body):
    print("\nSending Email...... from shipping queue")
    # sendShippingUpdates(json.loads(body))
    print()


def sendEmail(body):
    print(body)
    message = ""
    request_Id = body.get("request_Id", "")

    #message templates
    valid_warranty_message = f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}) and it is valid. Do send out your graphic card to the following address:
    <br>
    <br>
    Block 11 One Street #11-11
    <br>
    Singapore S(111111)
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""

    invalid_warranty_message = f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}) and it is invalid. Do ensure that you have keyed in the correct details and registered the warranty
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""

    expired_warranty_message = f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}). We are sorry to inform you that your warranty has expired.
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""

    damage_not_covered = f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}). We are sorry to inform you that the damages are not covered by the warranty.
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""

    repaired = f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}). We are happy to inform you that your graphic card has been fixed and we will be sending it back to you shortly.
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""


    not_repairable_one_to_one_replacement = f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}). Unfortunately the graphic card is not repairable. However we do have a one to one replacement available, and will be sending that to you instead.
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""

    
    pending_alternative_refund= f"""<html>
    Hello,<br><br>
    We have received your warranty request (ref ID: {request_Id}). Unfortunately the graphic card is not repairable and we do not have any in stock at the moment for a one to one exchange. We will send out a replacement immediately once we have stocks else we will process a refund within the next 7 days. Thank you for your kind understanding.
    <br>
    <br>
    Regards,
    <br>
    KuihDaDar
    </html>"""

    if body['status'] == "invalid_serial_no":
        message = invalid_warranty_message.format(request_Id=request_Id)
    elif body['status'] == "valid":
        message = valid_warranty_message.format(request_Id=request_Id)
    elif body['status'] == "expired":
        message = expired_warranty_message.format(request_Id=request_Id)
    elif body['status'] == "damage_not_covered":
        message = damage_not_covered.format(request_Id=request_Id)
    elif body['status'] == "repaired":
        message = repaired.format(request_Id=request_Id)
    elif body['status'] == "not_repairable_one_to_one_replacement":
        message = not_repairable_one_to_one_replacement.format(request_Id=request_Id)
    elif body['status'] == "pending_alternative_refund":
        message = pending_alternative_refund.format(request_Id=request_Id)
    


    if message !="":
        response = client.emails.send(
        From=from_email,
        To=body.get("email",""),
        Subject=subject,
        HtmlBody=message
    )
    # Check if the email was sent successfully
        if response["ErrorCode"] == 0:
            print("Email sent successfully!")
        else:
            print(f"Failed to send email. Error: {response.Message}")  

def sendShippingUpdates(info):
    print(info)
    message = ""
    ProductName = body.get("ProductName", "")
    CaseNumber = body.get("CaseNumber", "")
    SerialNumber = body.get("SerialNumber", "")

    returned_original_message=f"""<html>
    Hello,<br><br>
    We have resolved your issue and shipped back your {ProductName} to you.<br><br>
    Case Number:{CaseNumber}<br><br>
    Serial Number: {SerialNumber}
    <br><br>
    Do feel free to reach out if you encounter any issues!<br><br>
    Regards,<br>
    KuihDaDar
    </html>"""

    replace_same_message=f"""<html>
    Hello,<br><br>
    We have shipped you a new {ProductName}.<br><br>
    Case Number:{CaseNumber}<br><br>
    Serial Number: {SerialNumber}
    <br><br>
    Do feel free to reach out if you encounter any issues!<br><br>
    Regards,<br>
    KuihDaDar
    </html>"""


    replace_same_message=f"""<html>
    Hello,<br><br>
    We have shipped you a new {ProductName}.<br><br>
    Case Number:{CaseNumber}<br><br>
    Serial Number: {SerialNumber}
    <br><br>
    Do feel free to reach out if you encounter any issues!<br><br>
    Regards,<br>
    KuihDaDar
    </html>"""

    replace_alternative_message=f"""<html>
    Hello,<br><br>
    We have shipped you a new {ProductName}.<br><br>
    Case Number:{CaseNumber}<br><br>
    Serial Number: {SerialNumber}
    <br><br>
    Do feel free to reach out if you encounter any issues!<br><br>
    Regards,<br>
    KuihDaDar
    </html>"""

    if info['Remarks']== "returned originial":
        message =returned_original_message.format(ProductName=ProductName,CaseNumber=CaseNumber,SerialNumber=SerialNumber)
    elif info['Remarks']== "replace same":
        message =replace_same_message.format(ProductName=ProductName,CaseNumber=CaseNumber,SerialNumber=SerialNumber)
    elif info['Remarks']== "replace alternative":
        message =replace_alternative_message.format(ProductName=ProductName,CaseNumber=CaseNumber,SerialNumber=SerialNumber)

    response = client.emails.send(
    From=from_email,
    To=info.get('recipient',""),
    Subject=info.get('subject',""),
    HtmlBody=message
)
        # Check if the email was sent successfully
    if response["ErrorCode"] == 0:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Error: {response.Message}")  

def sendOfferAlternative(info):
    message = ""
    request_Id = body.get("request_Id", "")
    model_Id = body.get("model_Id","")
    offer_alternative=f"""<html>
    Hello,<br><br>
    We sorry to inform you that we are unable to repair your graphic card (Ref ID:{request_Id}). However we do have an alternative on hand, {model_Id} would you like that instead?<br><br>
    <br><br>
    Do feel free to reach out if you encounter any issues!<br><br>
    Regards,<br>
    KuihDaDar
    </html>"""
    print(info)
    message = offer_alternative
    response = client.emails.send(
    From=from_email,
    To=body.get("email",""),
    Subject=subject,
    HtmlBody=message
)
    # Check if the email was sent successfully
    if response["ErrorCode"] == 0:
        print("Email sent successfully!")
    else:
        print(f"Failed to send email. Error: {response.Message}")  


if __name__ == "__main__": # execute this program only if it is run as a script (not by 'import')    
    print("email microservice: Getting Connection")
    connection = amqp_connection.create_connection() #get the connection to the broker
    print("email microservice: Connection established successfully")
    channel1 = connection.channel()
    channel2 = connection.channel()
    channel3 = connection.channel()
    queues(channel1,channel2,channel3)

