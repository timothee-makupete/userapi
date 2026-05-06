import requests
from django.conf import settings

def fetch_external_users():
    """Fetch users from external API with error handling."""
    url = getattr(settings, 'EXTERNAL_API_URL', 'https://jsonplaceholder.typicode.com/users')
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return True, response.json()
    except requests.exceptions.ConnectionError:
        return False, "API connection failed: Unable to reach the server"
    except requests.exceptions.Timeout:
        return False, "API request timed out"
    except requests.exceptions.HTTPError as e:
        return False, f"API HTTP error: {e}"
    except requests.exceptions.RequestException as e:
        return False, f"API request failed: {str(e)}"
    except ValueError as e:
        return False, f"Invalid JSON response: {str(e)}"

def transform_user_data(external_user):
    """Transform external API user data to match our model structure with nested address/company."""
    address = external_user.get('address', {})
    company = external_user.get('company', {})
    geo = address.get('geo', {})
    
    return {
        'external_id': external_user.get('id'),
        'name': external_user.get('name', ''),
        'username': external_user.get('username', ''),
        'email': external_user.get('email', ''),
        'phone': external_user.get('phone', ''),
        'website': external_user.get('website', ''),
        'address': {
            'street': address.get('street', ''),
            'suite': address.get('suite', ''),
            'city': address.get('city', ''),
            'zipcode': address.get('zipcode', ''),
            'lat': geo.get('lat', ''),
            'lng': geo.get('lng', ''),
        },
        'company': {
            'name': company.get('name', ''),
            'catch_phrase': company.get('catchPhrase', ''),
            'bs': company.get('bs', ''),
        }
    }