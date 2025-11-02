import { useState } from 'react';

interface RecipeSections {
    title?: string[];
    nguyenlieu?: string[];
    soche?: string[];
    thuchien?: string[];
    howtouse?: string[];
    tips?: string[];
}
interface FetchResult {
    recipe: RecipeSections | null;
    multiResults: { title: string; url: string }[] | null;
}
export function useChatbotRecipe() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const _mapRecipeData = (item: any): RecipeSections => {
        return {
            title: item.title ? [item.title] : [],
            nguyenlieu: item.nguyenlieu || item.ingredients || [],
            soche: item.soche || item.preparation || [],
            thuchien: item.thuchien || item.cookingSteps || [],
            howtouse: item.howtouse || item.howToServe || [],
            tips: item.tips || [],
        };
    };

    const fetchRecipeByQuery = async (query: string): Promise<FetchResult> => {
        setLoading(true);
        setError('');
        try {
            const res = await fetch(
                `http://localhost:8000/api/v1/chatbot/recipe?query=${encodeURIComponent(query)}&isbot=true`
            );
            if (!res.ok) throw new Error('Không tìm thấy món ăn hoặc lỗi server');
            const data = await res.json();

            if (data.status === "only") {
                return {
                    recipe: _mapRecipeData(data.data),
                    multiResults: null,
                };
            } else if (data.status === "multiple") {
                return {
                    recipe: null,
                    multiResults: data.options,
                };
            } else {
                throw new Error(data.message || 'Không tìm thấy dữ liệu phù hợp');
            }
        } catch (err: any) {
            const errorMsg = err.message || 'Lỗi không xác định';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    const fetchRecipeByUrl = async (url: string, title: string): Promise<RecipeSections | null> => {
        setLoading(true);
        setError('');
        try {
            const res = await fetch(
                `http://localhost:8000/api/v1/chatbot/recipe?url=${encodeURIComponent(url)}&isbot=true`
            );
            if (!res.ok) throw new Error('Không tìm thấy món ăn hoặc lỗi server');
            const data = await res.json();

            if (data.status === "only") {
                const mapped = _mapRecipeData(data.data);
                return {
                    ...mapped,
                    title: title ? [title] : mapped.title,
                };
            } else {
                throw new Error(data.message || "Không tìm thấy món ăn phù hợp.");
            }
        } catch (err: any) {
            const errorMsg = err.message || 'Lỗi không xác định';
            setError(errorMsg);
            throw err;
        } finally {
            setLoading(false);
        }
    };

    return { loading, error, setError, fetchRecipeByQuery, fetchRecipeByUrl };
}