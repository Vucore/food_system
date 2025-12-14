// NutritionInfo.tsx
import React from "react";
import type { NutritionInfoProps } from "./NutritionInfo.type";

export const NutritionInfo: React.FC<NutritionInfoProps> = ({ nutritionData }) => {
    console.log("📊 Nutrition Data received:", nutritionData); // Debug log

    if (!nutritionData) {
        return (
            <section className="flex flex-col gap-4 p-6 bg-white rounded-2xl border border-gray-100 border-solid shadow-sm">
                <div className="flex justify-between items-center">
                    <h2 className="m-0 text-lg font-semibold leading-7 text-gray-800">
                        🥗 Nutrition Information
                    </h2>
                </div>
                <div className="text-center py-8 text-gray-500">
                    No nutrition data available
                </div>
            </section>
        );
    }

    const formatValue = (value: any, unit: string = ""): string => {
        // Kiểm tra null, undefined, NaN, empty string
        if (value === null || value === undefined || value === '' ||
            (typeof value === 'number' && isNaN(value))) {
            return 'N/A';
        }

        // Nếu là số, format với 2 chữ số thập phân
        if (typeof value === 'number') {
            return `${value.toFixed(2)}${unit ? ' ' + unit : ''}`;
        }

        // Nếu là string
        return `${value}${unit ? ' ' + unit : ''}`;
    };

    const nutritionFields = [
        { label: "Name", key: "name", unit: "" },
        { label: "Vietnamese Name", key: "vietnamese_name", unit: "" },
        { label: "English Name", key: "english_name", unit: "" },
        { label: "Water", key: "water", unit: "g" },
        { label: "Energy", key: "energy", unit: "kcal" },
        { label: "Protein", key: "protein", unit: "g" },
        { label: "Total Lipid (Fat)", key: "total_lipid_fat", unit: "g" },
        { label: "Carbohydrate", key: "carbohydrate_by_difference", unit: "g" },
        { label: "Calcium (Ca)", key: "calcium_ca", unit: "mg" },
        { label: "Iron (Fe)", key: "iron_fe", unit: "mg" },
        { label: "Magnesium (Mg)", key: "magnesium_mg", unit: "mg" },
        { label: "Potassium (K)", key: "potassium_k", unit: "mg" },
        { label: "Sodium (Na)", key: "sodium_na", unit: "mg" },
    ];

    return (
        <section className="flex flex-col gap-4 p-6 bg-white rounded-2xl border border-gray-100 border-solid shadow-sm">
            <div className="flex justify-between items-center">
                <h2 className="m-0 text-lg font-semibold leading-7 text-gray-800">
                    🥗 Nutrition Information
                </h2>
                <span className="px-3 py-1.5 text-sm font-medium text-blue-500 bg-blue-100 rounded-full">
                    Per 100g
                </span>
            </div>

            <div className="overflow-auto w-full custom-scroll" style={{ maxHeight: "480px" }}>
                <div className="space-y-3">
                    {nutritionFields.map((field, index) => {
                        const value = nutritionData[field.key as keyof typeof nutritionData];
                        console.log(`Field: ${field.key}, Value:`, value); // Debug log

                        return (
                            <div
                                key={index}
                                className="flex justify-between items-center p-3 rounded-lg hover:bg-gray-50 transition-colors duration-200"
                            >
                                <span className="text-sm font-medium text-gray-700">
                                    {field.label}:
                                </span>
                                <span className="text-sm font-semibold text-gray-900">
                                    {formatValue(value, field.unit)}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>
        </section>
    );
};