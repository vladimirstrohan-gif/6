from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CandidateForm

def apply(request):
    if request.method == "POST":
        form = CandidateForm(request.POST)
        if form.is_valid():
            messages.success(request, "Дякуємо, вашу анкету прийнято!")
            return redirect("apply")
        else:
            return render(request, "pages/apply.html", {"form": form})

    form = CandidateForm()
    return render(request, "pages/apply.html", {"form": form})