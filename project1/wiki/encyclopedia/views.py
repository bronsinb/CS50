from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random

from . import util

class AddEditForm(forms.Form):
    title = forms.CharField()
    entry = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': "Type Entry Here"}))

def index(request):
    if request.GET:
        query = request.GET["q"]
        return entry(request, query)
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })

def entry(request, entry):
    content = util.get_entry(entry)

    if content == None:
        return render(request, "encyclopedia/error.html", {
            "error": f"'{entry}' Not Found"
        })
    html = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": html
    })

def rand(request):
    title = random.choice(util.list_entries())
    content = util.get_entry(title)
    html = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": html
    })

def add(request):
    if request.method == "POST":
        form = AddEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if util.get_entry(title) is not None:
                return render(request, "encyclopedia/error.html", {
                    "error": f"'{title}' Already Exists"
                })
            content = form.cleaned_data["entry"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/addedit.html", {
                "type": "Edit",
                "form": form
            })
    else:
        return render(request, "encyclopedia/addedit.html", {
            "type": "Add",
            "form": AddEditForm()
        })

def edit(request):
    if request.method == "POST":
        form = AddEditForm(request.POST)
        print(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", args=[title]))
        else:
            return render(request, "encyclopedia/addedit.html", {
                "type": "Edit",
                "form": form
            })
    else:
        title = request.GET["edit"]
        content = util.get_entry(title)

        form = AddEditForm()
        form.fields["title"].widget.attrs['style'] = 'display:none;'
        form.fields["title"].label = ""
        form.fields["title"].initial = title
        form.fields["entry"].initial = content

        return render(request, "encyclopedia/addedit.html", {
            "type": f"Edit {title}",
            "form": form
        })