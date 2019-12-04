from actstream import action


def add_log_entry(verb, session_user, obj, description=''):
    action_details = {
        'sender': session_user,
        'action_object': obj,
        'verb': verb,
        'description': description,
    }
    action.send(**action_details)
