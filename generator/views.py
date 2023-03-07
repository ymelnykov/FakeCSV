import csv
import json
import os
from datetime import datetime

from faker import Faker

from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import User, Schema, Column, DataSet


fake = Faker()

# Create your views here.

def login_view(request):
    if request.method == 'POST':
        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'generator/login.html', {
                'message': 'Invalid username and/or password.',
                'username': username,
            })
    else:
        return render(request, 'generator/login.html')


def logout_view(request):
    # Logout user
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        new_user = dict(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            email=email,
            )
        # Ensure password matches confirmation
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')
        if password != confirmation:
            return render(request, 'generator/register.html', {
                'user': new_user,
                'message': 'Passwords must match.',
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            user.first_name = first_name
            user.last_name = last_name
            user.save(update_fields=['first_name', 'last_name'])
        except IntegrityError:
                return render(request, 'generator/register.html', {
                'user': new_user,
                'message': 'Username already taken.',
            })
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'generator/register.html')


def index(request):
    # If user is authenticate, show data schemas, else login
    if request.user.is_authenticated:
        queryset = Schema.objects.filter(
                owner=request.user).order_by('modified')
        schemas = list(enumerate(list(queryset), start=1))
        return render(request, 'generator/schemas.html', {
            'schemas': schemas,
        })
    else:
        return render(request, 'generator/login.html')


def create_schema(request):
    # Create new data schema
    if request.method == 'POST':
        # Get schema data from the form
        schema_name = request.POST.get('schema_name')
        schema_delimiter = request.POST.get('schema_delimiter')
        schema_character = request.POST.get('schema_character')
        # Create new schema object
        new_schema = Schema.objects.create(
            name=schema_name,
            delimiter=schema_delimiter,
            character=schema_character,
            owner=request.user,
        )
        # Get columns data from the form
        names = request.POST.getlist('name')
        types = request.POST.getlist('type')
        starts = request.POST.getlist('start')
        ends = request.POST.getlist('end')
        orders = request.POST.getlist('order')
        # Create column objects
        for i in range(len(names)):
            new_column = Column.objects.create(
                name=names[i],
                type=types[i],
                start=starts[i],
                end=ends[i],
                order=orders[i],
                owner=new_schema,
            )
        # Return new schema and datasets representation
        columns = Column.objects.filter(
                owner=new_schema).order_by('order')
        queryset = DataSet.objects.filter(owner=new_schema)
        datasets = list(enumerate(list(queryset), start=1))
        return render(request, 'generator/datasets.html', {
            'schema': new_schema,
            'columns': columns,
            'message': 'New schema successfully created!',
            'datasets': datasets,
        })
        # Return schemas page
        # queryset = Schema.objects.filter(
        #         owner=request.user).order_by('-modified')
        # schemas = list(enumerate(list(queryset), start=1))
        # return render(request, 'generator/schemas.html', {
        #     'schemas': schemas,
        #     'message': 'New schema successfully created!',
        # })
    else:
        columns = [(1, {'start': 0, 'end': 0})]
        return render(request, 'generator/schema.html', {
            'columns': columns
        })


def update_schema(request):
    # Update existing schema
    if request.method == 'GET':
        # Show prepopulated form with schema data
        schema_id = request.GET.get('schema_id')
        schema = Schema.objects.get(pk=schema_id)
        queryset = Column.objects.filter(
                owner=schema_id).order_by('order')
        columns = list(enumerate(list(queryset), start=1))
        return render(request, 'generator/schema.html', {
            'schema': schema,
            'columns': columns,
        })
    else:
        # Get schema data from the form and save changes
        schema_id = request.POST.get('schema_id')
        schema = Schema.objects.get(pk=schema_id)
        schema.name = request.POST.get('schema_name')
        schema.delimiter = request.POST.get('schema_delimiter')
        schema.character = request.POST.get('schema_character')
        schema.save()
        # Get columns data from the form
        names = request.POST.getlist('name')
        types = request.POST.getlist('type')
        starts = request.POST.getlist('start')
        ends = request.POST.getlist('end')
        orders = request.POST.getlist('order')
        # Delete all existing schema columns
        Column.objects.filter(owner=schema_id).delete()
        # Create new schema columns
        for i in range(len(names)):
            new_column = Column.objects.create(
                name=names[i],
                type=types[i],
                start=starts[i],
                end=ends[i],
                order=orders[i],
                owner=schema,
            )
        # Return updated schema and datasets representation
        columns = Column.objects.filter(
                owner=schema_id).order_by('order')
        queryset = DataSet.objects.filter(owner=schema)
        datasets = list(enumerate(list(queryset), start=1))
        return render(request, 'generator/datasets.html', {
            'schema': schema,
            'columns': columns,
            'message': 'Schema successfully updated!',
            'datasets': datasets,
        })
        # Return schemas page
        # queryset = Schema.objects.filter(
        #         owner=request.user).order_by('-modified')
        # schemas = list(enumerate(list(queryset), start=1))
        # return render(request, 'generator/schemas.html', {
        #     'schemas': schemas,
        #     'message': 'Schema successfully updated!',
        # })


def delete_schema(request):
    # Delete existing schema using Delete button
    if request.method == 'POST':
        schema_id = request.POST.get('schema_id')
        schema = Schema.objects.get(pk=schema_id)
        schema.delete()
        return HttpResponseRedirect(reverse('index'))
    else:
        return HttpResponse('Method must be "POST".')


"""Generate fake datasets in csv files using Faker library"""
def get_faker_method(type, *args):
    # Get Faker method to be used to generate fake data
    if getattr(fake, type) and callable(method := getattr(fake, type)):
        if type == 'paragraph':
            return method(fake.pyint(*args))
        else:
            return method(*args)


def create_fake_data(rows_number, columns):
    # Generate fake data records
    rows = []
    for _ in range(rows_number):
        row = {}
        for column in columns:
            if column.type == 'pyint' or column.type == 'paragraph':
                row[column.name] = get_faker_method(
                        column.type, int(column.start), int(column.end))
            else:
                row[column.name] = get_faker_method(column.type)
        rows.append(row)
    return rows


def create_csv_file(file, rows, schema, columns):
    # Create csv file with fake data records
    with open(file, 'w', newline='') as csvfile:
        fieldnames = [column.name for column in columns]
        writer = csv.DictWriter(
                csvfile, 
                fieldnames=fieldnames, 
                delimiter=schema.delimiter, 
                quotechar=schema.character,
                )
        writer.writeheader()
        writer.writerows(rows)


@csrf_exempt
def create_dataset(request):
    if request.method == 'GET':
        # Show existing datasets for chosen schema
        schema_id = request.GET.get('schema_id')
        schema = Schema.objects.get(pk=schema_id)
        columns = Column.objects.filter(owner=schema_id).order_by('order')
        queryset = DataSet.objects.filter(owner=schema_id)
        datasets = list(enumerate(list(queryset), start=1))
        return render(request, 'generator/datasets.html', {
            'schema': schema,
            'columns': columns,
            'datasets': datasets,
        })
    else:
        # Get data from json request
        data = json.loads(request.body)
        schema_id = data.get('schemaId')
        rows_number = int(data.get('rowsNumber'))
        schema = Schema.objects.get(pk=schema_id)
        columns = Column.objects.filter(owner=schema_id).order_by('order')
        # Create new dataset file
        dataset_name = f'{schema.name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        with open(dataset_name, 'a+') as f:
            dataset_file = File(f, name=dataset_name)
            new_dataset = DataSet.objects.create(
                    name = dataset_name,
                    file = dataset_file,
                    owner = schema,
                    )
        os.remove(dataset_name)
        # Generate data and record into the dataset file
        rows = create_fake_data(rows_number, columns)
        create_csv_file(new_dataset.file.path, rows, schema, columns)
        new_dataset.save()
        # Return json response with the dataset file url and date of creation
        url = new_dataset.get_file_url
        created = new_dataset.created.strftime('%Y-%m-%d %H:%M:%S')
        return JsonResponse({
            'url': url,
            'created': created,
            })

