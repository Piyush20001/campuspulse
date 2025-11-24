"""
Event data generator for Campus Pulse
"""
import random
from datetime import datetime, timedelta
from data.locations import UF_LOCATIONS

# Sample event data templates
EVENT_TEMPLATES = {
    'Academic': [
        {
            'title': 'Introduction to Machine Learning Workshop',
            'description': 'Learn the fundamentals of machine learning and neural networks. Hands-on coding session with Python and TensorFlow.',
            'tags': ['AI', 'Workshop', 'Technology']
        },
        {
            'title': 'Research Symposium: Climate Change',
            'description': 'Graduate students present their research on climate change impacts and sustainability solutions.',
            'tags': ['Research', 'Science', 'Sustainability']
        },
        {
            'title': 'Career Fair - Engineering',
            'description': 'Meet recruiters from top tech companies. Bring your resume and dress professionally.',
            'tags': ['Career', 'Engineering', 'Networking']
        },
        {
            'title': 'Guest Lecture: Future of Quantum Computing',
            'description': 'Dr. Sarah Chen from MIT discusses breakthrough developments in quantum computing.',
            'tags': ['Lecture', 'Technology', 'Physics']
        },
        {
            'title': 'Undergraduate Research Opportunities Fair',
            'description': 'Explore research opportunities across all departments. Perfect for sophomores and juniors.',
            'tags': ['Research', 'Academic', 'Opportunities']
        }
    ],
    'Social': [
        {
            'title': 'Gator Nights: Casino Night',
            'description': 'Free casino-style games, prizes, and snacks. No real gambling, just fun!',
            'tags': ['Entertainment', 'Games', 'Free Food']
        },
        {
            'title': 'International Coffee Hour',
            'description': 'Meet students from around the world. Free coffee and snacks provided.',
            'tags': ['Cultural', 'International', 'Coffee']
        },
        {
            'title': 'Spring Concert ft. Local Bands',
            'description': 'Outdoor concert featuring three local bands. Free admission with Gator ID.',
            'tags': ['Music', 'Concert', 'Outdoor']
        },
        {
            'title': 'Movie Night: Classic Film Series',
            'description': 'This week: The Shawshank Redemption. Free popcorn!',
            'tags': ['Movie', 'Entertainment', 'Free']
        },
        {
            'title': 'Paint & Sip Social',
            'description': 'Guided painting session with mocktails. All materials provided.',
            'tags': ['Art', 'Creative', 'Social']
        }
    ],
    'Sports': [
        {
            'title': 'Gators vs Tennessee - Football',
            'description': 'Home game at Ben Hill Griffin Stadium. Gates open 2 hours before kickoff.',
            'tags': ['Football', 'Game Day', 'Gators']
        },
        {
            'title': 'Intramural Basketball Championship',
            'description': 'Finals of the spring intramural basketball tournament. Free spectating.',
            'tags': ['Basketball', 'Intramural', 'Championship']
        },
        {
            'title': '5K Charity Run for Education',
            'description': 'Campus 5K run/walk. Registration includes t-shirt. Proceeds benefit local schools.',
            'tags': ['Running', '5K', 'Charity']
        },
        {
            'title': 'Yoga in the Plaza',
            'description': 'Free outdoor yoga session. Bring your own mat. All levels welcome.',
            'tags': ['Yoga', 'Fitness', 'Wellness']
        },
        {
            'title': 'Swimming & Diving Meet',
            'description': 'UF Swimming vs Georgia. Stephen C. O\'Connell Center pool.',
            'tags': ['Swimming', 'Competition', 'Gators']
        }
    ],
    'Cultural': [
        {
            'title': 'Diwali Festival Celebration',
            'description': 'Celebrate the Festival of Lights with traditional food, music, and dance performances.',
            'tags': ['Cultural', 'Festival', 'Indian']
        },
        {
            'title': 'Latin Dance Night',
            'description': 'Learn salsa, bachata, and merengue. No partner or experience required.',
            'tags': ['Dance', 'Latin', 'Lessons']
        },
        {
            'title': 'African Students Association Showcase',
            'description': 'Fashion show, poetry, and musical performances celebrating African culture.',
            'tags': ['Cultural', 'Performance', 'African']
        },
        {
            'title': 'Asian Night Market',
            'description': 'Street food, games, and performances from across Asia. Pay with Gator Bucks.',
            'tags': ['Food', 'Cultural', 'Market']
        },
        {
            'title': 'Indigenous Peoples Heritage Month Panel',
            'description': 'Discussion on indigenous history, culture, and contemporary issues.',
            'tags': ['Cultural', 'Educational', 'Panel']
        }
    ]
}

class EventGenerator:
    def __init__(self):
        self.locations = UF_LOCATIONS

    def generate_random_events(self, num_events=20):
        """Generate random events"""
        events = []
        event_id = 1

        for _ in range(num_events):
            # Pick random category
            category = random.choice(list(EVENT_TEMPLATES.keys()))
            template = random.choice(EVENT_TEMPLATES[category])

            # Pick random location
            location = random.choice(self.locations)

            # Generate random time (within next 14 days)
            days_ahead = random.randint(0, 14)
            hour = random.randint(9, 21)
            start_time = datetime.now() + timedelta(days=days_ahead, hours=hour - datetime.now().hour)
            start_time = start_time.replace(minute=random.choice([0, 15, 30, 45]), second=0, microsecond=0)

            # Duration: 1-4 hours
            duration_hours = random.choice([1, 1.5, 2, 2.5, 3, 4])
            end_time = start_time + timedelta(hours=duration_hours)

            event = {
                'id': event_id,
                'title': template['title'],
                'description': template['description'],
                'category': category,
                'tags': template['tags'],
                'location_name': location['name'],
                'location_id': location['id'],
                'start_time': start_time,
                'end_time': end_time,
                'organizer': self._generate_organizer(),
                'attendees_expected': random.randint(20, min(200, location['capacity'])),
                'is_free': random.choice([True, True, True, False]),  # 75% free
                'registration_required': random.choice([True, False])
            }

            events.append(event)
            event_id += 1

        # Sort by start time
        events.sort(key=lambda x: x['start_time'])
        return events

    def _generate_organizer(self):
        """Generate random organizer name"""
        organizations = [
            'Student Government',
            'Reitz Union Board',
            'UF Recreation',
            'International Center',
            'Career Connections Center',
            'Greek Life',
            'Graduate Student Council',
            'Department of Computer Science',
            'College of Liberal Arts',
            'Asian American Student Union',
            'Black Student Union',
            'Hispanic Student Association',
            'Engineering Student Council',
            'Pre-Med Society',
            'Entrepreneurship Club'
        ]
        return random.choice(organizations)

    def get_upcoming_events(self, events, limit=10):
        """Get upcoming events"""
        now = datetime.now()
        upcoming = [e for e in events if e['start_time'] > now]
        return sorted(upcoming, key=lambda x: x['start_time'])[:limit]

    def get_events_by_category(self, events, category):
        """Filter events by category"""
        if category == 'All':
            return events
        return [e for e in events if e['category'] == category]

    def get_events_by_location(self, events, location_id):
        """Get events at a specific location"""
        return [e for e in events if e['location_id'] == location_id]

    def get_events_today(self, events):
        """Get events happening today"""
        today = datetime.now().date()
        return [e for e in events if e['start_time'].date() == today]

# Training data for event classifier
TRAINING_EVENTS = [
    # Academic
    ("Machine Learning Workshop with Python", "Learn ML fundamentals", "Academic"),
    ("Career Fair Engineering Students", "Meet recruiters from top companies", "Academic"),
    ("Research Symposium Climate Science", "Graduate research presentations", "Academic"),
    ("Guest Lecture Quantum Computing", "Dr. Chen from MIT presents", "Academic"),
    ("Thesis Defense Computer Science", "PhD candidate presents research", "Academic"),
    ("Study Abroad Information Session", "Learn about international programs", "Academic"),
    ("Honors Convocation Ceremony", "Recognizing academic excellence", "Academic"),
    ("Graduate School Application Workshop", "Tips for strong applications", "Academic"),

    # Social
    ("Casino Night Gator Nights", "Free games and prizes", "Social"),
    ("Movie Night Free Popcorn", "Classic film screening", "Social"),
    ("Paint and Sip Event", "Creative social gathering", "Social"),
    ("Coffee Hour Meet Friends", "Casual social meetup", "Social"),
    ("Trivia Night Prizes", "Test your knowledge", "Social"),
    ("Game Night Board Games", "Fun evening with friends", "Social"),
    ("Karaoke Night Reitz Union", "Sing your favorite songs", "Social"),
    ("Speed Friending Event", "Make new connections", "Social"),

    # Sports
    ("Football Game Gators vs Tennessee", "Home game at stadium", "Sports"),
    ("Basketball Championship Finals", "Intramural tournament", "Sports"),
    ("5K Charity Run", "Campus run for education", "Sports"),
    ("Yoga in the Plaza", "Free outdoor fitness", "Sports"),
    ("Swimming Meet vs Georgia", "Competitive swimming", "Sports"),
    ("Volleyball Tournament", "Recreational sports competition", "Sports"),
    ("Soccer Practice Session", "Club soccer training", "Sports"),
    ("Marathon Training Group", "Long distance running", "Sports"),

    # Cultural
    ("Diwali Festival Celebration", "Festival of Lights event", "Cultural"),
    ("Latin Dance Night Salsa", "Learn traditional dances", "Cultural"),
    ("African Cultural Showcase", "Fashion and music performances", "Cultural"),
    ("Asian Night Market", "Street food and games", "Cultural"),
    ("Indigenous Heritage Panel", "Educational discussion", "Cultural"),
    ("International Food Festival", "Cuisine from around the world", "Cultural"),
    ("Lunar New Year Celebration", "Chinese cultural event", "Cultural"),
    ("Caribbean Carnival", "Music and dance celebration", "Cultural"),
]
