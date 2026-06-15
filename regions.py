from calgen.location_utils import extract_location_info
from calgen.regions import EventRejected

# Region taxonomy for the Salt Lake City / Wasatch Front metro area.
# Mirrors dctech.events' DC/MD/VA pattern: a core city region plus the
# surrounding counties that make up the metro within ~40 miles of downtown SLC.
_REGIONS = [
    {'slug': 'salt-lake-city', 'name': 'Salt Lake City'},
    {'slug': 'davis-county', 'name': 'Davis County'},
    {'slug': 'weber-county', 'name': 'Weber County'},
    {'slug': 'utah-county', 'name': 'Utah County'},
    {'slug': 'tooele-county', 'name': 'Tooele County'},
    {'slug': 'summit-county', 'name': 'Summit County (Park City)'},
]

# Main / default region for in-state locations we can't otherwise place.
_DEFAULT_SLUG = 'salt-lake-city'

# Map known metro cities (lowercased) to a region slug.
# Salt Lake County cities collapse into the core 'salt-lake-city' region;
# outer counties get their own region, like MD/VA in the DC site.
_CITY_TO_SLUG = {
    # --- Salt Lake County (core) -> salt-lake-city ---
    'salt lake city': 'salt-lake-city',
    'west valley city': 'salt-lake-city',
    'west valley': 'salt-lake-city',
    'west jordan': 'salt-lake-city',
    'south jordan': 'salt-lake-city',
    'sandy': 'salt-lake-city',
    'sandy city': 'salt-lake-city',
    'murray': 'salt-lake-city',
    'taylorsville': 'salt-lake-city',
    'draper': 'salt-lake-city',
    'riverton': 'salt-lake-city',
    'herriman': 'salt-lake-city',
    'cottonwood heights': 'salt-lake-city',
    'holladay': 'salt-lake-city',
    'midvale': 'salt-lake-city',
    'millcreek': 'salt-lake-city',
    'south salt lake': 'salt-lake-city',
    'magna': 'salt-lake-city',
    'bluffdale': 'salt-lake-city',
    'kearns': 'salt-lake-city',

    # --- Davis County -> davis-county ---
    'layton': 'davis-county',
    'bountiful': 'davis-county',
    'west bountiful': 'davis-county',
    'clearfield': 'davis-county',
    'kaysville': 'davis-county',
    'farmington': 'davis-county',
    'centerville': 'davis-county',
    'north salt lake': 'davis-county',
    'syracuse': 'davis-county',
    'clinton': 'davis-county',
    'woods cross': 'davis-county',
    'fruit heights': 'davis-county',
    'west point': 'davis-county',
    'sunset': 'davis-county',

    # --- Weber County -> weber-county ---
    'ogden': 'weber-county',
    'north ogden': 'weber-county',
    'south ogden': 'weber-county',
    'roy': 'weber-county',
    'riverdale': 'weber-county',
    'washington terrace': 'weber-county',
    'pleasant view': 'weber-county',
    'west haven': 'weber-county',
    'harrisville': 'weber-county',

    # --- Utah County -> utah-county ---
    'provo': 'utah-county',
    'orem': 'utah-county',
    'lehi': 'utah-county',
    'american fork': 'utah-county',
    'pleasant grove': 'utah-county',
    'lindon': 'utah-county',
    'springville': 'utah-county',
    'spanish fork': 'utah-county',
    'saratoga springs': 'utah-county',
    'eagle mountain': 'utah-county',
    'vineyard': 'utah-county',
    'highland': 'utah-county',
    'cedar hills': 'utah-county',
    'alpine': 'utah-county',
    'mapleton': 'utah-county',
    'payson': 'utah-county',

    # --- Tooele County -> tooele-county ---
    'tooele': 'tooele-county',
    'grantsville': 'tooele-county',
    'stansbury park': 'tooele-county',
    'erda': 'tooele-county',

    # --- Summit County (Park City area) -> summit-county ---
    'park city': 'summit-county',
    'snyderville': 'summit-county',
    'coalville': 'summit-county',
    'kamas': 'summit-county',
}


def list_regions():
    return _REGIONS


def location_to_region(location_str):
    if not location_str or not location_str.strip():
        return None

    city_name, state = extract_location_info(location_str)

    # Reject events that clearly belong to another state.
    if state and state.upper() != 'UT':
        raise EventRejected(
            f"Event is in {state.upper()}, outside the Salt Lake City metro area"
        )

    # Couldn't determine a state (e.g. online/unparseable) -> can't place it.
    if not state:
        return None

    # Map a known metro city to its region.
    if city_name:
        slug = _CITY_TO_SLUG.get(city_name.strip().lower())
        if slug:
            return slug

    # Unknown but in-state location: default to the core city region.
    return _DEFAULT_SLUG
