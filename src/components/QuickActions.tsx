import { Map, Calendar, Search, BookOpen } from "lucide-react";

interface QuickAction {
  id: number;
  label: string;
  icon: React.ReactNode;
}

const quickActions: QuickAction[] = [
  {
    id: 1,
    label: "Open Full Heat Map",
    icon: <Map className="w-8 h-8" />,
  },
  {
    id: 2,
    label: "Create Event",
    icon: <Calendar className="w-8 h-8" />,
  },
  {
    id: 3,
    label: "Explore Events Today",
    icon: <Search className="w-8 h-8" />,
  },
  {
    id: 4,
    label: "Find Study Spots",
    icon: <BookOpen className="w-8 h-8" />,
  },
];

interface QuickActionsProps {
  onNavigate: (page: "home" | "events" | "crowd") => void;
}

export function QuickActions({ onNavigate }: QuickActionsProps) {
  const handleActionClick = (actionId: number) => {
    if (actionId === 1) {
      // Open Full Heat Map -> navigate to crowd page
      onNavigate("crowd");
    } else if (actionId === 3) {
      // Explore Events Today -> navigate to events page
      onNavigate("events");
    }
    // Add other action handlers as needed
  };

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 pb-16">
      <h2 className="mb-6 text-white">Quick Actions</h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {quickActions.map((action) => (
          <button
            key={action.id}
            onClick={() => handleActionClick(action.id)}
            className="group relative p-6 rounded-2xl transition-all duration-300 
                     bg-white/5 backdrop-blur-sm
                     border border-blue-500/40
                     hover:border-orange-500/60
                     hover:shadow-lg hover:shadow-orange-500/20"
            style={{
              background: "rgba(255, 255, 255, 0.06)",
            }}
          >
            <div className="flex flex-col items-center gap-4">
              <div className="text-white group-hover:text-blue-300 transition-colors">
                {action.icon}
              </div>
              <span className="text-[#BDC5D5] text-center">
                {action.label}
              </span>
            </div>
            
            {/* Hover gradient ring effect */}
            <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
                 style={{
                   background: "linear-gradient(135deg, transparent, rgba(251, 146, 60, 0.1), transparent)",
                 }}
            />
          </button>
        ))}
      </div>
    </section>
  );
}