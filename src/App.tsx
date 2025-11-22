import { useState } from "react";
import { Header } from "./components/Header";
import { HeatMap } from "./components/HeatMap";
import { TrendingEvents } from "./components/TrendingEvents";
import { SavedLocations } from "./components/SavedLocations";
import { QuickActions } from "./components/QuickActions";
import { EventsPage } from "./components/EventsPage";
import { CrowdPage } from "./components/CrowdPage";

export default function App() {
  const [currentPage, setCurrentPage] = useState<"home" | "events" | "crowd">("home");

  return (
    <div className="min-h-screen bg-gray-950">
      <Header currentPage={currentPage} onNavigate={setCurrentPage} />
      <main>
        {currentPage === "home" ? (
          <>
            <HeatMap />
            <TrendingEvents />
            <SavedLocations />
            <QuickActions onNavigate={setCurrentPage} />
          </>
        ) : currentPage === "events" ? (
          <EventsPage />
        ) : (
          <CrowdPage />
        )}
      </main>
    </div>
  );
}