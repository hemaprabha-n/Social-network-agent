from topic_manager import TopicManager
from fastapi import APIRouter, HTTPException
import os
import random

router = APIRouter()
topic_manager = TopicManager()

TEXT_FILE = "company_text.txt"

MAX_CHARS = 3000


@router.get("/company-text")
def company_text():

    if not os.path.exists(TEXT_FILE):
        raise HTTPException(
            status_code=404,
            detail="company_text.txt not found."
        )

    with open(TEXT_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    if len(text) <= MAX_CHARS:
        return {
            "company_text": text
        }

    max_start = len(text) - MAX_CHARS
    start = random.randint(0, max_start)

    chunk = text[start:start + MAX_CHARS]

    return {
        "company_text": chunk
    }


@router.get("/next-topic")
def next_topic():

    topic = topic_manager.get_next_topic()

    return {
        "topic": topic
    }
