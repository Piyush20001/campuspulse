"""
UF Campus locations data
"""

UF_LOCATIONS = [
    {
        'id': 1,
        'name': 'Library West',
        'category': 'LIBRARIES',
        'lat': 29.6508,
        'lon': -82.3424,
        'capacity': 150,
        'description': 'Main undergraduate library'
    },
    {
        'id': 2,
        'name': 'Marston Science Library',
        'category': 'LIBRARIES',
        'lat': 29.6480,
        'lon': -82.3444,
        'capacity': 120,
        'description': 'Science and engineering library'
    },
    {
        'id': 3,
        'name': 'Reitz Union',
        'category': 'STUDY SPOTS',
        'lat': 29.6465,
        'lon': -82.3473,
        'capacity': 200,
        'description': 'Student union and activity center'
    },
    {
        'id': 4,
        'name': 'Southwest Rec Center',
        'category': 'GYMS',
        'lat': 29.6421,
        'lon': -82.3521,
        'capacity': 180,
        'description': 'Recreation and fitness center'
    },
    {
        'id': 5,
        'name': 'The Hub',
        'category': 'DINING',
        'lat': 29.6434,
        'lon': -82.3508,
        'capacity': 160,
        'description': 'Central dining location'
    },
    {
        'id': 6,
        'name': 'Broward Dining',
        'category': 'DINING',
        'lat': 29.6502,
        'lon': -82.3453,
        'capacity': 140,
        'description': 'Dining hall'
    },
    {
        'id': 7,
        'name': 'Newell Hall',
        'category': 'ACADEMIC',
        'lat': 29.6495,
        'lon': -82.3434,
        'capacity': 100,
        'description': 'Academic building'
    },
    {
        'id': 8,
        'name': 'Norman Field',
        'category': 'OUTDOORS',
        'lat': 29.6512,
        'lon': -82.3512,
        'capacity': 250,
        'description': 'Outdoor recreation area'
    },
    {
        'id': 9,
        'name': 'Turlington Hall',
        'category': 'ACADEMIC',
        'lat': 29.6501,
        'lon': -82.3450,
        'capacity': 130,
        'description': 'Classroom building'
    },
    {
        'id': 10,
        'name': 'Student Rec Center',
        'category': 'GYMS',
        'lat': 29.6454,
        'lon': -82.3521,
        'capacity': 220,
        'description': 'Main recreation center'
    },
    {
        'id': 11,
        'name': 'Plaza of the Americas',
        'category': 'OUTDOORS',
        'lat': 29.6482,
        'lon': -82.3441,
        'capacity': 300,
        'description': 'Central plaza'
    },
    {
        'id': 12,
        'name': 'Hume Hall',
        'category': 'HOUSING',
        'lat': 29.6518,
        'lon': -82.3467,
        'capacity': 180,
        'description': 'Student housing'
    },
    {
        'id': 13,
        'name': 'Graham Study Center',
        'category': 'STUDY SPOTS',
        'lat': 29.6487,
        'lon': -82.3458,
        'capacity': 90,
        'description': '24/7 study space'
    },
    {
        'id': 14,
        'name': 'Pugh Hall',
        'category': 'ACADEMIC',
        'lat': 29.6476,
        'lon': -82.3418,
        'capacity': 110,
        'description': 'CLAS academic building'
    },
    {
        'id': 15,
        'name': 'Ben Hill Griffin Stadium',
        'category': 'OUTDOORS',
        'lat': 29.6500,
        'lon': -82.3486,
        'capacity': 400,
        'description': 'Football stadium area'
    }
]

def get_locations_by_category(category):
    """Filter locations by category"""
    if category == "ALL":
        return UF_LOCATIONS
    return [loc for loc in UF_LOCATIONS if loc['category'] == category]

def get_location_by_id(location_id):
    """Get location by ID"""
    for loc in UF_LOCATIONS:
        if loc['id'] == location_id:
            return loc
    return None

def get_location_by_name(name):
    """Get location by name"""
    for loc in UF_LOCATIONS:
        if loc['name'] == name:
            return loc
    return None
