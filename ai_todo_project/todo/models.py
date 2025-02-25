from django.db import models
from django.contrib.auth.models import User
import uuid
from typing import List
from pydantic import BaseModel, Field


class TodoItem(models.Model):
    # In models.py
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todo_items')  # Remove the null=True
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    steps = models.JSONField(default=list)
    completed = models.BooleanField(default=False)
    

class AITodoItemSteps(BaseModel):
    steps: List[str] = Field([], description="The steps that the user should take to complete the ToDo item")
    
