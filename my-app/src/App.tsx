import "./App.css";
import NutriVision from "./components/NutriVision";
import RecipeDetails from "./components/RecipeDetails";
import Chatbot from "./components/Chatbot";
import { useState } from "react";
import { useRecipe } from "./hooks/useRecipe";

function App() {
  const [selectedFood, setSelectedFood] = useState<any>(null);
  const { recipeData, isLoading, fetchRecipe } = useRecipe();

  const handleSelectFood = async (food: any) => {
    setSelectedFood(food);
    await fetchRecipe(food.name);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-sky-50 via-white to-emerald-50 text-gray-800 flex flex-col">
      {/* Header */}
      <header className="py-2 text-center bg-white/70 backdrop-blur-md shadow-sm border-b border-gray-100">
        <h1 className="text-3xl font-bold tracking-tight text-emerald-700 drop-shadow-sm">
          🍽️ AI Food Recognition & Smart Dining Assistant
        </h1>
        <p className="text-gray-600 mt-1">
          Phân tích và gợi ý cửa hàng ăn dựa trên hình ảnh món ăn
        </p>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col items-center justify-start py-2 px-0">
        <div className="w-full space-y-8">
          <section className="bg-white/80 backdrop-blur-md rounded-3xl mx-2 p-8 shadow-lg border border-gray-100 transition-all duration-300 hover:shadow-xl">
            <NutriVision onSelectFood={handleSelectFood} />
          </section>
        </div>
      </main>

      {/* Modal */}
      {selectedFood && (
        <>
          <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 transition-opacity duration-300"
            onClick={() => setSelectedFood(null)}
          />

          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 overflow-y-auto">
            <div className="bg-white rounded-3xl shadow-2xl max-w-5xl w-full my-8">
              {/* Header */}
              <div className="flex justify-between items-center p-6 border-b border-gray-100">
                <h3 className="text-2xl font-bold text-emerald-700">
                  🍳 {selectedFood.name}
                </h3>
                <button
                  onClick={() => setSelectedFood(null)}
                  className="text-gray-500 hover:text-gray-700 transition-colors p-1 hover:bg-gray-100 rounded-lg"
                >
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                  </svg>
                </button>
              </div>

              {/* Body */}
              <div className="p-6 overflow-y-auto" style={{ maxHeight: "calc(100vh - 220px)" }}>
                {isLoading ? (
                  <div className="text-center py-8">
                    <div className="inline-block animate-spin">⏳</div>
                    <p className="text-gray-600 mt-2">Đang tải công thức...</p>
                  </div>
                ) : (
                  <RecipeDetails
                    nguyenlieu={recipeData.nguyenlieu}
                    soche={recipeData.soche}
                    thuchien={recipeData.thuchien}
                    howtouse={recipeData.howtouse}
                    tips={recipeData.tips}
                  />
                )}
              </div>

              {/* Footer */}
              <div className="p-6 border-t border-gray-100 flex justify-end gap-3">
                <button
                  onClick={() => setSelectedFood(null)}
                  className="px-8 py-2 bg-emerald-500 hover:bg-emerald-600 text-white font-medium rounded-lg transition-colors"
                >
                  Đóng
                </button>
              </div>
            </div>
          </div>
        </>
      )}

      {/* Chatbot */}
      <div className="fixed bottom-6 right-6 z-50">
        <Chatbot />
      </div>

      {/* Footer */}
      <footer className="py-6 text-center text-sm text-gray-500 bg-white/60 backdrop-blur-md border-t border-gray-100">
        © {new Date().getFullYear()} NutriVision – Built with ❤️ Nguyen Huu Minh Vu & Than Duc Nhat Tan
      </footer>
    </div>
  );
}

export default App;