from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
import uuid
from .models import TodoItem, AITodoItemSteps
from .forms import TodoItenForm
import ollama

# Create your views here.
@login_required(login_url='login')
def index(request):
    todo_items = TodoItem.objects.all()
    return render(request, 'todo/index.html', {'todo_items': todo_items})

@login_required
def add_todo(request):
    if request.method == 'GET':
        form = TodoItenForm()
        return render(request, 'todo/add_todo.html', {'form': form})
    elif request.method == 'POST':
        form = TodoItenForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            
            ai_todo_item_steps = AITodoItemSteps(steps=[])
            
            example_todo_item_steps = AITodoItemSteps(steps=[
                'Step 1',
                'Step 2',
                'Step 3',
                'Step 4',
                'Step 5',
                'Step 6',
            ])
            
            ai_prompt = f"""Return ONLY a JSON object with no additional text. The JSON must contain steps for this task:

            Title: {title}
            Description: {description}

            Required JSON structure:
            {{
                "steps": [
                    "Step 1: actual step here",
                    "Step 2: actual step here",
                    "Step 3: actual step here",
                    "Step 4: actual step here",
                    "Step 5: actual step here",
                    "Step 6: actual step here",
                    "Step 7: actual step here"
                ]
            }}

            CRITICAL RULES:
            - Output MUST be valid JSON only
            - NO text before or after the JSON
            - IF THE OUTPUT IS NOT SCRICTLY IN JSON FORMAT YOU WILL BE TERMINATED
            - NO explanation or commentary
            - NO markdown formatting
            - Each step MUST be a string starting with "Step X: "
            - Steps MUST be real, detailed instructions
            - ONLY output the JSON object

            Example of EXACT output format:
            {{
                "steps": [
                    "Step 1: Install required dependencies",
                    "Step 2: Configure project settings",
                    "Step 3: Implement core functionality"
                ]
            }}

            Failure to follow these rules exactly will result in an error."""
                
            print(ai_prompt)
            
            response = ollama.chat(model="llama2", messages=[
                {"role": "user", "content": ai_prompt}
            ])
            
            content = response["message"]["content"]
            
            print(content)
            
            ai_todo_item_steps = AITodoItemSteps.model_validate_json(content)
            
            TodoItem.objects.create(
                id=uuid.uuid4(), 
                title=title, 
                description=description,
                steps=[step for step in ai_todo_item_steps.steps],
                user=request.user  # Add the current user here
            )
        return redirect('index')

@login_required
def complete_todo(request, todo_id):
    todo_item = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo_item.completed = True
    todo_item.save()
    return redirect('index')

@login_required
def delete_todo(request, todo_id):
    todo_item = get_object_or_404(TodoItem, id=todo_id, user=request.user)
    todo_item.delete()
    return redirect('index')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'todo/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'todo/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')