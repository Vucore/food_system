import { useState } from 'react';

export function useCamera() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Nhận file ảnh từ CameraFeed component
  const handleCapture = async (imageFile: File) => {
    setIsAnalyzing(true);

    try {
      // Gửi ảnh lên backend để xử lý
      const formData = new FormData();
      formData.append("file", imageFile);

      const res = await fetch("http://localhost:8000/api/v1/capture", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        const data = await res.json();
        console.log("Kết quả từ backend:", data);
        // Xử lý kết quả phân tích ở đây (cập nhật state foods, nutrition, etc.)
      } else {
        console.error("Lỗi từ backend:", res.status);
      }
    } catch (error) {
      console.error("Lỗi gửi ảnh:", error);
    }

    setIsAnalyzing(false);
  };

  const handleReset = () => {
    setIsAnalyzing(false);
    // Reset các dữ liệu phân tích khác nếu cần
  };

  return { isAnalyzing, handleCapture, handleReset };
}