import os
import uuid
import json


def add_new_place(db_directory, location, name, type, description):
    """
    Persist new place.
    """
    # Convert GeoJSON to Python dictionary
    location_dict = json.loads(location)

    # Serialize data to json
    new_place_id = uuid.uuid4()
    place_dict = {
        'id': str(new_place_id),
        'location': location_dict['geometries'][0],
        'name': name,
        'type': type,
        'description': description
    }

    place_json = json.dumps(place_dict)

    # Write to file in {{db_directory}}/places/{{uuid}}.json
    # Make places dir if it doesn't exist
    places_dir = os.path.join(db_directory, 'places')
    if not os.path.exists(places_dir):
        os.mkdir(places_dir)

    # Name of the file is its id
    file_name = str(new_place_id) + '.json'
    file_path = os.path.join(places_dir, file_name)

    # Write json
    with open(file_path, 'w') as f:
        f.write(place_json)


def get_all_places(db_directory):
    """
    Get all persisted places.
    """
    # Write to file in {{db_directory}}/places/{{uuid}}.json
    # Make places dir if it doesn't exist
    places_dir = os.path.join(db_directory, 'places')
    if not os.path.exists(places_dir):
        os.mkdir(places_dir)

    places = []

    # Open each file and convert contents to python objects
    for place_json in os.listdir(places_dir):
        # Make sure we are only looking at json files
        if '.json' not in place_json:
            continue

        place_json_path = os.path.join(places_dir, place_json)
        with open(place_json_path, 'r') as f:
            place_dict = json.loads(f.readlines()[0])
            places.append(place_dict)

    return places
