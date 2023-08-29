from django.shortcuts import render, redirect
import logging
from .models import category
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required


@login_required(login_url='admin_login1')
def categories(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    categories = category.objects.all().order_by('id')
    return render(request, 'category/category.html', {'categories': categories})

@login_required(login_url='admin_login1')
def add_category(request):
    try:
        if not request.user.is_superuser:
            return redirect('admin_login1')

        if request.method == 'POST':
            image = request.FILES.get('image', None)
            name = request.POST['categories']
            description = request.POST['categories_discription']
            
            # Validation
            if name.strip() == '':
                messages.error(request, 'Name Not Found!')
                return redirect('categories')

            if category.objects.filter(categories=name).exists():
                messages.error(request, 'Category name already exists')
                return redirect('categories')
            # Save
            if not image:
                messages.error(request, 'Image not uploaded')
                return redirect('categories')

            new_category = category(categories=name, categories_discription=description, categories_image=image)
            new_category.save()
            messages.success(request,'category added successfully!')
            return redirect('categories')
    except:
        
            return redirect('categories')
    
@login_required(login_url='admin_login1')
def editcategory(request, editcategory_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if request.method == 'POST':
        name = request.POST['categories']
        description = request.POST['categories_discription']

# validation
        try:
            caterg = category.objects.get(id=editcategory_id)
            image = request.FILES.get('image')
            if image:
                caterg.categories_image = image
                caterg.save()
        except category.DoesNotExist:
            messages.error(request,'Image Not Fount')
            return redirect('categories')
        if name.strip() == '':
            messages.error(request,'Name field is empty')
            return redirect('categories')
        if category.objects.filter(categories=name).exists():
            check = category.objects.get(id = editcategory_id)
            if name == check.categories:
                pass
            else:
                messages.error(request, 'category name already exists')
                return redirect('categories')
        
        categr = category.objects.get(id=editcategory_id)
        categr.categories = name
        categr.slug = name
        categr.categories_discription = description
        categr.save()
        messages.success(request,'category edited successfully!')
        return redirect ('categories')
    
def deletecategory(request,deletecategory_id):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    categery = category.objects.get(id=deletecategory_id)
    categery.delete()
    messages.success(request,'category deleted successfully!')
    return redirect('categories')

# Search Category
@login_required(login_url='admin_login1')
def search_category(request):
    if not request.user.is_superuser:
        return redirect('admin_login1')
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cate = category.objects.filter(categories__icontains=keyword).order_by('id')
            if cate.exists():
                context = {
                    'category': cate,
                }
                return render(request, 'category/category.html', context)
            else:
                message = "Category not found"
                return render(request, 'category/category.html', {'message': message})
        else:
            message = "Please enter a valid search keyword"
            return render(request, 'category/category.html', {'message': message})
    else:
        return render(request, '404.html')
