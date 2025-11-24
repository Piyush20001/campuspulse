import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "./ui/table";

interface SavedLocation {
  id: number;
  location: string;
  statusNow: "Low" | "Medium" | "High";
  nextHour: "Low" | "Medium" | "High";
  bestTime: string;
}

const savedLocations: SavedLocation[] = [
  {
    id: 1,
    location: "Library West",
    statusNow: "High",
    nextHour: "Medium",
    bestTime: "9:00 PM",
  },
  {
    id: 2,
    location: "SouthWest Rec",
    statusNow: "Medium",
    nextHour: "High",
    bestTime: "2:00 PM",
  },
  {
    id: 3,
    location: "CSE Building",
    statusNow: "Low",
    nextHour: "Low",
    bestTime: "11:00 AM",
  },
];

function getStatusColor(status: "Low" | "Medium" | "High"): string {
  switch (status) {
    case "Low":
      return "text-green-400";
    case "Medium":
      return "text-yellow-400";
    case "High":
      return "text-red-400";
  }
}

export function SavedLocations() {
  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h2 className="mb-6 text-white">Your Saved Locations</h2>

      <div className="bg-gray-900 rounded-lg shadow-2xl overflow-hidden border border-gray-800">
        <Table>
          <TableHeader>
            <TableRow className="border-b border-gray-800 hover:bg-gray-900">
              <TableHead className="text-gray-400">Location</TableHead>
              <TableHead className="text-gray-400">Status Now</TableHead>
              <TableHead className="text-gray-400">Next Hour</TableHead>
              <TableHead className="text-gray-400">Best Time Today</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {savedLocations.map((location) => (
              <TableRow
                key={location.id}
                className="border-b border-gray-800 hover:bg-gray-800/50"
              >
                <TableCell className="text-gray-200">
                  {location.location}
                </TableCell>
                <TableCell className={getStatusColor(location.statusNow)}>
                  {location.statusNow}
                </TableCell>
                <TableCell className={getStatusColor(location.nextHour)}>
                  {location.nextHour}
                </TableCell>
                <TableCell className="text-gray-200">
                  {location.bestTime}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </section>
  );
}
