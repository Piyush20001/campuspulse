import { Search, ChevronDown, User } from "lucide-react";
import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import campusPulseLogo from "figma:asset/258b77799aeefa84f6f2be6b723b44927af69788.png";
import ufLogo from "figma:asset/e37c8c320c0798b5d8ad1a47705137f0e95aea70.png";

interface HeaderProps {
  currentPage: "home" | "events" | "crowd";
  onNavigate: (page: "home" | "events" | "crowd") => void;
}

export function Header({ currentPage, onNavigate }: HeaderProps) {
  return (
    <header className="bg-gray-950 border-b border-gray-800 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          {/* Left: UF Logo */}
          <div className="flex-shrink-0">
            <img src={ufLogo} alt="UF Logo" className="h-20" />
          </div>

          {/* Center: Campus Pulse Logo */}
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 cursor-pointer" onClick={() => onNavigate("home")}>
            <img
              src={campusPulseLogo}
              alt="Campus Pulse"
              className="h-18"
            />
          </div>

          {/* Navigation Buttons */}
          <div className="flex items-center gap-2">
            {/* Username Dropdown */}
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button
                  variant="ghost"
                  className="gap-1 text-gray-200 hover:text-white hover:bg-gray-800"
                >
                  <User className="h-4 w-4" />
                  USERNAME
                  <ChevronDown className="h-4 w-4" />
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                align="end"
                className="bg-gray-900 border-gray-800 text-gray-200 w-56"
              >
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Profile</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Saved Locations</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">My Interested Events</DropdownMenuItem>
                
                <DropdownMenuSeparator className="bg-gray-700" />
                
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Organizer Dashboard</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Create Event</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Manage My Events</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Event Analytics</DropdownMenuItem>
                
                <DropdownMenuSeparator className="bg-gray-700" />
                
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Settings</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Help / About</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Give Feedback</DropdownMenuItem>
                <DropdownMenuItem className="hover:bg-gray-800 cursor-pointer">Sign Out</DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>

            <Button
              variant="ghost"
              onClick={() => onNavigate("crowd")}
              className={`text-gray-200 hover:text-white hover:bg-gray-800 ${
                currentPage === "crowd" ? "bg-gray-800" : ""
              }`}
            >
              CROWD
            </Button>

            <Button
              variant="ghost"
              onClick={() => onNavigate("events")}
              className={`text-gray-200 hover:text-white hover:bg-gray-800 ${
                currentPage === "events" ? "bg-gray-800" : ""
              }`}
            >
              EVENTS
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
}