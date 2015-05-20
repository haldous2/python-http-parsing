# import requests
# import json
# from pprint import pprint

# url = 'http://maps.googleapis.com/maps/api/geocode/json'
# addr = '1325 4th Ave, Seattle, 98101'
# parameters = {'address': addr, 'sensor': 'false' }
#
# resp = requests.get(url, params=parameters)
# data = json.loads(resp.text)
# if data['status'] == 'OK':
#
#     #pprint(data)
#
#     location = data['results'][0]['geometry']['location']
#     latlng="{lat},{lng}".format(**location)
#     parameters = {'latlng': latlng, 'sensor': 'false'}
#     resp = requests.get(url, params=parameters)
#     data = json.loads(resp.text)
#     if data['status'] == 'OK':
#
#         pprint(data)

# response = geocoder.google('3906 Dayton Ave. N., Seattle, WA 98103')
# response.json
# print response.geojson
# print response["address"]

## pip install geocoder
import geocoder

def get_geojson(result):

    address = " ".join(result.get('Address', ''))

    if not address:
        return None

    geocoded = geocoder.google(address)
    geojson = geocoded.geojson
    inspection_data = {}
    use_keys = (
        'Business Name', 'Average Score', 'Total Inspections', 'High Score'
    )
    for key, val in result.items():
        if key not in use_keys:
            continue
        if isinstance(val, list):
            val = " ".join(val)
        inspection_data[key] = val
    geojson['properties'] = inspection_data

    return geojson

dAddress = {'Address':'3906 Dayton Ave. N.'}
print get_geojson(dAddress)
