from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
from ..database import get_db
from ..models import User, Conversation, Message
from ..schemas.chat import (
    Conversation as ConversationSchema,
    ConversationWithDetails,
    ConversationCreate,
    Message as MessageSchema,
    MessageCreate
)
from ..core.dependencies import get_current_active_user

router = APIRouter(prefix="/chats", tags=["Chats"])


@router.get("/", response_model=List[ConversationWithDetails])
def get_conversations(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for the current user"""
    conversations = db.query(Conversation).filter(
        or_(
            Conversation.participant1_id == current_user.id,
            Conversation.participant2_id == current_user.id
        )
    ).order_by(Conversation.updated_at.desc()).all()

    return conversations


@router.post("/", response_model=ConversationSchema)
def create_or_get_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new conversation or get existing one with a friend"""
    friend_id = conversation_data.friend_id

    # Check if friend exists
    friend = db.query(User).filter(User.id == friend_id).first()
    if not friend:
        raise HTTPException(status_code=404, detail="User not found")

    if friend_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot create conversation with yourself")

    # Check if conversation already exists
    existing_conversation = db.query(Conversation).filter(
        or_(
            and_(
                Conversation.participant1_id == current_user.id,
                Conversation.participant2_id == friend_id
            ),
            and_(
                Conversation.participant1_id == friend_id,
                Conversation.participant2_id == current_user.id
            )
        )
    ).first()

    if existing_conversation:
        return existing_conversation

    # Create new conversation
    new_conversation = Conversation(
        participant1_id=current_user.id,
        participant2_id=friend_id
    )
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)

    return new_conversation


@router.get("/{conversation_id}/messages", response_model=List[MessageSchema])
def get_messages(
    conversation_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all messages in a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if user is participant
    if conversation.participant1_id != current_user.id and conversation.participant2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this conversation")

    messages = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.sent_at).all()

    # Mark messages as read (messages sent by the other user)
    for message in messages:
        if message.sender_id != current_user.id and not message.is_read:
            message.is_read = True
    db.commit()

    return messages


@router.post("/{conversation_id}/messages", response_model=MessageSchema)
def send_message(
    conversation_id: int,
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Send a message in a conversation"""
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Check if user is participant
    if conversation.participant1_id != current_user.id and conversation.participant2_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to send messages in this conversation")

    # Create message
    new_message = Message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        content=message_data.content
    )
    db.add(new_message)

    # Update conversation updated_at
    from sqlalchemy import func
    conversation.updated_at = func.now()

    db.commit()
    db.refresh(new_message)

    return new_message
