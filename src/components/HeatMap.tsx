import { useState } from "react";
import campusMap from "figma:asset/6cfc64f77f88dd08ebaba02a343a3a72b5311bfb.png";

export function HeatMap() {
  const [intensity, setIntensity] = useState(0.6);

  // Generate mock heatmap data points
  const heatmapPoints = [
    { x: 20, y: 30, intensity: 0.8, label: "Student Union" },
    { x: 60, y: 40, intensity: 0.9, label: "Library" },
    { x: 40, y: 60, intensity: 0.5, label: "Stadium" },
    { x: 75, y: 25, intensity: 0.7, label: "Dining Hall" },
    { x: 30, y: 75, intensity: 0.4, label: "Rec Center" },
    { x: 85, y: 70, intensity: 0.6, label: "Engineering" },
  ];

  return (
    <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="bg-gray-900 rounded-lg shadow-2xl overflow-hidden border border-gray-800">
        <div className="p-6">
          <h2 className="mb-4 text-white">Campus Crowd Intensity</h2>
          
          {/* Map Container */}
          <div className="relative w-full aspect-[16/9] bg-gray-950 rounded-lg overflow-hidden">
            {/* Campus Map Background */}
            <img
              src={campusMap}
              alt="University of Florida Campus Map"
              className="absolute inset-0 w-full h-full object-cover"
            />
            
            {/* Heatmap Overlay */}
            <svg className="absolute inset-0 w-full h-full" style={{ filter: 'blur(40px)' }}>
              <defs>
                {heatmapPoints.map((point, index) => (
                  <radialGradient
                    key={index}
                    id={`heat-${index}`}
                    cx="50%"
                    cy="50%"
                  >
                    <stop
                      offset="0%"
                      style={{
                        stopColor: getHeatColor(point.intensity),
                        stopOpacity: 0.9,
                      }}
                    />
                    <stop
                      offset="50%"
                      style={{
                        stopColor: getHeatColor(point.intensity),
                        stopOpacity: 0.6,
                      }}
                    />
                    <stop
                      offset="100%"
                      style={{
                        stopColor: getHeatColor(point.intensity),
                        stopOpacity: 0,
                      }}
                    />
                  </radialGradient>
                ))}
              </defs>
              
              {heatmapPoints.map((point, index) => (
                <g key={index}>
                  <circle
                    cx={`${point.x}%`}
                    cy={`${point.y}%`}
                    r="15%"
                    fill={`url(#heat-${index})`}
                  />
                </g>
              ))}
            </svg>
          </div>

          {/* Legend */}
          <div className="mt-4 flex items-center justify-between">
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-400">Intensity:</span>
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-500">Low</span>
                <div className="w-48 h-6 rounded-full flex">
                  <div className="flex-1 bg-blue-600 rounded-l-full"></div>
                  <div className="flex-1 bg-cyan-500"></div>
                  <div className="flex-1 bg-yellow-500"></div>
                  <div className="flex-1 bg-orange-500"></div>
                  <div className="flex-1 bg-red-500 rounded-r-full"></div>
                </div>
                <span className="text-sm text-gray-500">High</span>
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Last updated: Just now
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function getHeatColor(intensity: number): string {
  if (intensity < 0.2) return "#2563eb"; // blue-600
  if (intensity < 0.4) return "#06b6d4"; // cyan-500
  if (intensity < 0.6) return "#eab308"; // yellow-500
  if (intensity < 0.8) return "#f97316"; // orange-500
  return "#ef4444"; // red-500
}