# -*- coding: utf-8 -*-
from __future__ import print_function
from botocore.vendored import requests
import googlemaps
from os import environ
from datetime import datetime

import random
import logging

from ask_sdk_core.utils import is_intent_name, get_slot_value
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
                                              AbstractRequestHandler, AbstractExceptionHandler,
                                              AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Start_intent(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input))
    
    def handle(self, handler_input):
        speech_output = "Welcome to the raspberri pi hub. You can ask me things like What's my daily rundown or set my Alarm to 9 am"
        handler_input.response_builder.speak(speech_output).ask(
                                                                HELP_REPROMPT).set_card(SimpleCard(
                                                                                                   SKILL_NAME, speech_output))
        return handler_input.response_builder.response
class CommuteToWork(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("CommuteToWork")(handler_input))
    
    def handle(self, handler_input):
        start_address, start_postcode = get_my_address()
        if not start_address:
            return permissions_error()
        destination = get_work_address()
        print('start: '+start_address+'; destination: '+destination + 'post' + start_postcode)
        speech_output, duration, summary = get_duration(start_postcode, destination, start_address)
        duration_summ = duration + ", " + summary
        handler_input.response_builder.set_should_end_session(True)
        handler_input.response_builder.speak(speech_output).set_card(SimpleCard(
                                                                                "Commute", duration_summ))
    return handler_input.response_builder.response
class AlarmSet(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AlarmSet")(handler_input))
    def handle(self, handler_input):
        time = get_slot_value(handler_input=handler_input, slot_name="time")
        print(time)
        speech_output = "Ok, setting alarm to " + time
        out = "Alarm On"
        handler_input.response_builder.set_should_end_session(True)
        handler_input.response_builder.speak(speech_output).set_card(SimpleCard(
                                                                                out, time))
        return handler_input.response_builder.response
class CancelAlarm(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("CancelAlarm")(handler_input))
    def handle(self, handler_input):
        speech_output = "Ok, removing alarm"
        out = "Alarm Off"
        handler_input.response_builder.set_should_end_session(True)
        handler_input.response_builder.speak(speech_output).set_card(SimpleCard(
                                                                                out, speech_output))
        return handler_input.response_builder.response
def get_my_address():
    return environ['HOME'], environ['HOME']

def get_work_address():
    return environ['WORK']

def get_duration(start_postcode, end, start_address):
    gmaps = googlemaps.Client(key=environ['API_KEY'])
    try:
        directions_result = gmaps.directions(start_postcode, end, departure_time=datetime.now())
    except:
        directions_result = []
    if len(directions_result) == 0:
        try:
            directions_result = gmaps.directions(start_postcode+', '+environ['COUNTRY'], end+', '+environ['COUNTRY'], departure_time=datetime.now())
        except:
            directions_result = []
        if len(directions_result) == 0:
            return ask_for_repeat(end)
    leg = directions_result[0]['legs'][0]
    duration=leg['duration_in_traffic']['text']
    summary = directions_result[0]['summary']
    to_say="Right now, it takes "+duration+" to get from home to work, via " +summary
    return to_say, duration, summary



class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)
    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")
        
        handler_input.response_builder.speak("What can I help you with?").ask(
                                                                              HELP_REPROMPT).set_card(SimpleCard(
                                                                                                                 SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")
        
        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
        
        AMAZON.FallbackIntent is only available in en-US locale.
        This handler will not be triggered except in that locale,
        so it is safe to deploy on any locale.
        """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        
        handler_input.response_builder.speak("Sorry I can't help you with that").ask(
                                                                                     FALLBACK_REPROMPT)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)
    
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")
        
        logger.info("Session ended reason: {}".format(
                                                      handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
        respond with custom message.
        """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True
    
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)
        
        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
                                                                    HELP_REPROMPT)
                                                                    
        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
                                                handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Register intent handlers
sb.add_request_handler(CommuteToWork())
sb.add_request_handler(CancelAlarm())
sb.add_request_handler(AlarmSet())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())



# Register exception handlers
sb.add_exception_handler(CatchAllExceptionHandler())

# Handler name that is used on AWS lambda
lambda_handler = sb.lambda_handler()

