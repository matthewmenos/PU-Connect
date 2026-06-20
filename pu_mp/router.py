"""
PU-Connect Database Router

global.db  (default)  — shared/public data
  - Auth:         auth, contenttypes, sessions, admin, sites
  - Listings:     Listings_app
  - Profiles:     Profile_app
  - Search:       search_app
  - Dashboard:    dash_app
  - Base:         Base_app
  - Auth app:     Auth_app
  - Reels:        Reels_app

user.db    (user_db)  — private/user data
  - Messaging:    chat_app  (Conversation, Message, PushSubscription, Notification)
"""

USER_DB_APPS = {'chat_app'}

GLOBAL_DB_APPS = {
    'auth', 'contenttypes', 'sessions', 'admin', 'sites',
    'Listings_app', 'Profile_app', 'search_app', 'dash_app',
    'Base_app', 'Auth_app', 'Reels_app', 'allauth',
    'account', 'socialaccount',
}


class PURouter:

    def db_for_read(self, model, **hints):
        if model._meta.app_label in USER_DB_APPS:
            return 'user_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in USER_DB_APPS:
            return 'user_db'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations within the same database
        db1 = 'user_db' if obj1._meta.app_label in USER_DB_APPS else 'default'
        db2 = 'user_db' if obj2._meta.app_label in USER_DB_APPS else 'default'
        return db1 == db2

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in USER_DB_APPS:
            return db == 'user_db'
        return db == 'default'
