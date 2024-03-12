from opentelemetry.instrumentation.boto3sqs import Boto3SQSInstrumentor
from opentelemetry import trace

import logging
import time


def dt_log(self, record):
    if (not self.disabled) and self.filter(record):
        ctx = trace.get_current_span().get_span_context()
        if ctx.is_valid:
            trace_id = "{0:032X}".format(ctx.trace_id)
            span_id = "{0:016X}".format(ctx.span_id)
            record.msg = f"[!dt dt.trace_id={trace_id},dt.span_id={span_id}] - {record.msg}"
            
        self.callHandlers(record) 

logging.Logger.handle = dt_log

import sendmessage



Boto3SQSInstrumentor().instrument()

import json
import boto3
from datetime import datetime

# class DynatraceFormatter(logging.Formatter):
#     def formatMessage(self, record: logging.LogRecord) -> str:
#         message = super().formatMessage(record)
#         ctx = trace.get_current_span().get_span_context()
#         if not ctx.is_valid:
#             return message
#         trace_id = "{0:032X}".format(ctx.trace_id)
#         span_id = "{0:016X}".format(ctx.span_id)
#         print("Formatting {}", message)
#         return f"[!dt dt.trace_id={trace_id},dt.span_id={span_id}] - {message}"


def lambda_handler(event, context):
    #requestContext=event['requestContext']
    print("Event: "+str(event))
    #print("RequestTime: "+ str(event['requestContext']['requestTime']))

    t = time.time()
    ml = int(t * 1000)
    
    print("CurrentTime: "+ str(t))
    #print(event)
    print("Context: "+str(context))
    #print()
    # formatter = DynatraceFormatter()
    # for handler in logging.getLogger().handlers:
    #     handler.setFormatter(formatter)
    logger = logging.getLogger() #.setLevel(log_level)
        
    
    logger.warn("This is with the new format")

    message = sendmessage.sendSomeMessage()
    now = datetime.now()
    # print("Now: ")
    # print(now)
    # print("now.second%2: ")
    # print(now.second%2)
    statusCode = 200
    errorMessage = ""
    try:
        if ((now.second%2)==0):
            logger.warn("This is a log line inside a trace: All bad...")
            statusCode = 400
        else:
            if ((now.second%3)==0):
                logger.error("This is VERY VERY BAD...")
                statusCode = 500
                raise ValueError('Bad value'+str(statusCode))
    except Exception as e:
        errorMessage = "[Business Error] "+str(e)
        raise e
    

    return {
        'statusCode': statusCode,
        errorMessage: errorMessage,
        'body': json.dumps(message)
    } 
