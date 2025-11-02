import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Loader2, X, Send, Bot } from 'lucide-react';
import { useChatbotRecipe } from '../hooks/useChatbotRecipe';
import type { RecipeSections } from './Chatbot.type';

const Chatbot: React.FC = () => {
    const [open, setOpen] = useState(false);
    const [query, setQuery] = useState('');
    const [result, setResult] = useState<RecipeSections | null>(null);
    const [multiResults, setMultiResults] = useState<{ title: string; url: string }[] | null>(null);
    const { loading, error, setError, fetchRecipeByQuery, fetchRecipeByUrl } = useChatbotRecipe();

    const handleToggle = () => setOpen((prev) => !prev);

    const handleSelectDish = async (dishUrl: string, dishTitle: string) => {
        setResult(null);
        setMultiResults(null);

        try {
            await new Promise((r) => setTimeout(r, 300));
            const recipe = await fetchRecipeByUrl(dishUrl, dishTitle);
            if (recipe) {
                setMultiResults(null);
                await new Promise((r) => setTimeout(r, 200));
                setResult(recipe);
            }
        } catch (err) {
            console.error(err);
        }
    };


    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setResult(null);
        setMultiResults(null);

        try {
            const { recipe, multiResults: results } = await fetchRecipeByQuery(query);

            if (recipe) {
                setResult(recipe);
            }
            if (results) {
                setMultiResults(results);
            }
        } catch (err) {
            console.error(err);
        }
    };
    return (
        <div className="fixed bottom-6 right-6 z-50">
            {/* Nút mở chatbot */}
            {!open && (
                <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleToggle}
                    className="bg-gradient-to-r from-green-500 to-lime-400 text-white rounded-full shadow-lg p-4 flex items-center gap-2 hover:from-green-600 hover:to-lime-500 transition"
                >
                    <Bot className="w-5 h-5" />
                    <span className="font-medium">Chat món ăn</span>
                </motion.button>
            )}

            {/* Cửa sổ Chatbot */}
            <AnimatePresence>
                {open && (
                    <motion.div
                        initial={{ opacity: 0, y: 0, scale: 0.9 }}
                        animate={{ opacity: 1, y: 0, scale: 1 }}
                        exit={{ opacity: 0, y: 0, scale: 0.9 }}
                        transition={{ duration: 0.25, ease: "easeOut" }}
                        className="w-96 bg-white/95 backdrop-blur-md rounded-2xl shadow-2xl border border-gray-100 p-4 flex flex-col space-y-4 fixed bottom-6 right-6 z-50"
                        style={{ transformOrigin: "bottom right" }}
                    >
                        {/* Header */}
                        <div className="flex justify-between items-center border-b pb-2">
                            <h3 className="font-bold text-lg text-green-700">🍲 Food Recipe Assistant</h3>
                            <button
                                onClick={handleToggle}
                                className="text-gray-500 hover:text-red-500 transition"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        {/* Ô nhập */}
                        <form onSubmit={handleSubmit} className="flex space-x-2">
                            <input
                                type="text"
                                className="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-400 text-sm"
                                placeholder="Nhập tên món ăn (VD: Cơm chiên, Phở bò...)"
                                value={query}
                                onChange={(e) => setQuery(e.target.value)}
                                required
                            />
                            <button
                                type="submit"
                                disabled={loading}
                                className="bg-green-500 hover:bg-green-600 text-white px-3 py-2 rounded-lg transition flex items-center justify-center"
                            >
                                {loading ? <Loader2 className="animate-spin w-4 h-4" /> : <Send className="w-4 h-4" />}
                            </button>
                        </form>

                        {/* Kết quả */}
                        <div className="max-h-80 overflow-y-auto pr-2 space-y-3">
                            {loading && <div className="text-green-600 text-sm flex items-center gap-2"><Loader2 className="animate-spin w-4 h-4" /> Đang tìm kiếm...</div>}
                            {error && <div className="text-red-500 text-sm">{error}</div>}

                            {result && (
                                <motion.div
                                    key="recipe-result"
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0 }}
                                    transition={{ duration: 0.3 }}
                                    className="space-y-4 text-sm leading-relaxed"
                                >
                                    {/* 🏷️ Hiển thị tên món ăn */}
                                    {result.title && (
                                        <div className="text-center border-b border-green-100 pb-2 mb-2">
                                            <h2 className="text-lg font-bold text-green-700 flex items-center justify-center gap-2">
                                                🍛 {result.title}
                                            </h2>
                                        </div>
                                    )}
                                    {result.nguyenlieu && result.nguyenlieu.length > 0 && (
                                        <section>
                                            <h4 className="font-semibold text-green-700 border-l-4 border-green-400 pl-2 mb-1">🥦 Nguyên liệu</h4>
                                            <ul className="list-disc ml-5 space-y-1 text-gray-700">
                                                {result.nguyenlieu.map((item, i) => <li key={i}>{item}</li>)}
                                            </ul>
                                        </section>
                                    )}

                                    {result.soche && result.soche.length > 0 && (
                                        <section>
                                            <h4 className="font-semibold text-green-700 border-l-4 border-green-400 pl-2 mb-1">🔪 Sơ chế</h4>
                                            <ul className="list-disc ml-5 space-y-1 text-gray-700">
                                                {result.soche.map((item, i) => <li key={i}>{item}</li>)}
                                            </ul>
                                        </section>
                                    )}

                                    {result.thuchien && result.thuchien.length > 0 && (
                                        <section>
                                            <h4 className="font-semibold text-green-700 border-l-4 border-green-400 pl-2 mb-1">🔥 Thực hiện</h4>
                                            <ul className="list-disc ml-5 space-y-1 text-gray-700">
                                                {result.thuchien.map((item, i) => <li key={i}>{item}</li>)}
                                            </ul>
                                        </section>
                                    )}

                                    {result.howtouse && result.howtouse.length > 0 && (
                                        <section>
                                            <h4 className="font-semibold text-green-700 border-l-4 border-green-400 pl-2 mb-1">🍽️ Cách dùng</h4>
                                            <ul className="list-disc ml-5 space-y-1 text-gray-700">
                                                {result.howtouse.map((item, i) => <li key={i}>{item}</li>)}
                                            </ul>
                                        </section>
                                    )}

                                    {result.tips && result.tips.length > 0 && (
                                        <section>
                                            <h4 className="font-semibold text-green-700 border-l-4 border-green-400 pl-2 mb-1">💡 Mẹo hay</h4>
                                            <ul className="list-disc ml-5 space-y-1 text-gray-700">
                                                {result.tips.map((item, i) => <li key={i}>{item}</li>)}
                                            </ul>
                                        </section>
                                    )}
                                </motion.div>
                            )}
                            <AnimatePresence mode="wait">
                                {multiResults && !loading && (
                                    <motion.div
                                        key="multi-list"
                                        initial={{ opacity: 0, y: 20 }}
                                        animate={{ opacity: 1, y: 0 }}
                                        exit={{ opacity: 0, y: -10 }}
                                        transition={{ duration: 0.3 }}
                                        className="mt-4"
                                    >
                                        <p className="font-medium">🔍 Tìm thấy nhiều món, bạn muốn chọn món nào?</p>
                                        <ul className="list-disc ml-5 space-y-1 mt-2">
                                            {multiResults.map((item, idx) => (
                                                <li key={idx}>
                                                    <button
                                                        onClick={() => handleSelectDish(item.url, item.title)}
                                                        className="text-blue-600 underline hover:text-blue-800 transition text-left"
                                                    >
                                                        {item.title}
                                                    </button>
                                                </li>
                                            ))}
                                        </ul>
                                    </motion.div>
                                )}
                            </AnimatePresence>

                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

export default Chatbot;
