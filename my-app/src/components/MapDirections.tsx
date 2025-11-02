import React, { useEffect, useState, useMemo } from "react";
import type { MapDirectionsProps } from "./MapDirections.type";

export const MapDirections: React.FC<MapDirectionsProps> = ({
  selectedFood,
  onClose,
}) => {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  // Lấy API Key từ backend
  useEffect(() => {
    const fetchApiKey = async () => {
      try {
        const response = await fetch(`http://localhost:8000/api/v1/config/maps-api-key`);
        if (!response.ok) {
          throw new Error("Không thể lấy API Key từ backend");
        }
        const data = await response.json();
        setApiKey(data.apiKey);
      } catch (err: any) {
        setError(err.message);
        console.error("Error fetching Maps API Key:", err);
      }
    };

    fetchApiKey();
  }, []);

  const mapUrl = useMemo(() => {
    if (!selectedFood?.address || !apiKey) return null;
    return `https://www.google.com/maps/embed/v1/place?key=${apiKey}&q=${encodeURIComponent(selectedFood.address)}`;
  }, [selectedFood?.address, apiKey]);

  const hasError = selectedFood?.address && !mapUrl && apiKey === null;

  return (
    <div className="w-full bg-white rounded-2xl border border-gray-100 shadow-lg p-6 animate-in fade-in slide-in-from-bottom-4">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 pb-4 border-b border-gray-100">
        <div>
          <h3 className="text-xl font-bold text-emerald-700">
            📍 {selectedFood?.name || "Bản đồ chỉ đường"}
          </h3>
          <p className="text-sm text-gray-600 mt-1">
            {selectedFood?.restaurant || "Chọn một món ăn để xem bản đồ"}
          </p>
        </div>
        {selectedFood && (
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 transition-colors p-2 hover:bg-gray-100 rounded-lg"
            title="Đóng"
          >
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        )}
      </div>

      {/* Map hoặc Placeholder */}
      <div
        className="rounded-xl overflow-hidden shadow-lg mb-4 bg-gray-100 flex items-center justify-center"
        style={{ height: "400px" }}
      >
        {mapUrl ? (
          <iframe
            width="100%"
            height="400"
            frameBorder="0"
            src={mapUrl}
            allowFullScreen
            loading="lazy"
            referrerPolicy="no-referrer-when-downgrade"
            title="Google Maps"
          ></iframe>
        ) : hasError || error ? (
          <div className="text-center text-red-500 p-4">
            <svg
              width="48"
              height="48"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              className="mx-auto mb-2"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <p className="text-sm font-medium">❌ Lỗi tải bản đồ</p>
            <p className="text-xs text-red-400 mt-1">{error || "API Key không hợp lệ"}</p>
          </div>
        ) : (
          <div className="text-center text-gray-500">
            <svg
              width="64"
              height="64"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="1"
              className="mx-auto mb-2 opacity-50"
            >
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            <p className="text-sm font-medium">Chưa chọn địa điểm</p>
            <p className="text-xs text-gray-400 mt-1">Bấm nút "Go" để xem bản đồ</p>
          </div>
        )}
      </div>

      {/* Address Info */}
      {selectedFood?.address && (
        <div className="p-4 bg-gray-50 rounded-lg mb-4">
          <p className="text-sm text-gray-600 font-medium mb-2">📮 Địa chỉ đầy đủ:</p>
          <p className="text-base text-gray-800 font-semibold">
            {selectedFood.address}
          </p>
        </div>
      )}

      {/* Action Buttons */}
      {selectedFood?.address ? (
        <div className="flex gap-3">
          <a
            href={`https://www.google.com/maps/search/${encodeURIComponent(
              selectedFood.address
            )}`}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white font-medium rounded-lg transition-colors text-center flex items-center justify-center gap-2"
          >
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
            >
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
              <circle cx="12" cy="10" r="3"></circle>
            </svg>
            Direction
          </a>
          <button
            onClick={onClose}
            className="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium rounded-lg transition-colors"
          >
            Close
          </button>
        </div>
      ) : (
        <div className="flex gap-3">
          <button
            disabled
            className="flex-1 px-4 py-2 bg-gray-300 text-gray-500 font-medium rounded-lg cursor-not-allowed opacity-50"
          >
            Direction
          </button>
        </div>
      )}
    </div>
  );
};

export default MapDirections;