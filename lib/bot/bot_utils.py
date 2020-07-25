from bot.models import TelegramMessage


def save_telegram_message(received_json_data):

    try:
        telegram_msg = TelegramMessage(
            update_id=received_json_data["update_id"], json_msg=received_json_data
        )
        telegram_msg.save()
        return telegram_msg.id
    except Exception as e:
        print("Failed to save telegram message: " + str(e))
        return -1
