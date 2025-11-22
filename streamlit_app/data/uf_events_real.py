"""
Comprehensive UF Events Data - 100 Real Campus Events
"""
import random
from datetime import datetime, timedelta
from data.locations import UF_LOCATIONS

# Comprehensive UF Event Templates organized by category
UF_EVENT_TEMPLATES = {
    'Academic': [
        # Career Events
        {
            'title': 'Career Showcase - Fall',
            'description': 'Largest campus career fair in the Southeast. Connect with 300+ employers from Fortune 500 companies to startups. Bring multiple copies of your resume and dress professionally.',
            'tags': ['Career', 'Networking', 'Professional', 'Recruiting'],
            'attendees_range': (1500, 3000)
        },
        {
            'title': 'Career Showcase - Spring',
            'description': 'Spring semester career fair featuring top employers across all industries. Perfect opportunity for internships and full-time positions.',
            'tags': ['Career', 'Internship', 'Jobs', 'Recruiting'],
            'attendees_range': (1200, 2500)
        },
        {
            'title': 'Technical Day Career Fair',
            'description': 'Specialized career fair for STEM majors. Meet recruiters from tech companies, engineering firms, and research organizations.',
            'tags': ['Technology', 'Engineering', 'STEM', 'Career'],
            'attendees_range': (800, 1500)
        },
        {
            'title': 'Non-Technical Day Career Fair',
            'description': 'Career fair for business, liberal arts, and humanities majors. Explore opportunities in marketing, finance, communications, and more.',
            'tags': ['Business', 'Career', 'Liberal Arts', 'Professional'],
            'attendees_range': (600, 1200)
        },
        {
            'title': 'Opportunity Meet-Up / Diversity Meet-Up',
            'description': 'Connect with employers committed to diversity and inclusion. Special focus on underrepresented groups in various industries.',
            'tags': ['Diversity', 'Career', 'Inclusion', 'Networking'],
            'attendees_range': (300, 600)
        },
        {
            'title': 'Part-Time Job Fair',
            'description': 'Find part-time employment opportunities on and around campus. Perfect for students seeking flexible work during the semester.',
            'tags': ['Part-Time', 'Jobs', 'Student Employment', 'Career'],
            'attendees_range': (400, 800)
        },
        {
            'title': 'Just in Time Fair - Spring',
            'description': 'Last-chance career fair for graduating seniors. Limited spots available with employers still hiring for immediate positions.',
            'tags': ['Career', 'Graduating', 'Jobs', 'Seniors'],
            'attendees_range': (300, 500)
        },
        {
            'title': 'Summer Experience Fair',
            'description': 'Explore summer internship and research opportunities. Connect with organizations offering summer programs worldwide.',
            'tags': ['Internship', 'Summer', 'Research', 'Experience'],
            'attendees_range': (500, 1000)
        },
        {
            'title': 'Graduate and Professional Schools Fair',
            'description': 'Meet representatives from graduate programs across the country. Learn about master\'s, PhD, law, and medical school opportunities.',
            'tags': ['Graduate School', 'Education', 'Professional', 'Advanced Degree'],
            'attendees_range': (400, 800)
        },
        {
            'title': 'CISE AI Career Fair',
            'description': 'Computer Science and AI-focused career fair. Meet companies working on cutting-edge AI, machine learning, and data science.',
            'tags': ['AI', 'Computer Science', 'Technology', 'Career'],
            'attendees_range': (300, 600)
        },
        {
            'title': 'MSE-NE Fair',
            'description': 'Material Science and Nuclear Engineering career fair. Connect with industry leaders in advanced materials and energy.',
            'tags': ['Engineering', 'Materials Science', 'Nuclear', 'Career'],
            'attendees_range': (150, 300)
        },
        {
            'title': 'Preview/Orientation Sessions - Summer',
            'description': 'Campus preview for incoming freshmen and transfer students. Tour campus, meet advisors, and register for classes.',
            'tags': ['Orientation', 'New Students', 'Preview', 'Campus Tour'],
            'attendees_range': (200, 400)
        },
        {
            'title': 'Transfer Preview',
            'description': 'Special orientation for transfer students. Learn about transfer credit, housing, and resources specific to transfer students.',
            'tags': ['Transfer', 'Orientation', 'New Students', 'Academic'],
            'attendees_range': (100, 200)
        },
        {
            'title': 'Graduate Student Orientation',
            'description': 'Welcome orientation for new graduate students. Meet faculty, learn about research opportunities, and connect with peers.',
            'tags': ['Graduate', 'Orientation', 'Research', 'Academic'],
            'attendees_range': (150, 300)
        },
        {
            'title': 'First Year Florida Course Introduction',
            'description': 'Informational session about First Year Florida courses designed to help new students transition to college life.',
            'tags': ['First Year', 'Academic', 'Course', 'New Students'],
            'attendees_range': (50, 100)
        },
        {
            'title': 'Career Ready Workshops',
            'description': 'Series of workshops on resume writing, interview skills, networking, and professional development.',
            'tags': ['Workshop', 'Career', 'Professional Development', 'Skills'],
            'attendees_range': (30, 80)
        },
        {
            'title': 'Professional U Workshop Series',
            'description': 'Professional development program covering business etiquette, communication skills, and workplace success.',
            'tags': ['Professional', 'Workshop', 'Career', 'Development'],
            'attendees_range': (25, 60)
        },
        {
            'title': 'Express Drop-In Career Advising',
            'description': 'Quick 15-minute career advising sessions. No appointment needed. Get resume feedback and career guidance.',
            'tags': ['Career', 'Advising', 'Drop-In', 'Professional'],
            'attendees_range': (20, 50)
        },
        {
            'title': 'Research Symposium',
            'description': 'Showcase of undergraduate and graduate research across all disciplines. Poster presentations and oral sessions.',
            'tags': ['Research', 'Academic', 'Symposium', 'Presentation'],
            'attendees_range': (200, 400)
        },
        {
            'title': 'Thesis Defense - Graduate Student',
            'description': 'Public doctoral dissertation defense. Graduate student presents research findings to committee and audience.',
            'tags': ['Research', 'Graduate', 'Defense', 'Academic'],
            'attendees_range': (10, 30)
        },
    ],

    'Cultural': [
        # Homecoming & Tradition Events
        {
            'title': 'Gator Growl',
            'description': 'Nation\'s largest student-run pep rally! Comedy acts, musical performances, and Gator spirit before the Homecoming game.',
            'tags': ['Homecoming', 'Tradition', 'Pep Rally', 'Entertainment'],
            'attendees_range': (10000, 20000)
        },
        {
            'title': 'Homecoming Parade',
            'description': 'Annual Homecoming parade through campus and downtown Gainesville. Floats, bands, and Gator pride!',
            'tags': ['Homecoming', 'Parade', 'Tradition', 'Spirit'],
            'attendees_range': (5000, 10000)
        },
        {
            'title': 'Homecoming Festival - Plaza of the Americas',
            'description': 'Festival on the Plaza featuring food, music, games, and student organization booths. Celebrate Gator Homecoming!',
            'tags': ['Homecoming', 'Festival', 'Food', 'Music'],
            'attendees_range': (3000, 6000)
        },
        {
            'title': 'Homecoming Pageant',
            'description': 'Showcase of talent, poise, and Gator spirit. Students compete for Homecoming Court titles.',
            'tags': ['Homecoming', 'Pageant', 'Competition', 'Talent'],
            'attendees_range': (500, 1000)
        },
        {
            'title': 'Gator Gallop 2-Mile Fun Run',
            'description': 'Homecoming week 2-mile fun run/walk. All fitness levels welcome. Orange and blue encouraged!',
            'tags': ['Homecoming', 'Running', 'Fitness', 'Fun Run'],
            'attendees_range': (200, 500)
        },
        {
            'title': 'Soulfest - Multicultural Showcase',
            'description': 'Celebration of diversity through music, dance, and cultural performances during Homecoming week.',
            'tags': ['Homecoming', 'Cultural', 'Diversity', 'Performance'],
            'attendees_range': (400, 800)
        },
        {
            'title': 'International Education Week',
            'description': 'Week-long celebration of international education and cultural exchange. Events, exhibits, and performances.',
            'tags': ['International', 'Education', 'Cultural', 'Global'],
            'attendees_range': (300, 600)
        },
        {
            'title': 'Culture Showcase',
            'description': 'Student organizations present cultural performances, food, and traditions from around the world.',
            'tags': ['Cultural', 'Performance', 'International', 'Diversity'],
            'attendees_range': (400, 800)
        },
        {
            'title': 'International Tea Time',
            'description': 'Weekly informal gathering for international and domestic students. Share cultures over tea and snacks.',
            'tags': ['International', 'Social', 'Cultural Exchange', 'Tea'],
            'attendees_range': (20, 50)
        },
        {
            'title': 'Heritage Month Celebration',
            'description': 'Monthly celebrations honoring various cultural heritages. Includes Hispanic, Black, Asian, and Native American heritage months.',
            'tags': ['Heritage', 'Cultural', 'Diversity', 'Celebration'],
            'attendees_range': (200, 500)
        },
        {
            'title': 'Study Abroad Passport Day',
            'description': 'Learn about study abroad opportunities worldwide. Passport photos available on-site.',
            'tags': ['Study Abroad', 'International', 'Travel', 'Education'],
            'attendees_range': (150, 300)
        },
        {
            'title': 'Global Gators Networking Event',
            'description': 'Connect with students who have studied abroad and learn about international opportunities.',
            'tags': ['International', 'Study Abroad', 'Networking', 'Global'],
            'attendees_range': (100, 200)
        },
    ],

    'Social': [
        # Orientation & Welcome Events
        {
            'title': 'Great Gator Welcome - Fall',
            'description': 'Kickoff event for new students! Activities, entertainment, and resources to start your Gator journey.',
            'tags': ['Welcome', 'New Students', 'Orientation', 'Activities'],
            'attendees_range': (2000, 4000)
        },
        {
            'title': 'GatorNights - Weekly Friday Events',
            'description': 'Free late-night programming every Friday! Movies, games, food, and entertainment.',
            'tags': ['Entertainment', 'Free', 'Games', 'Social'],
            'attendees_range': (300, 800)
        },
        {
            'title': 'Student Organization Fair - Fall',
            'description': 'Explore 1000+ student organizations! Find your community and get involved on campus.',
            'tags': ['Organizations', 'Involvement', 'Fair', 'Clubs'],
            'attendees_range': (3000, 6000)
        },
        {
            'title': 'Student Organization Fair - Spring',
            'description': 'Spring semester involvement fair. Join clubs, meet new people, and discover opportunities.',
            'tags': ['Organizations', 'Involvement', 'Fair', 'Clubs'],
            'attendees_range': (2000, 4000)
        },
        {
            'title': 'New Student Convocation',
            'description': 'Official welcome ceremony for new Gators. University leaders address incoming class.',
            'tags': ['Ceremony', 'Welcome', 'New Students', 'Tradition'],
            'attendees_range': (4000, 6000)
        },
        {
            'title': 'Family Weekend',
            'description': 'Welcome families to campus! Campus tours, activities, and opportunities to meet faculty.',
            'tags': ['Family', 'Weekend', 'Campus', 'Activities'],
            'attendees_range': (1000, 2000)
        },
        {
            'title': 'Always Orange Forever Blue Event',
            'description': 'Alumni networking event connecting current students with UF graduates.',
            'tags': ['Alumni', 'Networking', 'Social', 'Professional'],
            'attendees_range': (200, 400)
        },
        {
            'title': 'Reitz Union Game Room Tournament',
            'description': 'Billiards, bowling, and gaming tournaments. Compete for prizes and bragging rights!',
            'tags': ['Games', 'Tournament', 'Competition', 'Entertainment'],
            'attendees_range': (50, 150)
        },
        {
            'title': 'Campus Movie Night',
            'description': 'Free outdoor movie screening on the Plaza. Bring blankets and friends!',
            'tags': ['Movie', 'Free', 'Outdoor', 'Entertainment'],
            'attendees_range': (300, 600)
        },
        {
            'title': 'Late-Night Programming',
            'description': 'After-hours activities, snacks, and stress relief during finals week.',
            'tags': ['Late Night', 'Finals', 'Stress Relief', 'Activities'],
            'attendees_range': (200, 500)
        },
    ],

    'Sports': [
        # Athletics Events
        {
            'title': 'Gators Football vs SEC Opponent',
            'description': 'Home football game at The Swamp! One of the most intimidating venues in college football. Go Gators!',
            'tags': ['Football', 'Game Day', 'SEC', 'Athletics'],
            'attendees_range': (85000, 90000)
        },
        {
            'title': 'Pre-Game Tailgate Party',
            'description': 'Tailgate before the big game! Food, music, and Gator spirit. Start your game day right!',
            'tags': ['Tailgate', 'Football', 'Social', 'Game Day'],
            'attendees_range': (10000, 20000)
        },
        {
            'title': 'Gator Walk',
            'description': 'Watch the team walk into the stadium 2 hours before kickoff. Show your support!',
            'tags': ['Football', 'Tradition', 'Game Day', 'Spirit'],
            'attendees_range': (2000, 5000)
        },
        {
            'title': 'Men\'s Basketball Game',
            'description': 'Gators basketball at the O\'Connell Center. Fast-paced action and rowdy student section!',
            'tags': ['Basketball', 'Game', 'Athletics', 'Student Section'],
            'attendees_range': (8000, 12000)
        },
        {
            'title': 'Women\'s Basketball Game',
            'description': 'Support the Lady Gators! Exciting basketball in a great atmosphere.',
            'tags': ['Basketball', 'Women\'s Sports', 'Game', 'Athletics'],
            'attendees_range': (3000, 5000)
        },
        {
            'title': 'Volleyball Match',
            'description': 'Gators volleyball in the O\'Dome. High-energy matches and passionate fans!',
            'tags': ['Volleyball', 'Game', 'Athletics', 'Women\'s Sports'],
            'attendees_range': (2000, 4000)
        },
        {
            'title': 'Gymnastics Meet',
            'description': 'Watch the nationally-ranked Gators gymnastics team compete. Incredible athleticism!',
            'tags': ['Gymnastics', 'Competition', 'Athletics', 'Women\'s Sports'],
            'attendees_range': (5000, 8000)
        },
        {
            'title': 'Baseball Game at Florida Ballpark',
            'description': 'Gators baseball under the lights! One of the best college baseball programs in the nation.',
            'tags': ['Baseball', 'Game', 'Athletics', 'Outdoor'],
            'attendees_range': (3000, 6000)
        },
        {
            'title': 'Softball Game',
            'description': 'Support the Gators softball team! Fast-pitch action at one of the top programs.',
            'tags': ['Softball', 'Game', 'Athletics', 'Women\'s Sports'],
            'attendees_range': (1500, 3000)
        },
        {
            'title': 'Soccer Match',
            'description': 'Gators soccer at Pressly Stadium. Exciting matches in a beautiful setting.',
            'tags': ['Soccer', 'Game', 'Athletics', 'Outdoor'],
            'attendees_range': (1000, 2000)
        },
        {
            'title': 'Swimming & Diving Meet',
            'description': 'Watch the Gators swim team compete. Multiple Olympic athletes on the roster!',
            'tags': ['Swimming', 'Diving', 'Competition', 'Athletics'],
            'attendees_range': (800, 1500)
        },
        {
            'title': 'Track & Field Meet',
            'description': 'Outdoor track and field competition. Sprint, jump, and throw events.',
            'tags': ['Track', 'Field', 'Athletics', 'Outdoor'],
            'attendees_range': (500, 1000)
        },
        {
            'title': 'Tennis Match',
            'description': 'Gators tennis at the Ring Tennis Complex. Watch future pros compete!',
            'tags': ['Tennis', 'Match', 'Athletics', 'Outdoor'],
            'attendees_range': (300, 600)
        },
        {
            'title': 'Intramural Sports Championship',
            'description': 'Championship games for various intramural sports. Students compete for glory!',
            'tags': ['Intramural', 'Sports', 'Competition', 'Students'],
            'attendees_range': (100, 300)
        },
        {
            'title': 'Outdoor Recreation Trip - Kayaking',
            'description': 'Guided kayaking trip to nearby springs. Equipment and transportation provided.',
            'tags': ['Outdoor', 'Recreation', 'Kayaking', 'Adventure'],
            'attendees_range': (15, 30)
        },
        {
            'title': 'Campus Rec 5K Run',
            'description': 'Recreational 5K run around campus. All paces welcome!',
            'tags': ['Running', '5K', 'Fitness', 'Recreation'],
            'attendees_range': (100, 250)
        },
        {
            'title': 'Wellness Workshop - Yoga & Meditation',
            'description': 'Free yoga and meditation session. Reduce stress and improve wellness.',
            'tags': ['Wellness', 'Yoga', 'Meditation', 'Health'],
            'attendees_range': (20, 50)
        },
    ],
}

# Greek Life Events
GREEK_EVENTS = [
    {
        'title': 'IFC Fall Recruitment',
        'description': 'Interfraternity Council fall recruitment week. Meet UF fraternities and find your brotherhood.',
        'category': 'Social',
        'tags': ['Greek Life', 'Recruitment', 'Fraternity', 'Social'],
        'attendees_range': (800, 1500)
    },
    {
        'title': 'Panhellenic Sorority Recruitment',
        'description': 'Formal sorority recruitment. Join one of UF\'s Panhellenic sororities and find your sisterhood.',
        'category': 'Social',
        'tags': ['Greek Life', 'Recruitment', 'Sorority', 'Social'],
        'attendees_range': (1200, 2000)
    },
    {
        'title': 'NPHC Convocation',
        'description': 'National Pan-Hellenic Council informational and cultural celebration.',
        'category': 'Cultural',
        'tags': ['Greek Life', 'NPHC', 'Cultural', 'Diversity'],
        'attendees_range': (200, 400)
    },
    {
        'title': 'MGC Showcase',
        'description': 'Multicultural Greek Council showcase of diverse Greek organizations.',
        'category': 'Cultural',
        'tags': ['Greek Life', 'MGC', 'Multicultural', 'Diversity'],
        'attendees_range': (150, 300)
    },
    {
        'title': 'Greek Week Competition',
        'description': 'Week of competitions between Greek organizations. Philanthropy, athletics, and spirit!',
        'category': 'Social',
        'tags': ['Greek Life', 'Competition', 'Philanthropy', 'Spirit'],
        'attendees_range': (1000, 2000)
    },
    {
        'title': 'Greek Philanthropy Event',
        'description': 'Fundraising event supporting a charitable cause. Greek organizations give back to the community.',
        'category': 'Social',
        'tags': ['Greek Life', 'Philanthropy', 'Charity', 'Community Service'],
        'attendees_range': (200, 500)
    },
]

# Arts & Performance Events
ARTS_EVENTS = [
    {
        'title': 'UF Performing Arts - Broadway Series',
        'description': 'Touring Broadway production at the Phillips Center. Professional theater at its finest!',
        'category': 'Cultural',
        'tags': ['Theatre', 'Performance', 'Arts', 'Broadway'],
        'attendees_range': (800, 1200)
    },
    {
        'title': 'UF Symphony Orchestra Concert',
        'description': 'Full orchestra performing classical masterworks. Free admission for students!',
        'category': 'Cultural',
        'tags': ['Music', 'Orchestra', 'Classical', 'Performance'],
        'attendees_range': (300, 600)
    },
    {
        'title': 'Jazz Band Concert',
        'description': 'UF Jazz Bands perform big band classics and modern jazz. Swing night!',
        'category': 'Cultural',
        'tags': ['Music', 'Jazz', 'Performance', 'Concert'],
        'attendees_range': (200, 400)
    },
    {
        'title': 'Opera Scenes Performance',
        'description': 'Opera students perform famous opera scenes. Beautiful voices and dramatic performances.',
        'category': 'Cultural',
        'tags': ['Opera', 'Music', 'Performance', 'Classical'],
        'attendees_range': (150, 300)
    },
    {
        'title': 'Theatre Production - Student Show',
        'description': 'Student-directed and performed theatrical production. Support student artists!',
        'category': 'Cultural',
        'tags': ['Theatre', 'Performance', 'Students', 'Arts'],
        'attendees_range': (100, 250)
    },
    {
        'title': 'Dance Company Performance',
        'description': 'UF Dance Company showcases contemporary, modern, and ballet pieces.',
        'category': 'Cultural',
        'tags': ['Dance', 'Performance', 'Arts', 'Contemporary'],
        'attendees_range': (200, 400)
    },
    {
        'title': 'Harn Museum Exhibition Opening',
        'description': 'New art exhibition opening at the Harn Museum. Meet the artists and view new collections.',
        'category': 'Cultural',
        'tags': ['Art', 'Museum', 'Exhibition', 'Visual Arts'],
        'attendees_range': (100, 300)
    },
    {
        'title': 'Student Recital - Music School',
        'description': 'Music students perform solo and chamber music recitals. Show your support!',
        'category': 'Cultural',
        'tags': ['Music', 'Recital', 'Performance', 'Students'],
        'attendees_range': (30, 80)
    },
    {
        'title': 'Pipe Organ Concert',
        'description': 'Concert on the historic pipe organ at University Auditorium. Majestic music!',
        'category': 'Cultural',
        'tags': ['Music', 'Organ', 'Classical', 'Concert'],
        'attendees_range': (100, 200)
    },
    {
        'title': 'Choral Concert',
        'description': 'UF choirs perform choral masterworks. Angelic voices in harmony!',
        'category': 'Cultural',
        'tags': ['Music', 'Choir', 'Choral', 'Performance'],
        'attendees_range': (200, 400)
    },
]

# Science & Museum Events
SCIENCE_EVENTS = [
    {
        'title': 'Florida Museum of Natural History - Special Exhibit',
        'description': 'New exhibit at the Florida Museum. Explore natural history and cultural heritage.',
        'category': 'Academic',
        'tags': ['Museum', 'Science', 'Education', 'Exhibit'],
        'attendees_range': (200, 500)
    },
    {
        'title': 'Butterfly Rainforest Visit',
        'description': 'Experience hundreds of live butterflies in the Butterfly Rainforest. Beautiful and educational!',
        'category': 'Academic',
        'tags': ['Museum', 'Science', 'Nature', 'Educational'],
        'attendees_range': (100, 300)
    },
]

class UFEventGenerator:
    def __init__(self):
        self.locations = UF_LOCATIONS
        self.all_templates = []

        # Combine all event templates
        for category, templates in UF_EVENT_TEMPLATES.items():
            for template in templates:
                template['category'] = category
                self.all_templates.append(template)

        # Add Greek events
        for event in GREEK_EVENTS:
            self.all_templates.append(event)

        # Add Arts events
        for event in ARTS_EVENTS:
            self.all_templates.append(event)

        # Add Science events
        for event in SCIENCE_EVENTS:
            self.all_templates.append(event)

    def generate_semester_events(self, num_events=50):
        """Generate events for a semester (diverse selection)"""
        events = []
        event_id = 1

        # Randomly sample events to create variety
        selected_templates = random.sample(self.all_templates, min(num_events, len(self.all_templates)))

        for template in selected_templates:
            # Pick appropriate location based on event type
            location = self._select_location_for_event(template)

            # Generate random time (within next 60 days for semester)
            days_ahead = random.randint(0, 60)
            hour = self._select_hour_for_event(template)
            start_time = datetime.now() + timedelta(days=days_ahead, hours=hour - datetime.now().hour)
            start_time = start_time.replace(minute=random.choice([0, 15, 30]), second=0, microsecond=0)

            # Duration based on event type
            duration_hours = self._select_duration_for_event(template)
            end_time = start_time + timedelta(hours=duration_hours)

            event = {
                'id': event_id,
                'title': template['title'],
                'description': template['description'],
                'category': template['category'],
                'tags': template['tags'],
                'location_name': location['name'],
                'location_id': location['id'],
                'start_time': start_time,
                'end_time': end_time,
                'organizer': self._get_organizer_for_event(template),
                'attendees_expected': random.randint(template['attendees_range'][0], template['attendees_range'][1]),
                'is_free': self._is_free_event(template),
                'registration_required': self._requires_registration(template)
            }

            events.append(event)
            event_id += 1

        # Sort by start time
        events.sort(key=lambda x: x['start_time'])
        return events

    def _select_location_for_event(self, template):
        """Select appropriate location based on event type"""
        title_lower = template['title'].lower()

        # Stadium events
        if 'football' in title_lower or 'gator walk' in title_lower or 'tailgate' in title_lower:
            return next((loc for loc in self.locations if 'Stadium' in loc['name']), self.locations[0])

        # Career fairs - large venues
        if 'career' in title_lower or 'fair' in title_lower:
            return next((loc for loc in self.locations if 'Reitz' in loc['name']), self.locations[0])

        # Athletic events
        if any(sport in title_lower for sport in ['basketball', 'volleyball', 'gymnastics']):
            return next((loc for loc in self.locations if 'Rec' in loc['name']), self.locations[0])

        # Outdoor events
        if 'outdoor' in title_lower or 'plaza' in title_lower or 'parade' in title_lower:
            return next((loc for loc in self.locations if 'Plaza' in loc['name'] or 'Norman' in loc['name']), self.locations[0])

        # Academic events
        if template['category'] == 'Academic':
            academic_locations = [loc for loc in self.locations if loc['category'] in ['ACADEMIC', 'LIBRARIES']]
            return random.choice(academic_locations) if academic_locations else self.locations[0]

        # Social events
        if template['category'] == 'Social':
            social_locations = [loc for loc in self.locations if loc['category'] in ['STUDY SPOTS', 'DINING']]
            return random.choice(social_locations) if social_locations else self.locations[0]

        # Default to Reitz Union
        return next((loc for loc in self.locations if 'Reitz' in loc['name']), self.locations[0])

    def _select_hour_for_event(self, template):
        """Select appropriate hour based on event type"""
        title_lower = template['title'].lower()

        if 'football' in title_lower:
            return random.choice([12, 15, 19])  # Noon, 3pm, or 7pm games
        elif 'gator walk' in title_lower:
            return random.choice([10, 13, 17])  # 2 hours before games
        elif 'tailgate' in title_lower:
            return random.choice([9, 12, 16])
        elif 'night' in title_lower or 'evening' in title_lower:
            return random.randint(18, 21)
        elif 'breakfast' in title_lower or 'morning' in title_lower:
            return random.randint(8, 10)
        elif 'career' in title_lower or 'fair' in title_lower:
            return random.randint(10, 14)
        else:
            return random.randint(10, 18)

    def _select_duration_for_event(self, template):
        """Select appropriate duration based on event type"""
        title_lower = template['title'].lower()

        if 'football' in title_lower:
            return 3.5
        elif 'fair' in title_lower or 'showcase' in title_lower:
            return random.choice([3, 4, 5])
        elif 'workshop' in title_lower:
            return random.choice([1.5, 2, 3])
        elif 'concert' in title_lower or 'performance' in title_lower:
            return random.choice([1.5, 2])
        elif 'defense' in title_lower:
            return 1.5
        elif 'basketball' in title_lower or 'volleyball' in title_lower:
            return 2
        else:
            return random.choice([1, 1.5, 2, 2.5])

    def _get_organizer_for_event(self, template):
        """Get organizer based on event type"""
        category = template['category']
        title_lower = template['title'].lower()

        if 'career' in title_lower:
            return 'Career Connections Center'
        elif category == 'Sports' or 'athletic' in title_lower:
            return 'UF Athletics'
        elif 'greek' in title_lower:
            return 'Greek Life Office'
        elif 'homecoming' in title_lower:
            return 'Homecoming Committee'
        elif 'international' in title_lower:
            return 'International Center'
        elif any(word in title_lower for word in ['concert', 'performance', 'recital', 'orchestra']):
            return 'UF School of Music'
        elif 'museum' in title_lower:
            return 'Florida Museum of Natural History'
        elif 'orientation' in title_lower:
            return 'New Student & Family Programs'
        elif category == 'Academic':
            return random.choice(['Graduate School', 'Academic Advising', 'Student Affairs', 'Career Center'])
        elif category == 'Cultural':
            return random.choice(['Multicultural Affairs', 'International Center', 'Cultural Organizations'])
        else:
            return 'Student Activities'

    def _is_free_event(self, template):
        """Determine if event is free"""
        title_lower = template['title'].lower()

        # Most student events are free
        if any(word in title_lower for word in ['gator', 'student', 'orientation', 'fair', 'workshop']):
            return True
        # Ticketed events
        elif any(word in title_lower for word in ['football', 'basketball', 'broadway', 'concert']):
            return random.choice([False, True])  # Some are free for students
        else:
            return random.choice([True, True, True, False])  # 75% free

    def _requires_registration(self, template):
        """Determine if registration is required"""
        title_lower = template['title'].lower()

        if any(word in title_lower for word in ['fair', 'showcase', 'game', 'concert', 'parade']):
            return False
        elif any(word in title_lower for word in ['workshop', 'orientation', 'trip', 'recruitment']):
            return True
        else:
            return random.choice([True, False])

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

# Expanded training data for better classifier performance
TRAINING_EVENTS = []

# Generate comprehensive training data from templates
for category, templates in UF_EVENT_TEMPLATES.items():
    for template in templates:
        TRAINING_EVENTS.append((template['title'], template['description'], category))

# Add Greek events to training
for event in GREEK_EVENTS:
    TRAINING_EVENTS.append((event['title'], event['description'], event['category']))

# Add Arts events to training
for event in ARTS_EVENTS:
    TRAINING_EVENTS.append((event['title'], event['description'], event['category']))

# Add Science events to training
for event in SCIENCE_EVENTS:
    TRAINING_EVENTS.append((event['title'], event['description'], event['category']))

# Additional training variations for better model performance
ADDITIONAL_TRAINING = [
    # More Academic examples
    ("Graduate Research Presentation", "PhD students present dissertation research findings", "Academic"),
    ("Undergraduate Research Expo", "Showcase of undergraduate research projects across disciplines", "Academic"),
    ("Study Skills Workshop", "Learn effective study techniques and time management", "Academic"),
    ("Honors Thesis Presentation", "Honors students present capstone research projects", "Academic"),
    ("Academic Advising Session", "Meet with advisors to plan your academic path", "Academic"),

    # More Social examples
    ("Game Night at Reitz", "Board games, video games, and fun with friends", "Social"),
    ("Trivia Competition", "Test your knowledge and win prizes in team trivia", "Social"),
    ("Comedy Show", "Stand-up comedy night featuring student comedians", "Social"),
    ("Karaoke Night", "Sing your favorite songs with friends", "Social"),
    ("Paint and Sip", "Creative painting session with refreshments", "Social"),

    # More Sports examples
    ("Intramural Soccer Finals", "Championship match for intramural soccer league", "Sports"),
    ("Rec Center Fitness Class", "Group fitness class - all levels welcome", "Sports"),
    ("Ultimate Frisbee Tournament", "Compete in ultimate frisbee competition", "Sports"),
    ("Marathon Training Run", "Group training run for upcoming marathon", "Sports"),
    ("Climbing Wall Competition", "Test your climbing skills in friendly competition", "Sports"),

    # More Cultural examples
    ("Chinese New Year Celebration", "Ring in the lunar new year with performances and food", "Cultural"),
    ("African Dance Workshop", "Learn traditional African dance moves", "Cultural"),
    ("International Film Festival", "Screening of award-winning international films", "Cultural"),
    ("Language Exchange Meetup", "Practice foreign languages with native speakers", "Cultural"),
    ("World Music Concert", "Musicians perform traditional music from around the globe", "Cultural"),
]

TRAINING_EVENTS.extend(ADDITIONAL_TRAINING)
