import json
import boto3
from datetime import datetime
import logging


def sendSomeMessage():
    now = datetime.now()                                        
    date = "%m/%d/%Y"                                           
    time = "%H:%M"                                          
    current_time = now.strftime(date+" "+time)
    message = "This message was sent: " + current_time
    logger = logging.getLogger() #.setLevel(log_level)
        
    
    logger.warn("this is a log line inside the sendSomeMessage meth")
    #logging.info("this is a log line inside the sendSomeMessage meth")
    

    sqs = boto3.client('sqs')

    sqs.send_message(
        QueueUrl="https://sqs.us-east-1.amazonaws.com/537309256512/BankQueueFinal",
        MessageBody=current_time
    )

    return message
