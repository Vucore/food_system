import './App.css'
import NutriVision from './components/NutriVision';
import Chatbot from './components/Chatbot';

function App() {
  return (
    <>
      <div className="max-w-7xl mx-auto space-y-8">
        <section className="bg-white rounded-lg p-6 shadow-sm">
          <h2 className="text-xl font-semibold mb-4">Food Calorie Rating System</h2>
          <NutriVision />
        </section>
      </div>
      <Chatbot />
    </>
  );
}

export default App;
