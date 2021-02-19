# beepbeep.ps: google pubsub functions
from typing import Optional, Union, Dict, Any
import os
import base64
from google.cloud import pubsub_v1


def publish_message_to_pubsub_topic(topic_name:str, attributes_dict: dict) -> dict:
    """
    Publishes messages to a Pub/Sub topic.

    Parameters:
        topic_name (str) : Your topic ID.
        attributes_dict (dict) : Pipeline config attributes as metadata in Pub/Sub
    
    Returns:
        If successful:
            status (string): "success" for successful pubsub message posted to topic path.
        If error:
            message (string): Exception or error message if applicable.
    """
    try:
        project_id = os.environ.get('GCP_PROJECT')
        PS = pubsub_v1.PublisherClient()
        topic_path = f"projects/{project_id}/topics/{topic_name}"
        
        PS.publish(topic_path, b'pipeline_config in attributes', **attributes_dict)
        
        message_status: dict = {"status": "success", "message": f"pubsub message posted to {topic_path}"}

    except Exception as e:
        message_status = {"status": "fail", "message": e}
    
    return message_status


def publish_message_to_pubsub_topic_with_text_payload(topic_name:str, text_payload: str) -> dict:
    """
    Publishes messages to a Pub/Sub topic with text payload.

    Parameters:
        topic_name (str) : Your topic ID.
        text_payload (str) : Text Payload
    
    Returns:
        If successful:
            status (string): "success" for successful pubsub message posted to topic path.
        If error:
            message (string): Exception or error message if applicable.
    """

    try:
        project_id = os.environ.get('GCP_PROJECT')
        PS = pubsub_v1.PublisherClient()
        topic_path = f"projects/{project_id}/topics/{topic_name}"
        
        text_payload_encoded = base64.b64encode(text_payload.encode("utf-8"))

        PS.publish(topic_path, text_payload_encoded)
        
        message_status: dict = {"status": "success", "message": f"pubsub message posted to {topic_path}"}

    except Exception as e:
        message_status = {"status": "fail", "message": e}
    
    return message_status


def build_pubsub_event_payload(text_payload: str, attribute_dict: dict = None) -> dict:
    """
    Build a Pub/Sub event payload.

    Parameters:
        text_payload (str) : Text Payload
        attributes_dict (dict) : Attributes as metadata to build a Pub/Sub event payload.
    
    Returns:
        If successful:
            Returns the event payload
        If error:
            Returns a empty object
    """

    try:
        # base64 encode text payload
        text_payload_encoded: bytes = base64.b64encode(text_payload.encode("utf-8"))

        # construct event dict
        event = {}
        event['data'] = text_payload_encoded
        event['attributes'] = attribute_dict
    
    except Exception as e:
        event = {}

    return event


def get_test_event_payload() -> dict:
    """
    This function returns a testing event payload.

    
    Returns:
        Returns Default Dummy Data.
    """

    # construct event dict with default dummy data
    test_payload = build_pubsub_event_payload("payload in attributes", {"key": "test_value"})
    return test_payload

