import { useState, useEffect } from 'react';
import type { Food } from '../components/NutriVision.type';

const backendUrl = "http://localhost:8000"; // Thay thế bằng URL backend

export interface UseCameraResult {
  isAnalyzing: boolean;
  handleCapture: (imageFile?: File) => Promise<void>;
  handleReset: () => void;
  detectedFoods: Food[];
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
  // Lắng nghe WebSocket từ ESP32 button
  useEffect(() => {
    if (!backendUrl) return;

    const wsUrl = `${backendUrl.replace(/^http/, "ws")}/api/v1/ws/button`;
    const ws = new WebSocket(wsUrl);

    ws.onopen = () => {
      console.log("WebSocket connected for button events");
    };

    ws.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      try {
        const message = JSON.parse(event.data);

        if (message.type === "capture_result") {
          console.log("Button capture result:", message.data);
          const response = message.data;

          if (response.success && response.detected_foods) {
            const foods: Food[] = (response.detected_foods ?? []).map((f: any, idx: number) => ({
              id: f._id ?? f.id ?? idx + 1,
              name: f.name ?? 'Unknown',
              restaurant: f.restaurant ?? '',
              address: f.address ?? '',
              google_maps: f.google_maps ?? '',
              icon: f.icon ?? 'food',
              color: f.color ?? '#E5E7EB',
            }));

            console.log("Mapped foods from button:", foods);
            setDetectedFoods(foods);
            setIsAnalyzing(false);
          }
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    ws.onclose = () => {
      console.log("WebSocket disconnected");
    };

    return () => {
      ws.close();
    };
  }, []);
  // Nhận file ảnh từ CameraFeed component
  const handleCapture = async (imageFile?: File) => {
    setIsAnalyzing(true);

    try {
      if (!imageFile) {
        console.error("Không có file ảnh để gửi");
        setIsAnalyzing(false);
        return;
      }

      await sendImageToBackend(imageFile);
    } catch (error) {
      console.error("Lỗi gửi ảnh:", error);
      setIsAnalyzing(false);
    }
  };
  const sendImageToBackend = async (fileToSend: File) => {
    try {
      const formData = new FormData();
      formData.append("file", fileToSend);
      formData.append("user_id", getUserId());

      const res = await fetch(`${import.meta.env.VITE_BACKEND_URL}/api/v1/capture`, {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        const foods: Food[] = (data?.detected_foods ?? []).map((f: any, idx: number) => ({
          id: f._id ?? f.id ?? idx + 1,
          name: f.name ?? 'Unknown',
          restaurant: f.restaurant ?? '',
          address: f.address ?? '',
          google_maps: f.google_maps ?? '',
          icon: f.icon ?? 'food',
          color: f.color ?? '#E5E7EB',
        }));
        setDetectedFoods(foods);
      } else {
        console.error("Lỗi từ backend:", res.status);
      }
    } catch (error) {
      console.error("Lỗi gửi ảnh:", error);
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setIsAnalyzing(false);
    setDetectedFoods([]);
    localStorage.removeItem("user_id");
  };

  return { isAnalyzing, handleCapture, handleReset, detectedFoods };
}