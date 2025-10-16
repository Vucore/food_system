import { useState } from 'react';

export function useCamera() {
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  // Nhận file ảnh làm tham số
const handleCapture = async () => {
    setIsAnalyzing(true);

    try {
      // Lấy ảnh từ backend proxy (không bị CORS)
      const imageRes = await fetch("http://localhost:8000/api/v1/proxy_capture");
      const imageBlob = await imageRes.blob();
      const imageFile = new File([imageBlob], "capture.jpg", { type: "image/jpeg" });

      // Gửi ảnh lên backend (nếu cần xử lý tiếp)
      const formData = new FormData();
      formData.append("file", imageFile);

      const res = await fetch("http://localhost:8000/api/v1/capture", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      console.log("Kết quả từ backend:", data);
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