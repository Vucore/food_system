"use client";
import React, { useState } from "react";
import { Header } from "./Header";
import { CameraFeed } from "./CameraFeed";
import { DetectedFoods } from "./DetectedFoods";
import { NutritionSummary } from "./NutritionSummary";
import type { Food } from "./NutriVision.type";
import { useCamera } from '../hooks/useCamera';


export const NutriVision: React.FC = () => {
  const { isAnalyzing, handleCapture, handleReset } = useCamera();
  const [detectedFoods, setDetectedFoods] = useState<Food[]>([
    {
      id: 1,
      name: "Grilled Chicken",
      portion: "150g portion",
      calories: 248,
      protein: 46,
      carbs: 0,
      fat: 5,
      icon: "chicken",
      color: "#FFEDD5",
    },
    {
      id: 2,
      name: "Mixed Salad",
      portion: "100g portion",
      calories: 25,
      protein: 2,
      carbs: 4,
      fat: 0,
      icon: "salad",
      color: "#D1FAE5",
    },
    {
      id: 3,
      name: "Steamed Rice",
      portion: "80g portion",
      calories: 103,
      protein: 2,
      carbs: 23,
      fat: 0,
      icon: "rice",
      color: "#FEF9C3",
    },
  ]);

  // const [isAnalyzing, setIsAnalyzing] = useState(true);
  const [isLiveFeedActive, setIsLiveFeedActive] = useState(true);
  const [totalCalories, setTotalCalories] = useState(376);
  const [totalProtein, setTotalProtein] = useState(50);
  const [totalCarbs, setTotalCarbs] = useState(27);
  const [totalFat, setTotalFat] = useState(5);


  // const handleReset = () => {
  //   setDetectedFoods([]);
  //   setTotalCalories(0);
  //   setTotalProtein(0);
  //   setTotalCarbs(0);
  //   setTotalFat(0);

  // };

  const handleSaveToLog = () => {
    console.log("Saving to log:", {
      detectedFoods,
      totalCalories,
      totalProtein,
      totalCarbs,
      totalFat,
    });
  };

  const handleExport = () => {
    console.log("Exporting data:", {
      detectedFoods,
      totalCalories,
      totalProtein,
      totalCarbs,
      totalFat,
    });
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header isLiveFeedActive={isLiveFeedActive} />
      <main className="flex gap-6 justify-center items-start p-6 w-full max-md:flex-col max-md:items-center">
        <div className="flex flex-col items-center max-w-full w-[684px]">
          <CameraFeed
            isAnalyzing={isAnalyzing}
            onCapture={handleCapture}
            onReset={handleReset}
          />
        </div>
        <div className="flex flex-col gap-6 max-w-full w-[684px]">
          <DetectedFoods detectedFoods={detectedFoods} />
          <NutritionSummary
            totalCalories={totalCalories}
            totalProtein={totalProtein}
            totalCarbs={totalCarbs}
            totalFat={totalFat}
            onSaveToLog={handleSaveToLog}
            onExport={handleExport}
          />
        </div>
      </main>
    </div>
  );
};

export default NutriVision;
