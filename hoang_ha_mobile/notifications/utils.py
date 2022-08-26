from hoang_ha_mobile.base.services.notifications.firebase import get_device_user, send_message_to


def push_notification_order(user_id, title, body):
    mess_data = {
        "title": title,
        "body": body
    }
    device = get_device_user(user_id)

    send_message_to(None, device, mess_data)
    
    