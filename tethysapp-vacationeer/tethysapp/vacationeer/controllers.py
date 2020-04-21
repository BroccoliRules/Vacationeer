from django.contrib import messages
from django.shortcuts import render, reverse, redirect
from tethys_sdk.permissions import login_required
from tethys_sdk.gizmos import (Button, MapView, TextInput, DatePicker,
                               SelectInput, DataTableView, MVDraw, MVView,
                               MVLayer)
from tethys_sdk.workspaces import app_workspace
from .model import add_new_place, get_all_places


@app_workspace
@login_required()
def home(request, app_workspace):
    """
    Controller for the app home page.
    """
    # Get list of places and create places MVLayer:
    places = get_all_places(app_workspace.path)
    features = []
    lat_list = []
    lng_list = []

    # Define GeoJSON Features
    for place in places:
        place_location = place.pop('location')
        lat_list.append(place_location['coordinates'][1])
        lng_list.append(place_location['coordinates'][0])

        place_feature = {
            'type': 'Feature',
            'geometry': {
                'type': place_location['type'],
                'coordinates': place_location['coordinates'],
            }
        }

        features.append(place_feature)

    # Define GeoJSON FeatureCollection
    places_feature_collection = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'EPSG:4326'
            }
        },
        'features': features
    }

    style = {'ol.style.Style': {
        'image': {'ol.style.Circle': {
            'radius': 10,
            'fill': {'ol.style.Fill': {
                'color':  '#d84e1f'
            }},
            'stroke': {'ol.style.Stroke': {
                'color': '#ffffff',
                'width': 1
            }}
        }}
    }}

    # Create a Map View Layer
    places_layer = MVLayer(
        source='GeoJSON',
        options=places_feature_collection,
        legend_title='Places',
        layer_options={'style': style}
    )

    # Define view centered on place locations
    try:
        view_center = [sum(lng_list) / float(len(lng_list)), sum(lat_list) / float(len(lat_list))]
    except ZeroDivisionError:
        view_center = [-84.079149, 9.933149]

    view_options = MVView(
        projection='EPSG:4326',
        center=view_center,
        zoom=8.5,
        maxZoom=18,
        minZoom=2
    )

    vacationeer_map = MapView(
        height='100%',
        width='100%',
        layers=[places_layer],
        basemap='OpenStreetMap',
        view=view_options
    )

    add_place_button = Button(
        display_text='Add place',
        name='add-place-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        href=reverse('vacationeer:add_place')
    )

    context = {
        'vacationeer_map': vacationeer_map,
        'add_place_button': add_place_button
    }

    return render(request, 'vacationeer/home.html', context)


@app_workspace
@login_required()
def add_place(request, app_workspace):
    """
    Controller for the Add place page.
    """
    # Default Values
    name = ''
    type = ''
    description = ''
    location = ''

    # Errors
    name_error = ''
    type_error = ''
    location_error = ''
    description_error = ''

    # Handle form submission
    if request.POST and 'add-button' in request.POST:
        # Get values
        has_errors = False
        name = request.POST.get('name', None)
        type = request.POST.get('type', None)
        description = request.POST.get('description', None)
        location = request.POST.get('geometry', None)

        # Validate
        if not name:
            has_errors = True
            name_error = 'Name is required.'

        if not type:
            has_errors = True
            type_error = 'type is required.'

        if not description:
            has_errors = True
            date_error = 'Date Built is required.'

        if not location:
            has_errors = True
            location_error = 'Location is required.'

        if not has_errors:
            add_new_place(db_directory=app_workspace.path, location=location, name=name, type=type, description=description)
            return redirect(reverse('vacationeer:home'))

        messages.error(request, "Please fix errors.")

    # Define form gizmos
    name_input = TextInput(
        display_text='Name',
        name='name',
        initial=name,
        error=name_error
    )

    type_input = SelectInput(
        display_text='Type of Activity',
        name='type',
        multiple=False,
        options=[('Adventure', 'Adventure'), ('Relax', 'Relax'), ('Sightseeing', 'Sightseeing')],
        initial=['Adventure'],
        error=type_error
    )

    description = TextInput(
        name='description',
        display_text='Description of Activity',
        initial=description,
        error=description_error
    )

    initial_view = MVView(
        projection='EPSG:4326',
        center=[-84.079149, 9.933149],
        zoom=7.5
    )
    drawing_options = MVDraw(
            controls=['Modify', 'Delete', 'Move', 'Point'],
            initial='Point',
            output_format='GeoJSON',
            point_color='#FF0000'
            )
    location_input = MapView(
        height='500px',
        width='100%',
        basemap='OpenStreetMap',
        draw=drawing_options,
        view=initial_view
    )

    add_button = Button(
        display_text='Add',
        name='add-button',
        icon='glyphicon glyphicon-plus',
        style='success',
        attributes={'form': 'add-place-form'},
        submit=True
    )

    cancel_button = Button(
        display_text='Cancel',
        name='cancel-button',
        href=reverse('vacationeer:home')
    )

    context = {
        'name_input': name_input,
        'type_input': type_input,
        'description_input': description,
        'location_input': location_input,
        'location_error': location_error,
        'add_button': add_button,
        'cancel_button': cancel_button,
    }

    return render(request, 'vacationeer/add_place.html', context)



@app_workspace
@login_required()
def list_places(request, app_workspace):
    """
    Show all places in a table view.
    """
    places = get_all_places(app_workspace.path)
    table_rows = []

    for place in places:
        table_rows.append(
            (
                place['name'],
                place['type'], place['description']
            )
        )

    places_table = DataTableView(
        column_names=('Name', 'Type', 'Description'),
        rows=table_rows,
        searching=False,
        orderClasses=False,
        lengthMenu=[ [10, 25, 50, -1], [10, 25, 50, "All"] ],
    )

    context = {
        'places_table': places_table
    }

    return render(request, 'vacationeer/list_places.html', context)
