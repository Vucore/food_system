"use client";
import React, { useState, useEffect } from "react";
import { Header } from "./Header";
import { CameraFeed } from "./CameraFeed";
import { DetectedFoods } from "./DetectedFoods";
import { MapDirections } from "./MapDirections";
import { useCamera } from '../hooks/useCamera';
import type { NutriVisionProps } from "./NutriVision.type";

export const NutriVision: React.FC<NutriVisionProps> = ({ onSelectFood }) => {
  const {
    isAnalyzing,
    handleCapture,
    handleReset,
    detectedFoods,
  } = useCamera();

  const [selectedFoodForMap, setSelectedFoodForMap] = useState<any>(null);

  useEffect(() => {
    handleReset();
  }, []);

  const [isLiveFeedActive] = useState(true);
  const handleSelectFood = (food: any) => {
    if (onSelectFood) {
      onSelectFood(food);
    }
  };

  // Chỉ hiển thị map
  const handleShowMap = (food: any) => {
    setSelectedFoodForMap(food);
  };
  return (
    <div className="min-h-screen bg-gray-50">
      <Header isLiveFeedActive={isLiveFeedActive} />
      <main className="flex gap-6 justify-center items-start p-6 w-full max-md:flex-col max-md:items-center">
        {/* Cột trái: Camera - Nhỏ hơn và hình vuông */}
        <div className="flex flex-col items-center max-w-full w-[480px] h-[480px]">
          <CameraFeed
            isAnalyzing={isAnalyzing}
            onCapture={handleCapture}
            onReset={handleReset}
          />
        </div>

        {/* Cột phải: Detected Foods - Lớn hơn */}
        <div className="flex flex-col gap-6 max-w-full w-[700px]">
          <DetectedFoods
            detectedFoods={detectedFoods}
            onSelectFood={handleSelectFood}
            onShowMap={handleShowMap}
          />
          <MapDirections
            selectedFood={selectedFoodForMap}
            onClose={() => setSelectedFoodForMap(null)}
          />
        </div>
      </main>
    </div>
  );
};

export default NutriVision;