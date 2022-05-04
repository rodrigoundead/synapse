# Synapse

#### Synapse help to do not repeat yourself

 You can display messages using redirect instead of render on Django only with Python
 If you have a view and only need to display a message, you can use Synapse message to set redirect instead of render, this avoid to set the values of all the objects of this view again.
 For example, if you have a list of itens and the user click in one of the items in this list, and see a page about this item, in this page the user is able to make a comment about this item. If he tries to comment and some error occurs you want to display an error msg to this user, to do that you need to render the view and set the values in all the objects
<p>
 
</p>

> **To import:**
```
 from synapse.message import set_message, get_message
```
<p>
</p>

> **In the view that has template.html**
>
>> if has a message from this view:
>>
```
    return render(request, "examples/example.html", {
                "message": get_message(request, "kind_of_msg", "msg_content")
    })
```
<p>
</p>

>> if this view do not has any message, but you want to render messages from another view:
>>
```
    return render(request, "examples/example.html", {
                "message": get_message(request)
    })
```
<p>
</p>

> **In the view to use redirect instead of render:**
>
```
    set_message(request, "kind_of_msg", "Message to display.")
    return HttpResponseRedirect(reverse("your_view", args=(object.id,)))
```
<p>
</p>

> **On template:**
>> this in the html to display a message:
>>
```
    {% if message.content %}
        <div class="{{ message.kind }}">
                {{ message.content }}
        </div>
    {% endif %}
```
>> kind_of_msg can be a bootstrap kind of message: danger, primary, warning, success, ...
>>
```
    {% if message.content %}
        <div class="alert alert-{{ message.kind }}" role="alert">
                {{ message.content }}
        </div>
    {% endif %}
```

<p>

</p>

---
<p>

</p>

**Generic Code Example:**

> With Synapse:

```
def remove_from_list(request, object_id):
        object = Object.objects.filter(pk=object_id).first()
        if object:
                list = request.user.list.filter().first()
                if list and list.have_this_object(object_id):
                        list.objects.remove(object)
                set_message(request, ("success" if not list.have_this_object(object_id) else ("danger")), ("Object removed from your WatchList!" if not list.have_this_object(object_id) else ("Can't remove this Object from your List"))
                return HttpResponseRedirect(reverse("show_object", args=(object.id,)))

        set_message(request, "danger", "Can't found this object.")
        return HttpResponseRedirect(reverse("index"))
```

> Without Synapse:

```
def remove_from_list(request, object_id):
        object = Object.objects.filter(pk=object_id).first()
        if object:
                list = request.user.list.filter().first()
                if list and list.have_this_object(object_id):
                        list.objects.remove(object)
                related_objects = object.related_objects.filter()
                return render(request, "objects/show_object.html", {
                        "object": object,
                        "related_objects": related_objects,
                        "some_flag": True if (object.some_behavior()) else (False),
                        "another_flag": True if (related_object.some_behavior()) else (False),
                        "kind_of_msg": "warning",
                        "message": "Object removed from your WatchList"
                })
        objects = Object.objects.filter(active=True)
        return render(request, "objects/index.html", {
                "objects": objects,
                "kind_of_msg": "danger",
                "message": "Can't found this object."
        })
```
<p>
</p>

___
<p>

</p>

**A Simplistic Code Example:**

<p>
This in the html file to use with bootstrap
</p>

> With Synapse:

```
    {% if message.content %}
        <div class="alert alert-{{ message.kind }}" role="alert">
                {{ message.content }}
        </div>
    {% endif %}
```

> Without Synapse:

```
    {% if message %}
        <div class="alert alert-{{ kind_of_msg }}" role="alert">
                {{ message }}
        </div>
    {% endif %}
```

<p>

This one has a template but do not has a message, the messages here come from another view
</p>

> With Synapse:

```
    def index(request):
            products = Product.objects.filter(active=True)
            watchlist = request.user.watchlist.filter().first() if (request.user.is_authenticated) else (None)
            return render(request, "products/index.html", {
                    "products": products,
                    "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                    "has_category": True if (Category.objects.all().first()) else (False),
                    "message": get_message(request)
            })
```

> Without Synapse:

```
    def index(request):
            products = Product.objects.filter(active=True)
            watchlist = request.user.watchlist.filter().first() if (request.user.is_authenticated) else (None)
            return render(request, "products/index.html", {
                    "products": products,
                    "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                    "has_category": True if (Category.objects.all().first()) else (False),
            })
```

<p>

This one has a template and render message on another template
</p>

> With Synapse:

```
@login_required
def new_product(request):
        watchlist = request.user.watchlist.filter().first()
        if request.method == "POST":
                form = NewProductForm(request.POST)
                if form.is_valid():
                        product = Product().new_populate(form.cleaned_data, request.user)
                        product.save()

                        set_message(request, "primary", "Product Created")
                        return HttpResponseRedirect(reverse("index"))
                else:
                        return render(request, "products/new_product.html", {
                                "form": form,
                                "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                                "has_category": True if (Category.objects.all().first()) else (False)
                        })
        return render(request, "products/new_product.html", {
                "form": NewProductForm(),
                "has_watchlist": True if (wachlist and watchlist.products.filter().first()) else (False),
                "has_category": True if (Category.objects.all().first()) else (False)
        })
```

> Without Synapse:

```
@login_required
def new_product(request):
        watchlist = request.user.watchlist.filter().first()
        if request.method == "POST":
                form = NewProductForm(request.POST)
                if form.is_valid():
                        product = Product().new_populate(form.cleaned_data, request.user)
                        product.save()
                        products = Product.objects.filter(active=True)
                        return render(request, "products/index.html", {
                                "products": products,
                                "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                                "has_category": True if (Category.objects.all().first()) else (False),
                                "kind_of_msg": "primary",
                                "message": "Product Created"
                        })
            else:
                    return render(request, "products/new_product.html", {
                        "form": form,
                        "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                        "has_category": True if (Category.objects.all().first()) else (False)
                    })
        return render(request, "products/new_product.html", {
            "form": NewProductForm(),
            "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
            "has_category": True if (Category.objects.all().first()) else (False)
        })
```

<p>

This one has a template, a message, and here has messages from another views too
</p>

> With Synapse:

```
@login_required
def show_product(request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product:
                watchlist = request.user.watchlist.filter().first()
                in_watchlist = watchlist and watchlist.have_this_product(product_id)

                comments = product.comments.filter()
                winner = product.is_winner(request.user.id)

                return render(request, "products/show_product.html", {
                        "product": product,
                        "is_owner": product.is_owner(request.user.id),
                        "comments": comments,
                        "in_watchlist": in_watchlist,
                        "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                        "has_category": True if (Category.objects.all().first()) else (False),
                        "message": get_message(request, "primary" if (winner) else (""), "Win a Gift" if (winner) else (""))
                })
        set_message(request, "danger", "Sorry, can't found this product.")
        return HttpResponseRedirect(reverse("index"))
```

> Without Synapse:

```
@login_required
def show_product(request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product:
                watchlist = request.user.watchlist.filter().first()
                in_watchlist = watchlist and watchlist.have_this_product(product_id)

                comments = product.comments.filter()
                winner = product.is_winner(request.user.id)

                return render(request, "products/show_product.html", {
                        "product": product,
                        "comments": comments,
                        "in_watchlist": in_watchlist,
                        "is_owner": product.is_owner(request.user.id),
                        "has_watchlist": True if (watchlist and watchlist.products.filter().first()) else (False),
                        "has_category": True if (Category.objects.all().first()) else (False), 
                        "kind_of_msg": "primary" if (winner and winner.id == request.user.id) else (None),
                        "message": "Congratulations you win!" if (winner and winner.id == request.user.id) else (None)
                })
        products = Product.objects.filter(active=True)
        return render(request, "products/index.html", {
                "products": products,
                "kind_of_msg": "danger",
                "message": "Sorry, can't found this product"
        })
```

<p>

Here has no template, only set a message and redirect to another view
</p>

> With Synapse:

```
@login_required
def add_to_watchlist(request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product:
                watchlist = request.user.watchlist.filter().first()
                if not watchlist:
                        watchlist = WatchList(user=request.user)
                        watchlist.save()
                if not watchlist.have_this_product(product_id):
                        watchlist.products.add(product)

                set_message(request, "success", "Product add to your WatchList.")
                return HttpResponseRedirect(reverse("show_product", args=(product.id,)))

        set_message(request, "danger", "Sorry, can't found this product.")
        return HttpResponseRedirect(reverse("index"))
```

> Without Synapse:

```
@login_required
def add_to_watchlist(request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product:
                watchlist = request.user.watchlist.filter().first()
                if not watchlist:
                        watchlist = WatchList(user=request.user)
                        watchlist.save()
                if not watchlist.have_this_product(product_id):
                        watchlist.products.add(product)
                in_watchlist = watchlist and watchlist.have_this_product(product_id)
                winner = product.has_winner()

                comments = product.comments.filter()

                return render(request, "products/show_product.html", {
                        "product": product,
                        "comments": comments,
                        "in_watchlist": in_watchlist,
                        "is_owner": product.is_owner(request.user.id),
                        "has_watchlist": True if (watchlist) else (False),
                        "has_category": True if (Category.objects.all().first()) else (False),
                        "kind_of_msg": "success",
                        "message": "Product add to your WatchList"
                })
        products = Product.objects.filter(active=True)
        return render(request, "products/index.html", {
                "products": products,
                "kind_of_msg": "danger",
                "message": "Sorry, can't found this product."
        })
```

<p>

Like de view before, only set a message and redirect to another view
</p>

> With Synapse:

```
@login_required
def remove_from_watchlist(request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product:
                watchlist = request.user.watchlist.filter().first()
                if watchlist and watchlist.have_this_product(product_id):
                        watchlist.products.remove(product)
                set_message(request, ("warning" if not watchlist.have_this_product(product_id) else ("danger")), ("Product removed from your WatchList!" if not watchlist.have_this_product(product_id) else ("Can't remove this Product from your Watchlist"))
                return HttpResponseRedirect(reverse("show_product", args=(product.id,)))

        set_message(request, "danger", "Sorry, can't found this product.")
        return HttpResponseRedirect(reverse("index"))
```
> Without Synapse:

```
@login_required
def remove_from_watchlist(request, product_id):
        product = Product.objects.filter(pk=product_id).first()
        if product:
                watchlist = request.user.watchlist.filter().first()
                if watchlist and watchlist.have_this_product(product_id):
                        watchlist.products.remove(product)
                comments = product.comments.filter()
                return render(request, "products/show_product.html", {
                        "product": product,
                        "comments": comments,
                        "in_watchlist": watchlist and watchlist.have_this_product(product_id),
                        "is_owner": product.is_owner(request.user.id),
                        "has_watchlist": True if (watchlist) else (False),
                        "has_category": True if (Category.objects.all().first()) else (False),
                        "kind_of_msg": "warning",
                        "message": "Product removed from your WatchList"
                })
        products = Product.objects.filter(active=True)
        return render(request, "products/index.html", {
                "products": products,
                "kind_of_msg": "danger",
                "message": "Sorry somethig wrong"
        })
```
