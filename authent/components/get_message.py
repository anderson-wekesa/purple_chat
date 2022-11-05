from django_unicorn.components import UnicornView
from django.utils.timezone import now
from django.http import HttpResponse
from authent.models import Message


class GetMessageView(UnicornView):
    template_name = "unicorn/get-message.html"
    messages: Message = None
    message: str = ""
    
    def mount(self):
        self.messages = Message.objects.all()
        return super().mount()

    def save_message(self):
        # if self.message is not None:
        #     return HttpResponse(self.message)
        Message.objects.create(user=self.request.user, content=self.message)

        #reset
        self.message = ""
        self.messages = Message.objects.all()

    def refresh_chats(self):
        self.messages = Message.objects.all()
        #self.message = self.message
        #return self.messages


#Refreshes the chats div every two second to display new messages
class PollingView(UnicornView):
    current_time = now()
    messages: Message = None
    template_name = "unicorn/get-message.html"

    def refresh_chats(self):
        self.messages = Message.objects.all()
        self.message = self.message
        