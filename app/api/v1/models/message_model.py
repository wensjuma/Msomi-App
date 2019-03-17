from datetime import datetime
message = []

class Message(object):

    """class to handle sending of Direct Messages"""

    def __init__(self):
        self.message = message
    

    def create_message(self, data):
        message = {
            'message_id': len(self.message) + 1,
            'message_body':data['body'],
            'message_sender': data['sender'],
            'message_recipient':data['recipient'],
            'message_timestamp':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message_chatid': '4'
        }

        self.message.append(message)

        return message
    
    def fetch_messages(self):
        return self.message