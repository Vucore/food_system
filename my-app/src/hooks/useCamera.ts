import { useState, useEffect, useRef } from 'react';
import type { Food } from '../components/NutriVision.type';

export interface NutritionData {
  predicted_class: string;
  confidence: number;
  nutrition_info: {
    Vietnamese_Name: string;
    English_Name: string;
    Name: string;
    Water: number;
    Energy: number;
    Protein: number;
    Total_lipid_fat: number;
    Carbohydrate_by_difference: number;
    Calcium_Ca: number;
    Iron_Fe: number;
    Magnesium_Mg: number;
    Potassium_K: number;
    Sodium_Na: number;
  };
}

export interface UseCameraResult {
  isAnalyzing: boolean;
  handleCapture: (imageFile?: File) => Promise<void>;
  handleReset: () => void;
  detectedFoods: Food[];
  nutritionData: NutritionData | null;
  nutritionMode: boolean;
  setNutritionMode: (mode: boolean) => void;
}

function getUserId(): string {
  let userId = localStorage.getItem("user_id");
  if (!userId) {
    userId = "user_" + Math.random().toString(36).substring(2, 10);
    localStorage.setItem("user_id", userId);
  }
  return userId;
}

export function useCamera(): UseCameraResult {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [detectedFoods, setDetectedFoods] = useState<Food[]>([]);
  const [nutritionData, setNutritionData] = useState<NutritionData | null>(null);
  const [nutritionMode, setNutritionMode] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Lắng nghe WebSocket từ ESP32 button
  useEffect(() => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    if (!backendUrl) return;

    const wsUrl = `${backendUrl.replace(/^http/, "ws")}/api/v1/ws/button`;

    const connectWebSocket = () => {
      if (wsRef.current) {
        wsRef.current.close();
      }

      console.log("Connecting to WebSocket:", wsUrl);
      const ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        console.log("✅ WebSocket connected for button events");
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
          reconnectTimeoutRef.current = null;
        }

        // Gửi thông tin mode hiện tại
        ws.send(JSON.stringify({
          type: "set_mode",
          mode: nutritionMode ? "nutrition" : "restaurant"
        }));
      };

      ws.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log("📨 WebSocket message received:", message);

          if (message.type === "capture_result") {
            // Restaurant mode result
            const newFood = message.data.new_food;
            if (newFood) {
              setDetectedFoods((prev) => [newFood, ...prev]);
            }
          } else if (message.type === "nutrition_result") {
            // Nutrition mode result
            const data = message.data;
            if (data) {
              setNutritionData({
                predicted_class: data.predicted_class,
                confidence: data.confidence,
                nutrition_info: data.nutrition_data
              });
            }
          } else if (message.type === "mode_updated") {
            console.log("✅ Mode updated on server:", message.mode);
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.onerror = (error) => {
        console.error("❌ WebSocket error:", error);
      };

      ws.onclose = () => {
        console.log("🔌 WebSocket disconnected, reconnecting in 3s...");
        reconnectTimeoutRef.current = setTimeout(connectWebSocket, 3000);
      };
    };

    connectWebSocket();

    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []); // Chỉ connect 1 lần

  // Send mode update when nutrition mode changes
  useEffect(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        type: "set_mode",
        mode: nutritionMode ? "nutrition" : "restaurant"
      }));
      console.log("📤 Sent mode update:", nutritionMode ? "nutrition" : "restaurant");
    }
  }, [nutritionMode]);

  const handleCapture = async (imageFile?: File) => {
    const backendUrl = import.meta.env.VITE_BACKEND_URL;
    if (!backendUrl) return;

    setIsAnalyzing(true);
    const userId = getUserId();

    try {
      if (!imageFile) {
        console.error("No image file provided");
        return;
      }

      const formData = new FormData();
      formData.append("file", imageFile);
      formData.append("user_id", userId);
      formData.append("mode", nutritionMode ? "nutrition" : "restaurant");

      const response = await fetch(`${backendUrl}/api/v1/capture`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      if (nutritionMode) {
        setNutritionData({
          predicted_class: data.predicted_class,
          confidence: data.confidence,
          nutrition_info: data.nutrition_data
        });
      } else {
        if (data.detected_foods && data.detected_foods.length > 0) {
          setDetectedFoods(data.detected_foods);
        }
      }
    } catch (error) {
      console.error("Error capturing image:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setDetectedFoods([]);
    setNutritionData(null);
  };

  return {
    isAnalyzing,
    handleCapture,
    handleReset,
    detectedFoods,
    nutritionData,
    nutritionMode,
    setNutritionMode,
  };
}