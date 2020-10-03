from geopy.geocoders import Nominatim


def get_atm_addresses_by_coords(lat_lon_2d_array):
    geolocator = Nominatim(user_agent="gazprombank-atm-geolocation-app")

    return [
        '\n'.join((
            f'Банкомат №{index}',
            f'ШИРОТА: {lat} ; ДОЛГОТА: {lon}',
            'АДРЕС: ' + geolocator.reverse(f'{lat} {lon}').address
        ))
        for index, [lat, lon] in enumerate(lat_lon_2d_array, start=1)
    ]
