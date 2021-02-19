import os
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import NewTopic

from mobio.libs.kafka_lib import KAFKA_BOOTSTRAP, MobioEnvironment


def create_kafka_topics(lst_topic):
    admin_client = AdminClient({"bootstrap.servers": KAFKA_BOOTSTRAP})
    existing_topics = list(admin_client.list_topics().topics.keys())
    new_topics = []
    for required_topic in lst_topic:
        if required_topic not in existing_topics:
            new_topics.append(
                NewTopic(
                    required_topic,
                    num_partitions=4,
                    replication_factor=int(os.getenv(MobioEnvironment.KAFKA_REPLICATION_FACTOR)),
                )
            )
        else:
            print("Topic {} existed".format(required_topic))

    if new_topics:
        fs = admin_client.create_topics(new_topics)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("New Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create new topic {}: {}".format(topic, e))


if __name__ == "__main__":
    create_kafka_topics([])
