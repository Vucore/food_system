import { useState } from 'react';

export function useCamera() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Nhận file ảnh làm tham số
  const handleCapture = async (imageFile: File) => {
    setIsAnalyzing(true);
    const formData = new FormData();
    formData.append("file", imageFile);

    try {
      const res = await fetch("http://localhost:8000/api/v1/capture", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("Kết quả từ backend:", data);
      // Xử lý kết quả ở đây nếu cần
    } catch (error) {
      console.error("Lỗi gửi ảnh:", error);
    }
    setIsAnalyzing(false);
  };


  const handleReset = () => {
    setIsAnalyzing(false);
    // Đặt lại trạng thái hoặc dữ liệu ở đây
  };

  return { isAnalyzing, handleCapture, handleReset };
}