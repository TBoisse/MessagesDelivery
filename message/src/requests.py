from pydantic import BaseModel

class CreateChatRequest(BaseModel):
    chat_name : str
    description : str = ""
    icon : str = ""

class DeleteChatRequest(BaseModel):
    chat_id : str
    
class CreateMessageRequest(BaseModel):
    chat_id : str
    content : str
    
class AddChatMemberRequest(BaseModel):
    chat_id : str
    contact_phone : str