from django.shortcuts import render
import markdown2

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    content = util.get_entry(entry)

    if content == None:
        return render(request, "encyclopedia/error.html", {
            "title": entry
        })
    html = markdown2.markdown(content)
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": html
    })