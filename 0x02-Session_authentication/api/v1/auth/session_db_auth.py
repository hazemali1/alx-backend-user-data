#!/usr/bin/env python3
"""Auth class's models"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """session db auth class"""
    def create_session(self, user_id=None):
        """create session with session db auth"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        obj = UserSession()
        obj.user_id = user_id
        obj.session_id = session_id
        obj.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id for session id"""
        print("================================")
        if session_id is None:
            return None
        obj = UserSession()
        li = obj.search({'session_id': session_id})
        if len(li) == 0:
            return None
        s = li[0]
        c_a = s.get('created_at')
        if c_a is None:
            return None
        c_a = datetime.fromisoformat(c_a)
        t = (datetime.now() - c_a).total_seconds()
        if int(t) > self.session_duration:
            return None
        return s.get('user_id')

    def destroy_session(self, request=None):
        """destroy session from db"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        obj = UserSession()
        obj = obj.search({'session_id': session_id})[0]
        obj.remove()
        return True
