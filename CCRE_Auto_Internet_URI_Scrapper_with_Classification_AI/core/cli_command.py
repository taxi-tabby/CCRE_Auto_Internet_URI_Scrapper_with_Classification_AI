from typing import List, Union

from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.console import CommandHandler
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.db.models.roots import Roots
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.pika_rabbitmq import PikaRabbitMQ
from CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.schema.implement.sqlalchemy import SQLAlchemyConnection
import platform
from datetime import datetime

import CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.rds as rds
import CCRE_Auto_Internet_URI_Scrapper_with_Classification_AI.core.local as local_rds

class CLICommand:
    def __init__(self, console_handler: CommandHandler, roots: List['Roots'], mq_sessions: List['PikaRabbitMQ'], db_session: 'SQLAlchemyConnection', local_session: 'SQLAlchemyConnection'):
        self.console_handler = console_handler
        self.roots = roots
        self.mq_sessions = mq_sessions
        self.db_session = db_session
        self.local_session = local_session
        
        # Constants for profile keys as dictionary
        self.PROFILE_KEYS = {
            'PARTY_ALIAS_NAME': 'party_alias_name'
        }

    def empty(self):
        """
        Not available command.
        """
        return
    
    
    def motd(self):
        """
        print welcome message of the day.
        """
        
        print = self.console_handler.print_formatted
        
        banner = """
        ╔════════════════════════════════════════════════════════╗
        ║                                                        ║
        ║   CCRE Auto Internet URI Scrapper with Classification  ║
        ║                                                        ║
        ╚════════════════════════════════════════════════════════╝
        """
        
        self.console_handler.print_formatted(banner)
        print()
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        print('[Profile]')
        with self.local_session.get_db() as db:
            (lambda r: print(f'alias name: {r}', 'info') if r is not None else None)(local_rds.get_latest_local_profile(db, self.PROFILE_KEYS['PARTY_ALIAS_NAME']))
    
    def party_alias_name_change(self, name: str):
        """
        Change the party alias name.
        """
        key = self.PROFILE_KEYS['PARTY_ALIAS_NAME']
        r: str = ''
        with self.local_session.get_db() as db:
            local_rds.save_local_profile(db, key, name)
            
            response = local_rds.get_latest_local_profile(db, key)
            if response is not None:
                r = response
                
        print(f"Party alias name changed to: {r}") 
            
