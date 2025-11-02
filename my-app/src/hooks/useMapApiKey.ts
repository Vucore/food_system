import { useState, useEffect } from "react";

export function useMapApiKey() {
  const [apiKey, setApiKey] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchApiKey = async () => {
      try {
        setLoading(true);
        const response = await fetch(
          `${import.meta.env.VITE_BACKEND_URL}/api/v1/config/maps-api-key`
        );

        if (!response.ok) {
          throw new Error(`HTTP Error: ${response.status}`);
        }

        const data = await response.json();
        setApiKey(data.apiKey);
        setError(null);
      } catch (err: any) {
        const errorMsg = err.message || "Không thể lấy API Key từ backend";
        setError(errorMsg);
        console.error("Error fetching Maps API Key:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchApiKey();
  }, []);

  return { apiKey, error, loading };
}