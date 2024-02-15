#!/usr/bin/env python3
"""Auth class's models"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """session exp auth class"""
    def __init__(self):
        """init session exp auth"""
        if os.environ.get('SESSION_DURATION') is None:
            s = 0
        else:
            try:
                s = int(os.environ.get('SESSION_DURATION'))
            except ValueError:
                s = 0
        self.session_duration = s

    def create_session(self, user_id=None):
        """create session with session exp auth"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""

        if self.session_duration <= 0:
            return u_i_b_s_i.get('user_id')
