import { Search, ChevronDown, Heart, Ticket, Users, MapPin, Calendar } from "lucide-react";
import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { Input } from "./ui/input";
import { Badge } from "./ui/badge";
import { useState } from "react";

interface Event {
  id: number;
  title: string;
  date: string;
  time: string;
  location: string;
  category: string;
  interested: number;
  cost: string;
  description?: string;
}

const events: Event[] = [
  {
    id: 1,
    title: "TONIGHT: Gators vs Samford",
    date: "Tue, 7-9 PM",
    time: "7:00 PM",
    location: "Exacta Arena",
    category: "Sports",
    interested: 832,
    cost: "Tickets",
  },
  {
    id: 2,
    title: "Machine Learning Intro Workshop",
    date: "Wed, 4-6 PM",
    time: "4:00 PM",
    location: "CSE 220",
    category: "Academic",
    interested: 145,
    cost: "Free",
  },
  {
    id: 3,
    title: "Campus Art Exhibition Opening",
    date: "Thu, 6-8 PM",
    time: "6:00 PM",
    location: "Harn Museum",
    category: "Arts",
    interested: 234,
    cost: "Free",
  },
  {
    id: 4,
    title: "Career Fair: Tech Companies",
    date: "Fri, 10 AM-4 PM",
    time: "10:00 AM",
    location: "Reitz Union",
    category: "Career",
    interested: 1205,
    cost: "Free",
  },
];

const filterOptions = [
  {
    label: "Popularity",
    options: ["Trending", "Highly Anticipated", "Newly Posted", "Near Capacity"],
  },
  {
    label: "Category",
    options: ["Academic/Career", "Social", "Sports & Fitness", "Arts/Performance", "Clubs/Organisations", "Volunteering/Charity", "Admin/Official", "Food"],
  },
  {
    label: "Type",
    options: ["Workshop", "Meeting", "Performance", "Social Hangout", "Competition", "Career Event", "Miscellaneous"],
  },
  {
    label: "Cost",
    options: ["Free", "Ticketed"],
  },
  {
    label: "Date",
    options: ["Today", "Tomorrow", "This Week", "This Month"],
  },
  {
    label: "Time",
    options: ["Morning", "Afternoon", "Evening", "Night"],
  },
  {
    label: "Organiser",
    options: ["Clubs", "UF Departments", "Student Orgs", "Greek Life", "Athletics"],
  },
  {
    label: "Size",
    options: ["Small (10-30)", "Medium (30-100)", "Large (100+)"],
  },
];

export function EventsPage() {
  const [interestedEvents, setInterestedEvents] = useState<Set<number>>(new Set());
  const [openDropdown, setOpenDropdown] = useState<string | null>(null);

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
    <div className="min-h-screen bg-gray-950 pt-20">
      {/* Browse By Filter Bar */}
      <div className="bg-gray-900/80 border-b border-gray-800 sticky top-16 z-30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <span className="text-gray-400 whitespace-nowrap text-xs uppercase tracking-wide">BROWSE BY</span>
            
            {/* Filter Dropdowns */}
            <div className="flex items-center gap-2 flex-1 overflow-x-auto">
              {filterOptions.map((filter) => (
                <DropdownMenu 
                  key={filter.label}
                  open={openDropdown === filter.label}
                  onOpenChange={(isOpen) => setOpenDropdown(isOpen ? filter.label : null)}
                >
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="outline"
                      className="gap-1 bg-gray-800/50 border-gray-700 text-gray-300 hover:bg-gray-700 hover:text-white text-xs uppercase tracking-wide px-3 py-1.5 h-auto whitespace-nowrap flex-shrink-0"
                      onMouseEnter={() => setOpenDropdown(filter.label)}
                      onMouseLeave={() => setOpenDropdown(null)}
                    >
                      {filter.label}
                      <ChevronDown className="h-3 w-3" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent 
                    align="start"
                    className="bg-gray-800 border-gray-700 text-gray-200 min-w-[180px] z-50"
                    onMouseEnter={() => setOpenDropdown(filter.label)}
                    onMouseLeave={() => setOpenDropdown(null)}
                  >
                    {filter.options.map((option) => (
                      <DropdownMenuItem
                        key={option}
                        className="hover:bg-gray-700 cursor-pointer text-sm text-gray-200"
                      >
                        {option}
                      </DropdownMenuItem>
                    ))}
                  </DropdownMenuContent>
                </DropdownMenu>
              ))}
            </div>

            {/* Search */}
            <div className="flex items-center gap-3 flex-shrink-0">
              <span className="text-gray-400 whitespace-nowrap text-xs uppercase tracking-wide">FIND AN EVENT</span>
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-500" />
                <Input
                  placeholder="Search events..."
                  className="pl-10 bg-gray-800/50 border-gray-700 text-gray-200 placeholder:text-gray-500 w-64"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar */}
          <div className="lg:col-span-1 space-y-6">
            {/* Popular Section */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-4">
              <h3 className="text-white mb-4">Popular</h3>
              <div className="space-y-3">
                {events.slice(0, 2).map((event) => (
                  <div
                    key={event.id}
                    className="p-3 bg-gray-800/50 rounded border border-gray-700 hover:border-blue-500/50 cursor-pointer transition-all"
                  >
                    <div className="text-gray-200 text-sm mb-1">{event.title}</div>
                    <div className="flex items-center gap-2 text-xs text-gray-400">
                      <Users className="h-3 w-3" />
                      {event.interested}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* This Week Section */}
            <div className="bg-gray-900/50 border border-gray-800 rounded-lg p-4">
              <h3 className="text-white mb-4">This Week</h3>
              <div className="space-y-3">
                {events.slice(2, 4).map((event) => (
                  <div
                    key={event.id}
                    className="p-3 bg-gray-800/50 rounded border border-gray-700 hover:border-blue-500/50 cursor-pointer transition-all"
                  >
                    <div className="text-gray-200 text-sm mb-1">{event.title}</div>
                    <div className="flex items-center gap-2 text-xs text-gray-400">
                      <Users className="h-3 w-3" />
                      {event.interested}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Event Cards Grid */}
          <div className="lg:col-span-3">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {events.map((event) => (
                <div
                  key={event.id}
                  className="bg-gray-900/50 border border-gray-800 rounded-lg p-6 hover:border-blue-500/50 transition-all group"
                >
                  {/* Category Badge */}
                  <Badge className="mb-3 bg-blue-500/20 text-blue-300 border-blue-500/40">
                    {event.category}
                  </Badge>

                  {/* Event Title */}
                  <h3 className="text-white mb-4 group-hover:text-blue-300 transition-colors">
                    {event.title}
                  </h3>

                  {/* Event Details */}
                  <div className="space-y-2 mb-4">
                    <div className="flex items-center gap-2 text-gray-400 text-sm">
                      <Calendar className="h-4 w-4" />
                      {event.date}
                    </div>
                    <div className="flex items-center gap-2 text-gray-400 text-sm">
                      <MapPin className="h-4 w-4" />
                      {event.location}
                    </div>
                    <div className="flex items-center gap-2 text-gray-400 text-sm">
                      <Users className="h-4 w-4" />
                      {event.interested} interested
                    </div>
                    <div className="flex items-center gap-2 text-gray-400 text-sm">
                      <Ticket className="h-4 w-4" />
                      {event.cost}
                    </div>
                  </div>

                  {/* Interested Button */}
                  <Button
                    className="w-full bg-transparent border border-blue-500/40 text-blue-300 hover:bg-blue-500/10 hover:border-blue-500 transition-all"
                    onClick={() => toggleInterested(event.id)}
                  >
                    <Heart 
                      className={`h-4 w-4 mr-2 transition-all ${
                        interestedEvents.has(event.id) 
                          ? 'fill-red-500 text-red-500' 
                          : ''
                      }`}
                    />
                    Interested
                  </Button>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}