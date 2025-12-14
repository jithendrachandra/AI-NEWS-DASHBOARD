"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/ui/Sidebar";
import NewsCard from "@/components/ui/NewsCard";
import { getFavorites, NewsItem } from "@/lib/api";
import { RefreshCw } from "lucide-react";

export default function FavoritesPage() {
  const [favorites, setFavorites] = useState<NewsItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadFavorites = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getFavorites();
      setFavorites(data);
    } catch (e) {
      console.error(e);
      setError("Failed to load favorites");
    }
    setLoading(false);
  };

  useEffect(() => {
    loadFavorites();
  }, []);

  const handleFavoriteChange = (id: number, isFavorited: boolean) => {
    if (!isFavorited) {
      setFavorites((prev) => prev.filter((n) => n.id !== id));
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <header className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">
              Favorites
            </h1>
            <p className="text-gray-500 mt-1">
              Only your saved AI news items are shown here.
            </p>
          </div>
          <button
            onClick={loadFavorites}
            className="p-2 text-gray-500 hover:bg-gray-200 rounded-full transition-colors"
            title="Refresh Favorites"
          >
            <RefreshCw size={20} />
          </button>
        </header>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {loading ? (
          <div className="flex flex-col items-center justify-center py-32 text-gray-400">
            <RefreshCw className="animate-spin mb-4" size={32} />
            <p>Loading your favorites...</p>
          </div>
        ) : favorites.length === 0 ? (
          <div className="text-center py-20 border-2 border-dashed border-gray-200 rounded-xl">
            <p className="text-gray-500 text-lg">No favorites yet.</p>
            <p className="text-gray-400 text-sm mt-2">
              Go to the main feed and click “Favorite” on any article.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-10">
            {favorites.map((item) => (
              <NewsCard
                key={item.id}
                item={{ ...item, is_favorited: true }}
                onFavoriteChange={handleFavoriteChange}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
