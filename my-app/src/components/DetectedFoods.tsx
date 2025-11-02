import React, { useState } from "react";
import { FoodIcon } from "./FoodIcon";
import type { DetectedFoodsPropsWithClick, Food } from "./DetectedFood.type";

export const DetectedFoods: React.FC<DetectedFoodsPropsWithClick> = ({
  detectedFoods,
  onSelectFood,
  onShowMap,
}) => {
  const [hoveredId, setHoveredId] = useState<number | null>(null);

  // Click hàng: mở recipe modal
  const handleRowClick = (food: Food) => {
    if (onSelectFood) {
      onSelectFood(food);
    }
  };

  // Click nút Go: chỉ hiển thị map
  const handleGoButtonClick = (e: React.MouseEvent, food: Food) => {
    e.stopPropagation();
    if (onShowMap) {
      onShowMap(food);
    }
  };

  return (
    <section className="flex flex-col gap-4 p-6 bg-white rounded-2xl border border-gray-100 border-solid shadow-sm">
      <div className="flex justify-between items-center">
        <h2 className="m-0 text-lg font-semibold leading-7 text-gray-800">
          🍽️ Detected Foods
        </h2>
        <span className="px-3 py-1.5 text-sm font-medium text-emerald-500 bg-emerald-100 rounded-full">
          {detectedFoods.length} items found
        </span>
      </div>
      <div className="overflow-auto w-full custom-scroll" style={{ maxHeight: "320px" }}>
        <table className="w-full border-collapse">
          <thead>
            <tr className="border-b border-solid border-b-gray-100">
              <th className="px-2 py-3.5 text-sm font-medium text-left text-gray-600">
                Food Item
              </th>
              <th className="px-2 py-3.5 text-sm font-medium text-left text-gray-600">
                Restaurant
              </th>
              <th className="px-2 py-3.5 text-sm font-medium text-left text-gray-600">
                Address
              </th>
              <th className="px-2 py-3.5 text-sm font-medium text-center text-gray-600">
                Directions
              </th>
            </tr>
          </thead>

          <tbody>
            {detectedFoods?.map((food, index) => (
              <tr
                key={food.id}
                onClick={() => handleRowClick(food)}
                style={{
                  borderTop: index > 0 ? "1px solid #F9FAFB" : "none",
                }}
                className="cursor-pointer hover:bg-emerald-50 transition-colors duration-200"
              >
                {/* Food Item Column */}
                <td className="px-2 py-4">
                  <div className="flex gap-3 items-center">
                    <div
                      className="flex justify-center items-center px-3 py-2 w-10 h-10 rounded-lg flex-shrink-0"
                      style={{
                        background: food.color ?? "#E5E7EB",
                      }}
                    >
                      <FoodIcon icon={food.icon ?? "food"} />
                    </div>
                    <div className="min-w-0">
                      <div className="text-base font-medium leading-6 text-gray-800 truncate">
                        {food.name}
                      </div>
                    </div>
                  </div>
                </td>

                {/* Restaurant Column */}
                <td className="px-2 py-4">
                  <div className="text-base text-gray-700 truncate">
                    {food.restaurant || "N/A"}
                  </div>
                </td>

                {/* Address Column */}
                <td className="px-2 py-4">
                  <div
                    className="relative group"
                    onMouseEnter={() => setHoveredId(food.id)}
                    onMouseLeave={() => setHoveredId(null)}
                  >
                    <div className="text-base text-gray-700 line-clamp-2 cursor-pointer hover:text-blue-600 transition-colors">
                      {food.address || "N/A"}
                    </div>

                    {/* Tooltip - Hiển thị full address khi hover */}
                    {hoveredId === food.id && food.address && food.address.length > 40 && (
                      <div className="absolute bottom-full left-0 mb-2 p-3 bg-gray-900 text-white text-sm rounded-lg shadow-lg z-10 whitespace-normal max-w-xs">
                        {food.address}
                        <div className="absolute top-full left-2 w-2 h-2 bg-gray-900 transform rotate-45"></div>
                      </div>
                    )}
                  </div>
                </td>

                {/* Action Column - Nút Go */}
                <td
                  className="px-4 py-4 text-center"
                  onClick={(e) => e.stopPropagation()}
                >
                  <button
                    onClick={(e) => handleGoButtonClick(e, food)}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium rounded-lg transition-all duration-200 shadow-sm"
                    title="Hiển thị bản đồ"
                  >
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="text-white"
                    >
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                    Go
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
};