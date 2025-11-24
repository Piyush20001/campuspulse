import { ChevronDown } from "lucide-react";
import { Button } from "./ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./ui/dropdown-menu";
import { HeatMap } from "./HeatMap";
import { useState } from "react";

const filterButtons = ["ALL", "GYMS", "LIBRARIES", "DINING", "ACADEMIC", "HOUSING", "STUDY SPOTS", "OUTDOORS"];

const distanceOptions = ["Within 5 min", "Within 10 min", "Within 15 min", "Within 30 min", "Anywhere on Campus"];

export function CrowdPage() {
  const [activeFilter, setActiveFilter] = useState("ALL");
  const [openDropdown, setOpenDropdown] = useState(false);

  return (
    <div className="min-h-screen bg-gray-950 pt-20">
      {/* Filter By Bar */}
      <div className="bg-gray-900/80 border-b border-gray-800 sticky top-16 z-30 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center gap-3">
            <span className="text-gray-400 whitespace-nowrap text-xs uppercase tracking-wide">FILTER BY</span>
            
            {/* Filter Buttons */}
            <div className="flex items-center gap-2 flex-1 overflow-x-auto">
              {filterButtons.map((filter) => (
                <Button
                  key={filter}
                  variant="outline"
                  className={`gap-1 border-gray-700 text-xs uppercase tracking-wide px-3 py-1.5 h-auto whitespace-nowrap flex-shrink-0 transition-all ${
                    activeFilter === filter
                      ? "bg-blue-500/20 border-blue-500/40 text-blue-300"
                      : "bg-gray-800/50 text-gray-300 hover:bg-gray-700 hover:text-white"
                  }`}
                  onClick={() => setActiveFilter(filter)}
                >
                  {filter}
                </Button>
              ))}
              
              {/* Distance Dropdown */}
              <DropdownMenu 
                open={openDropdown}
                onOpenChange={setOpenDropdown}
              >
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="outline"
                    className="gap-1 bg-gray-800/50 border-gray-700 text-gray-300 hover:bg-gray-700 hover:text-white text-xs uppercase tracking-wide px-3 py-1.5 h-auto whitespace-nowrap flex-shrink-0"
                    onMouseEnter={() => setOpenDropdown(true)}
                    onMouseLeave={() => setOpenDropdown(false)}
                  >
                    DISTANCE
                    <ChevronDown className="h-3 w-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent 
                  align="start"
                  className="bg-gray-800 border-gray-700 text-gray-200 min-w-[180px] z-50"
                  onMouseEnter={() => setOpenDropdown(true)}
                  onMouseLeave={() => setOpenDropdown(false)}
                >
                  {distanceOptions.map((option) => (
                    <DropdownMenuItem
                      key={option}
                      className="hover:bg-gray-700 cursor-pointer text-sm text-gray-200"
                    >
                      {option}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          </div>
        </div>
      </div>

      {/* Heatmap */}
      <HeatMap />
    </div>
  );
}
