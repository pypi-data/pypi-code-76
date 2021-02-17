from serpentmonkee import SecretMonkee

from neo4j import GraphDatabase, basic_auth  # , ServiceUnavailable
from neo4j.exceptions import ServiceUnavailable
import firebase_admin
from firebase_admin import credentials, firestore
import logging
from google.cloud import secretmanager
import os
import time
from datetime import datetime, timedelta, timezone
import json
from google.cloud.firestore_v1.transforms import DELETE_FIELD
from serpentmonkee import SecretMonkee, NeoMonkee
import sqlalchemy
import pg8000
import UtilsMonkee as um
import redis
from google.cloud import pubsub_v1
from NeoDriver import NeoDriver
from NeoMonkee import NeoMonkee
from PubSubMonkee import PubSubMonkee

from CypherTransaction import CypherTransactionBlock, CypherTransactionBlockWorker
from CypherQueue import CypherQueue, CypherQueues


# pip3 install neo4j==4.1.1
# pip3 install neo4j==1.7.6

if __name__ == '__main__':

    project_id = "monkee-int"  # <-- THE LOCAL DEV ENVIRONMENT

    if project_id == "monkee-prod":
        credfp = "/Users/lwicverhoef/gcp_jsons/monkee-prod-firebase-adminsdk-xvdxy-95ddc9c905.json"
    elif project_id == "monkee-dev":
        credfp = "/Users/lwicverhoef/gcp_jsons/monkee-dev-firebase-adminsdk-qw55p-b132b8a850.json"
        sqldb = sqlalchemy.create_engine(
            "postgresql+pg8000://postgres:pingping@localhost:1234/postgres")
    elif project_id == "monkee-int":
        credfp = "/Users/lwicverhoef/gcp_jsons/monkee-int.json"
        sqldb = sqlalchemy.create_engine(
            "postgresql+pg8000://postgres:g3i92lfowE8c1ED7@localhost:1236/postgres"
        )

    cred = credentials.Certificate(credfp)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credfp

    secretclient = secretmanager.SecretManagerServiceClient()
    redis_client = redis.Redis()
    pubSubPublisher = pubsub_v1.PublisherClient()

    firebase_admin.initialize_app(
        cred,
        {
            "projectId": project_id,
        },
    )

    sm = SecretMonkee(secretclient, project_id, ['neo']).getSecrets()

    neo_driver = NeoDriver(
        neoDriver=None, redisClient=redis_client, sqlClient=sqldb, callingCF='neo_sync_interactionTemplates_v2', publisher=pubSubPublisher, topicId='cypher_worker', projectId=project_id)

    neo_driver.makeNeoDriver(
        sm["neo_uri"], sm["neo_user"], sm["neo_pass"])

    neomnkee = NeoMonkee(
        neoDriver=neo_driver.neoDriver,
        redisClient=redis_client,
        sqlClient=sqldb,
        callingCF='testingCF',
        publisher=pubSubPublisher,
        topicId='testingProj',
        projectId=project_id,
        sqlTable='monkee.neo4j_queries')

    neomnkee.makeNeoDriver(sm['neo_uri'], sm['neo_user'], sm['neo_pass'])

    def test_readWrite():
        query = """MATCH (h:humans {_project:$projectname})
        RETURN h.uid as uid, h.stepNumber as step limit 10
        """
        params = {'projectname': 'Sandbox'}
        res = neomnkee.syncRead(query=query,
                                params=params,
                                cfInstanceUid='1234')

        params = {'projectname': 'Sandbox', 'uid': '0000'}
        query = """MATCH (h:humans {uid:$uid, _project:$projectname})
        SET h.val1 = 'one'
        RETURN h.uid as uid, h.stepNumber as step
        """

        neomnkee.asyncWriteStatement(query=query,
                                     params=params,
                                     cfInstanceUid='1234')

        batch = [
            '01602cb23de544e8b33c4612810e96a5',
            '016a8a2f414c43b49b656b655da07fbe',
            '01f62dc44f6d4e85b0c2a7a973f97750'
        ]
        query = """
                    UNWIND $batch AS hB
                    MERGE (h:humans:test { uid: hB, _project: $projectname })
                    set h.val = 314159
                    return h.uid as uid
                    """

        params = {'projectname': 'Sandbox'}
        neomnkee.asyncWriteStatement(query=query,
                                     params=params,
                                     batch=batch,
                                     cfInstanceUid='1234')

        for r in res:
            print(r['uid'])

    redisClient = redis.Redis()
    cQH = CypherQueue("cypherQ_High")
    cQM = CypherQueue("cypherQ_Medium")
    cQL = CypherQueue("cypherQ_Low")
    wQ = CypherQueue("cypherWorking")
    compQ = CypherQueue("cypherDone")
    queues = [cQH, cQM, cQL]

    cqs = CypherQueues(redisClient=redisClient,
                       cQueues=queues, workingQ=wQ, completedQ=compQ)

    # cqs.killQueues()

    for i in range(0):
        statements = [
            {
                "cypher":
                """MERGE (c:interactionTemplates:test {uid: $contentUid, _project:$projectName})-[:TEST]->(t:tag:test {_project:$projectName, uid:"t1"})<-[:TEST2]-(h:humans:test {_project:$projectName, uid:"AAA"})
            RETURN id(c)""",
                "parameters": {
                    "contentUid": um.get_uuid(),
                    "projectName": "testing"
                }
            },
            {
                "cypher":
                """MERGE (c:interactionTemplates:test {uid: $contentUid, _project:$projectName})-[:TEST]->(t:tag:test {_project:$projectName, uid:"t2"})<-[:TEST2]-(h:humans:test {_project:$projectName, uid:"AAA"})
            RETURN id(c)""",
                "parameters": {
                    "contentUid": um.get_uuid(),
                    "projectName": "testing"
                }
            },
        ]
        ctb = CypherTransactionBlock(priority='M',
                                     statements=statements,
                                     transactionUid=um.get_uuid(),
                                     origin='TEST',
                                     appUid='testApp',
                                     originDocUid='sflkjdf',
                                     sqlClient=sqldb,
                                     callingCF='testcf')

        cqs.pushCtbToWaitingQ(ctb)

    cqs.getQLens()

    topicId = 'cypher_worker'
    pubsub = PubSubMonkee(pubSubPublisher, project_id, topicId)
    w = CypherTransactionBlockWorker(
        neoDriver=neomnkee.neoDriver, cypherQueues=cqs, sqlClient=sqldb, pubsub=pubsub)

    w.goToWork(forHowLong=100)
    cqs.getQLens()
