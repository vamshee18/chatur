from django.shortcuts import render, redirect
from .models import Prompt
from .forms import PromptForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login

def home(request):
    search = request.GET.get('search', '')
    category = request.GET.get('category', '')
    tag = request.GET.get('tag', '')

    prompts = Prompt.objects.all().order_by('-created_at')

    if search:
        prompts = prompts.filter(Q(title__icontains=search) | Q(prompt_text__icontains=search))
    if category:
        prompts = prompts.filter(category=category)
    if tag:
        prompts = prompts.filter(tags__icontains=tag)

    paginator = Paginator(prompts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Process tags for each prompt
    for prompt in page_obj:
        if prompt.tags:
            prompt.tag_list = [t.strip() for t in prompt.tags.split(',')]
        else:
            prompt.tag_list = []

    # Collect all unique tags
    all_tags = set()
    for p in Prompt.objects.all():
        if p.tags:
            all_tags.update([t.strip() for t in p.tags.split(',')])

    return render(request, 'prompts/index.html', {
        'page_obj': page_obj,
        'search': search,
        'category': category,
        'tag': tag,
        'all_tags': sorted(all_tags)
    })


def submit_prompt(request):
    if request.method == 'POST':
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.user = request.user if request.user.is_authenticated else None
            prompt.save()
            return redirect('home')
    else:
        form = PromptForm()
    return render(request, 'prompts/submit.html', {'form': form})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect("login")
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log in the user right after signup
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, "auth/signup.html", {"form": form})


@login_required
def my_prompts(request):
    user_prompts = Prompt.objects.filter(user=request.user).order_by('-created_at')

    for prompt in user_prompts:
        prompt.tag_list = [t.strip() for t in prompt.tags.split(',')] if prompt.tags else []

    return render(request, "prompts/my_prompts.html", {
        "prompts": user_prompts
    })