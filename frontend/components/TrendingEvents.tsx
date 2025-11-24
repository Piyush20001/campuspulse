import { Heart, Users } from "lucide-react";
import { ImageWithFallback } from "./figma/ImageWithFallback";
import { useState } from "react";

interface Event {
  id: number;
  title: string;
  day: string;
  time: string;
  interested: number;
  posterUrl: string;
}

const trendingEvents: Event[] = [
  {
    id: 1,
    title: "Gator Growl Comedy Show",
    day: "WED",
    time: "10 AM",
    interested: 88,
    posterUrl: "https://images.unsplash.com/photo-1623253489134-8096e1d64f50?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2xsZWdlJTIwc3R1ZGVudHMlMjBldmVudCUyMHBvc3RlcnxlbnwxfHx8fDE3NjM0OTQ3ODF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
  },
  {
    id: 2,
    title: "Football Game Tailgate",
    day: "TUE",
    time: "9 PM",
    interested: 100,
    posterUrl: "https://images.unsplash.com/photo-1623253489134-8096e1d64f50?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2xsZWdlJTIwc3R1ZGVudHMlMjBldmVudCUyMHBvc3RlcnxlbnwxfHx8fDE3NjM0OTQ3ODF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
  },
  {
    id: 3,
    title: "Engineering Career Fair",
    day: "THU",
    time: "2 PM",
    interested: 145,
    posterUrl: "https://images.unsplash.com/photo-1623253489134-8096e1d64f50?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2xsZWdlJTIwc3R1ZGVudHMlMjBldmVudCUyMHBvc3RlcnxlbnwxfHx8fDE3NjM0OTQ3ODF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
  },
  {
    id: 4,
    title: "Live Music @ Turlington",
    day: "FRI",
    time: "6 PM",
    interested: 67,
    posterUrl: "https://images.unsplash.com/photo-1623253489134-8096e1d64f50?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxjb2xsZWdlJTIwc3R1ZGVudHMlMjBldmVudCUyMHBvc3RlcnxlbnwxfHx8fDE3NjM0OTQ3ODF8MA&ixlib=rb-4.1.0&q=80&w=1080&utm_source=figma&utm_medium=referral",
  },
];

export function TrendingEvents() {
  const [interestedEvents, setInterestedEvents] = useState<Set<number>>(new Set());

  const toggleInterested = (eventId: number) => {
    setInterestedEvents(prev => {
      const newSet = new Set(prev);
      if (newSet.has(eventId)) {
        newSet.delete(eventId);
      } else {
        newSet.add(eventId);
      }
      return newSet;
    });
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-16">
      <h2 className="mb-6 text-white">Trending Events</h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {trendingEvents.map((event) => (
          <div
            key={event.id}
            className="bg-gray-900 rounded-lg shadow-xl overflow-hidden hover:shadow-2xl transition-shadow cursor-pointer border border-gray-800 hover:border-gray-700"
          >
            {/* Event Poster */}
            <div className="relative aspect-[3/4] bg-gradient-to-br from-orange-400 to-orange-600">
              <ImageWithFallback
                src={event.posterUrl}
                alt={event.title}
                className="w-full h-full object-cover"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent"></div>
              <div className="absolute bottom-0 left-0 right-0 p-4">
                <h3 className="text-white">{event.title}</h3>
              </div>
            </div>

            {/* Event Details */}
            <div className="p-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-gray-400 text-sm">{event.day}</div>
                  <div className="text-gray-200">{event.time}</div>
                </div>
                <div className="flex items-center gap-1 text-gray-400">
                  <Users className="h-4 w-4" />
                  <span className="text-sm">{event.interested} interested</span>
                </div>
              </div>
              <button className="w-full mt-3 flex items-center justify-center gap-2 px-4 py-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-gray-200"
                onClick={() => toggleInterested(event.id)}
              >
                <Heart 
                  className={`h-4 w-4 transition-all ${
                    interestedEvents.has(event.id) 
                      ? 'fill-red-500 text-red-500' 
                      : ''
                  }`} 
                />
                <span className="text-sm">Interested</span>
              </button>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}