import { useState } from 'react';
import type { Food } from '../components/NutriVision.type';

export interface UseCameraResult {
  isAnalyzing: boolean;
  handleCapture: (imageFile: File) => Promise<void>;
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

// Code tạm fake ảnh nếu không có camera
export function useCamera(): UseCameraResult {
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [detectedFoods, setDetectedFoods] = useState<Food[]>([]);

  // Nhận file ảnh từ CameraFeed component
  const handleCapture = async (imageFile?: File) => {
    setIsAnalyzing(true);

    try {
      // Nếu không có imageFile, tạo ảnh fake
      let fileToSend = imageFile;
      if (!fileToSend) {
        // Tạo canvas ảnh fake
        const canvas = document.createElement('canvas');
        canvas.width = 640;
        canvas.height = 480;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.fillStyle = '#87CEEB';
          ctx.fillRect(0, 0, canvas.width, canvas.height);
          ctx.fillStyle = '#FFA500';
          ctx.beginPath();
          ctx.arc(320, 240, 50, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillStyle = '#000';
          ctx.font = '20px Arial';
          ctx.textAlign = 'center';
          ctx.fillText('Fake Food Image', 320, 450);
        }
        // Chuyển canvas thành Blob rồi File
        canvas.toBlob((blob) => {
          if (blob) {
            fileToSend = new File([blob], 'fake_image.jpg', { type: 'image/jpeg' });
            sendImageToBackend(fileToSend);
          }
        }, 'image/jpeg');
        return;
      }

      sendImageToBackend(fileToSend);
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

      const res = await fetch("http://localhost:8000/api/v1/capture", {
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


// export function useCamera(): UseCameraResult {
//   const [isAnalyzing, setIsAnalyzing] = useState(false);
//   const [detectedFoods, setDetectedFoods] = useState<Food[]>([]);

//   // Nhận file ảnh từ CameraFeed component
//   const handleCapture = async (imageFile: File) => {
//     setIsAnalyzing(true);

//     try {
//       // Gửi ảnh lên backend để xử lý
//       const formData = new FormData();
//       formData.append("file", imageFile);
//       formData.append("user_id", getUserId());

//       const res = await fetch("http://localhost:8000/api/v1/capture", {
//         method: "POST",
//         body: formData,
//       });

//       if (res.ok) {
//         const data = await res.json();
//         // Chuẩn hoá dữ liệu trả về từ backend thành Food[]; nếu thiếu id/icon/color thì gán mặc định
//         const foods: Food[] = (data?.detected_foods ?? []).map((f: any, idx: number) => ({
//           id: f.id ?? idx + 1,
//           name: f.name ?? 'Unknown',
//           restaurant: f.restaurant ?? '',
//           address: f.address ?? '',
//           google_maps: f.google_maps ?? '',
//           icon: f.icon ?? 'food',
//           color: f.color ?? '#E5E7EB',
//         }));
//         setDetectedFoods(foods);
//       } else {
//         console.error("Lỗi từ backend:", res.status);
//       }
//     } catch (error) {
//       console.error("Lỗi gửi ảnh:", error);
//     }

//     setIsAnalyzing(false);
//   };

//   const handleReset = () => {
//     setIsAnalyzing(false);
//     setDetectedFoods([]);
//     localStorage.removeItem("user_id");
//   };

//   return { isAnalyzing, handleCapture, handleReset, detectedFoods };
// }