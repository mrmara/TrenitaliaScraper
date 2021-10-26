# importing all required libraries
import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
class bot():
    def __init__(self,id):
        # get your api_id, api_hash, token
        # from telegram as described above
        self.api_id = ''
        self.api_hash = ''
        self.message = "Working..."

        # your phone number
        self.phone = '00393464768609'

        # creating a telegram session and assigning
        # it to a variable client
        self.client = TelegramClient(id, self.api_id, self.api_hash)

        # connecting and building the session
        self.client.connect()

        # in case of script ran first time it will
        # ask either to input token or otp sent to
        # number or sent or your telegram id
        if not self.client.is_user_authorized():

            self.client.send_code_request(self.phone)
            
            # signing in the client
            self.client.sign_in(self.phone, input('Enter the code: '))

    def send(self, mess):
        try:
            # receiver user_id and access_hash, use
            # my user_id and access_hash for reference
            #self.client.send_message("+",mess)
            #self.client.send_message("+",mess)
            self.client.send_message("+",mess)
        except Exception as e:           
            # there may be many error coming in while like peer
            # error, wrong access_hash, flood_error, etc
            print(e)

        # disconnecting the telegram session
        #client.disconnect()
