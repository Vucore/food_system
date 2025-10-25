import React from "react";
import type { NutritionChartProps } from "./NutritionChart.type";

export const NutritionChart: React.FC<NutritionChartProps> = ({
  totalProtein,
  totalCarbs,
  totalFat,
}) => {
  const total = totalProtein + totalCarbs + totalFat;
  const proteinPercent = total ? (totalProtein / total) * 100 : 0;
  const carbsPercent = total ? (totalCarbs / total) * 100 : 0;
  const fatPercent = total ? (totalFat / total) * 100 : 0;

  // Góc bắt đầu cho từng phần
  const proteinAngle = (proteinPercent / 100) * 360;
  const carbsAngle = (carbsPercent / 100) * 360;
  // Fat là phần còn lại

  // Hàm chuyển phần trăm sang tọa độ trên vòng tròn
  function getCoordsForPercent(percent: number) {
    const angle = (percent / 100) * 2 * Math.PI - Math.PI / 2;
    return {
      x: 64 + 44 * Math.cos(angle),
      y: 64 + 44 * Math.sin(angle),
    };
  }

  // Tạo path cho từng phần
  function describeArc(startPercent: number, endPercent: number, color: string) {
    const start = getCoordsForPercent(startPercent);
    const end = getCoordsForPercent(endPercent);
    const largeArcFlag = endPercent - startPercent > 50 ? 1 : 0;
    return (
      <path
        d={`
          M ${start.x} ${start.y}
          A 44 44 0 ${largeArcFlag} 1 ${end.x} ${end.y}
        `}
        stroke={color}
        strokeWidth="20"
        fill="none"
      />
    );
  }

  return (
    <div className="flex flex-col justify-center items-center w-32 h-32">
      <svg width="128" height="128" viewBox="0 0 128 128">
        {/* Protein */}
        {describeArc(0, proteinPercent, "#10B981")}
        {/* Carbs */}
        {describeArc(proteinPercent, proteinPercent + carbsPercent, "#F59E0B")}
        {/* Fat */}
        {describeArc(proteinPercent + carbsPercent, 100, "#EF4444")}
      </svg>
      <div className="mt-2 text-xs text-center">
        <div>Protein: {totalProtein}g</div>
        <div>Carbs: {totalCarbs}g</div>
        <div>Fat: {totalFat}g</div>
      </div>
    </div>
  );
};