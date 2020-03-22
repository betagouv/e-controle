from actstream import action


def add_log_entry(verb, session_user, obj, description='', target=None):
    action_details = {
        'sender': session_user,
        'action_object': obj,
        'verb': verb,
        'description': description,
        'target': target,
    }
    action.send(**action_details)
