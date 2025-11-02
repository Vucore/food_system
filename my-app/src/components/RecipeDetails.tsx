import React, { useState } from "react";
import { motion } from "framer-motion";
import type { RecipeDetailsProps } from "./RecipeDetails.type";

export const RecipeDetails: React.FC<RecipeDetailsProps> = ({
  nguyenlieu = [],
  soche = [],
  thuchien = [],
  howtouse = [],
  tips = [],
}) => {
  const [activeTab, setActiveTab] = useState<
    "nguyenlieu" | "soche" | "thuchien" | "howtouse" | "tips"
  >("nguyenlieu");

  const tabs = [
    { id: "nguyenlieu", label: "Nguyên liệu", icon: "🥦" },
    { id: "soche", label: "Cách sơ chế", icon: "🔪" },
    { id: "thuchien", label: "Thực hiện", icon: "👨‍🍳" },
    { id: "howtouse", label: "Cách dùng", icon: "🍽️" },
    { id: "tips", label: "Mẹo hay", icon: "💡" },
  ];

  const colorMap: Record<string, string> = {
    nguyenlieu: "bg-emerald-500",
    soche: "bg-orange-500",
    thuchien: "bg-sky-500",
    howtouse: "bg-amber-500",
    tips: "bg-yellow-500",
  };

  const getContent = () => {
    switch (activeTab) {
      case "nguyenlieu":
        return nguyenlieu;
      case "soche":
        return soche;
      case "thuchien":
        return thuchien;
      case "howtouse":
        return howtouse;
      case "tips":
        return tips;
      default:
        return [];
    }
  };

  const content = getContent();

  return (
    <div className="w-full bg-white/80 backdrop-blur-md rounded-2xl shadow-md p-6 space-y-5 border border-emerald-50">
      <div className="flex gap-2 flex-wrap justify-center">
        {tabs.map((tab) => (
          <motion.button
            whileTap={{ scale: 0.95 }}
            whileHover={{ scale: 1.05 }}
            key={tab.id}
            onClick={() => setActiveTab(tab.id as any)}
            className={`flex items-center px-4 py-2 rounded-full font-semibold transition-all shadow-sm ${
              activeTab === tab.id
                ? `${colorMap[tab.id]} text-white shadow-md`
                : "bg-gray-100 text-gray-700 hover:bg-gray-200"
            }`}
          >
            <span className="mr-2 text-lg">{tab.icon}</span>
            {tab.label}
          </motion.button>
        ))}
      </div>

      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="bg-gradient-to-br from-emerald-50 via-white to-amber-50 rounded-xl p-5 min-h-[220px] max-h-[420px] overflow-y-auto border border-gray-100"
      >
        {content.length > 0 ? (
          <ul className="space-y-3">
            {content.map((item, index) => (
              <li key={index} className="flex items-start gap-3 text-gray-700">
                <span className="text-emerald-600 font-bold mt-1">•</span>
                <span className="text-[15px] leading-relaxed">{item}</span>
              </li>
            ))}
          </ul>
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400 italic">
            Không có thông tin cho mục này 🍃
          </div>
        )}
      </motion.div>
    </div>
  );
};

export default RecipeDetails;
