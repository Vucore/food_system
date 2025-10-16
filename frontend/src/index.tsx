import './index.css';
import { useState, useRef, useEffect } from "react";
import type { DetectedFood, Nutrients } from "./foodTypes";
import { sampleDetected } from "./foodTypes";
// FoodCalorieDashboard.tsx
// React + TypeScript single-file component for a food-calorie web UI.
// TailwindCSS classes are used for styling. This file is meant to be previewed
// or dropped into a React + Vite/CRA project configured with Tailwind.

export default function FoodCalorieDashboard() {
  const [detected, setDetected] = useState<DetectedFood[]>(sampleDetected);
  const [isDetecting, setIsDetecting] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  // total calories computed from detected list
  const totalCalories = detected.reduce((s, f) => s + f.calories, 0);

  useEffect(() => {
    // Try to access local camera as a placeholder for ESP32 stream.
    // In production you may set <video src="http://ESP32-CAM-IP:81/stream" />
    // or use a WebSocket/ MJPEG endpoint from ESP32.
    // Here we request permission for the local webcam to simulate preview.
    async function startLocalCamera() {
      if (!videoRef.current) return;
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
        videoRef.current.srcObject = stream;
        videoRef.current.play();
      } catch (err) {
        // ignore errors in demo environment
        // console.warn("Camera access failed:", err);
      }
    }

    startLocalCamera();

    return () => {
      // stop tracks when unmounting
      const v = videoRef.current;
      if (v && v.srcObject) {
        const st = v.srcObject as MediaStream;
        st.getTracks().forEach((t) => t.stop());
      }
    };
  }, []);

  function handleStartDetection() {
    setIsDetecting(true);
    // Demo: append a new detected food every 3s (for UI demo)
    const demoItems: DetectedFood[] = [
      {
        id: Date.now().toString(),
        name: "Salad rau",
        calories: 80,
        nutrients: { protein: 2, carbs: 8, fat: 4 },
        confidence: 0.79,
      },
    ];

    const t = setTimeout(() => {
      setDetected((d) => [...demoItems, ...d]);
      setIsDetecting(false);
    }, 1200);

    // In a real app, start a websocket or polling to your AI detection service.

    return () => clearTimeout(t);
  }

  function handleClearSession() {
    setDetected([]);
  }

  function renderNutrientBar(n: Nutrients) {
    const total = n.protein + n.carbs + n.fat || 1;
    const p = Math.round((n.protein / total) * 100);
    const c = Math.round((n.carbs / total) * 100);
    const f = 100 - p - c;
    return (
      <div className="w-full h-3 rounded-full overflow-hidden bg-gray-100 flex">
        <div className="h-3" style={{ width: `${c}%` }} />
        <div className="h-3 bg-white/0" style={{ width: `${p}%` }} />
        <div className="h-3" style={{ width: `${f}%` }} />
        {/* Using background colors via utility classes is ideal, but keeping
            generic here so designers can adapt. */}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-gray-50 p-6 font-sans text-slate-800">
      {/* Header */}
      <header className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M4 12h16" stroke="#16a34a" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M12 4v16" stroke="#16a34a" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          </div>
          <div>
            <div className="text-sm text-slate-500">Hệ thống</div>
            <div className="text-lg font-semibold">Đánh giá khẩu phần ăn tự động</div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button className="px-3 py-2 bg-white border rounded-md shadow-sm text-sm">Trợ giúp</button>
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center">NV</div>
            <div className="text-sm">Người dùng</div>
          </div>
        </div>
      </header>

      {/* Main layout */}
      <main className="grid grid-cols-12 gap-6">
        {/* Left: Camera area (col-span 7) */}
        <section className="col-span-7">
          <div className="bg-white rounded-2xl shadow p-4 h-full flex flex-col">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-md font-medium">Camera nhận diện món ăn</h3>
              <div className="text-sm text-slate-500">ESP32-CAM Stream</div>
            </div>

            <div className="flex-1 flex gap-4">
              <div className="flex-1 bg-gray-50 rounded-xl overflow-hidden border border-gray-100 flex items-center justify-center">
                {/* Video element - replace src for ESP32 stream in production */}
                <video
                  ref={videoRef}
                  className="w-full h-full object-cover"
                  playsInline
                  muted
                  autoPlay
                />
              </div>

              <div className="w-44 flex flex-col gap-3">
                <div className="bg-white rounded-xl p-3 shadow-sm border">
                  <div className="text-sm text-slate-500">Trạng thái</div>
                  <div className="mt-2 flex items-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${isDetecting ? 'bg-emerald-400' : 'bg-gray-300'}`} />
                    <div className="text-sm font-medium">{isDetecting ? 'Đang nhận diện' : 'Sẵn sàng'}</div>
                  </div>
                </div>

                <div className="bg-white rounded-xl p-3 shadow-sm border flex-1 flex flex-col">
                  <div className="text-sm text-slate-500">Điều khiển</div>
                  <div className="mt-3 flex flex-col gap-2">
                    <button onClick={handleStartDetection} className="px-3 py-2 bg-emerald-500 text-white rounded-md text-sm">Bắt đầu nhận diện</button>
                    <button onClick={handleClearSession} className="px-3 py-2 bg-white border rounded-md text-sm">Xóa phiên</button>
                    <div className="text-xs text-slate-400">Trong demo, nút sẽ thêm mục mẫu.</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="mt-4 text-xs text-slate-500">Ghi chú: Để dùng ESP32-CAM, thay nguồn video bằng endpoint MJPEG hoặc HLS từ thiết bị của bạn.</div>
          </div>
        </section>

        {/* Right: Info panel (col-span 5) */}
        <aside className="col-span-5">
          <div className="bg-white rounded-2xl shadow p-4 mb-4">
            <h4 className="text-md font-semibold mb-2">Món ăn đang nhận diện</h4>
            <div className="space-y-3">
              {/* show the most recent detected item */}
              {detected.length > 0 ? (
                detected.slice(0, 3).map((item) => (
                  <div key={item.id} className="flex items-center gap-3 p-2 rounded-xl border hover:bg-gray-50 transition">
                    <div className="w-14 h-14 bg-gray-100 rounded-md flex items-center justify-center">{item.thumbnail ? <img src={item.thumbnail} alt={item.name} className="w-full h-full object-cover rounded-md" /> : <svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="12" cy="12" r="10" stroke="#e5e7eb" strokeWidth="1.5" /></svg>}</div>
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <div className="font-medium">{item.name}</div>
                        <div className="text-sm text-slate-500">{Math.round((item.confidence ?? 0) * 100)}%</div>
                      </div>
                      <div className="text-sm text-slate-600">{item.calories} kcal</div>
                      <div className="mt-2">{renderNutrientBar(item.nutrients)}</div>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-sm text-slate-400">Chưa có món ăn nào được nhận diện.</div>
              )}
            </div>
          </div>

          <div className="bg-white rounded-2xl shadow p-4">
            <h4 className="text-md font-semibold mb-2">Tổng hợp phiên</h4>
            <div className="flex items-center justify-between mb-3">
              <div>
                <div className="text-sm text-slate-500">Tổng calo</div>
                <div className="text-2xl font-bold">{totalCalories} kcal</div>
              </div>

              <div className="w-28 h-28 bg-gray-50 rounded-full flex items-center justify-center">
                {/* simple macronutrient mini-chart (textual) */}
                <div className="text-center">
                  <div className="text-sm text-slate-500">Macro</div>
                  <div className="text-sm font-medium">C:{detected.reduce((s, f) => s + f.nutrients.carbs, 0)}g</div>
                  <div className="text-sm font-medium">P:{detected.reduce((s, f) => s + f.nutrients.protein, 0)}g</div>
                  <div className="text-sm font-medium">F:{detected.reduce((s, f) => s + f.nutrients.fat, 0)}g</div>
                </div>
              </div>
            </div>

            <div className="space-y-2 max-h-48 overflow-auto">
              {detected.length === 0 && <div className="text-sm text-slate-400">Không có mục nào trong phiên.</div>}

              {detected.map((item) => (
                <div key={item.id} className="flex items-center justify-between p-2 border rounded-md">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gray-100 rounded-md flex items-center justify-center">{item.name.charAt(0)}</div>
                    <div>
                      <div className="font-medium text-sm">{item.name}</div>
                      <div className="text-xs text-slate-500">{item.calories} kcal</div>
                    </div>
                  </div>
                  <div className="text-sm text-slate-500">{Math.round((item.confidence ?? 0) * 100)}%</div>
                </div>
              ))}
            </div>

            <div className="mt-4 flex gap-2">
              <button className="flex-1 px-3 py-2 bg-emerald-500 text-white rounded-md">Xuất báo cáo</button>
              <button className="px-3 py-2 bg-white border rounded-md" onClick={() => alert('Giả lập: tải xuống CSV')}>Tải CSV</button>
            </div>
          </div>
        </aside>
      </main>

      <footer className="mt-6 text-center text-sm text-slate-400">© 2025 FoodCal - Demo UI</footer>
    </div>
  );
}
