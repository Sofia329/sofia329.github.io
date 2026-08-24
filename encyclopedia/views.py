from django.shortcuts import render, redirect

from . import util

from django.urls import reverse

import random


from markdown2 import Markdown
markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):

    if util.get_entry(title) is None:
        return render (request, "encyclopedia/title.html",{
            "title_name": None
        })
    else:
        content = markdowner.convert(util.get_entry(title))

        return render(request, "encyclopedia/title.html", {
            "title_name": title,
            "content": content
        })

def search(request):
    q = request.POST.get("q")
    if util.get_entry(q):
        return title(request, title=q)
    else:
        return render(request, "encyclopedia/search.html", {
            # list comprehension to pass search.html a list of entires that is the query as a substring
            "entries": [entry for entry in util.list_entries() if q in entry]
        })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "existence": False
        })
    else:
        title_name=request.POST.get("title").strip()
        content=request.POST.get("content").strip()

        # pass back title & content to new.html to validate if user's input

        if not title_name or title_name in util.list_entries():
            return render(request, "encyclopedia/new.html",{
                "existence": True,
                "title_name": title_name,
                "content": content,

            })
        # if title not exists, then save the entry, and return the entry page
        else:
            util.save_entry(title_name, content)
            return title(request, title=title_name)

def edit(request, title_name):
    if request.method=="GET":
        content = util.get_entry(title_name)
        return render(request, "encyclopedia/edit.html", {
            "content": content,
            "title_name": title_name
    })

    else:
        content=request.POST.get("content")
        util.save_entry(title_name, content)
        return title(request, title_name)

def random_page(request):
    entries = util.list_entries()
    entry = random.choice(entries)
    return redirect("wiki:title", entry)





