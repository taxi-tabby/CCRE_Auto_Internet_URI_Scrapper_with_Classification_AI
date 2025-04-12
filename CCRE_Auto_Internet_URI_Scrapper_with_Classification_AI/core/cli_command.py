from typing import List, Union

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models.roots import Roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection

class CLICommand:
    def __init__(self, roots: List['Roots'], mq_sessions: List['PikaRabbitMQ'], db_session: 'SQLAlchemyConnection'):
        self.roots = roots
        self.mq_sessions = mq_sessions
        self.db_session = db_session

    def empty(self):
        return
