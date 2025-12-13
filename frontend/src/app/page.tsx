"use client";

import { useEffect, useState } from "react";
import { fetchNews, searchNews, NewsItem } from "@/lib/api";
import NewsCard from "@/components/ui/NewsCard";
import Sidebar from "@/components/ui/Sidebar";
import { Search, RefreshCw } from "lucide-react";

export default function Dashboard() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);

  // Load initial data
  useEffect(() => {
    loadNews();
  }, []);

  const loadNews = async () => {
    setLoading(true);
    try {
      const data = await fetchNews();
      setNews(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Use Semantic Search if query exists, else regular fetch
      const data = query ? await searchNews(query) : await fetchNews();
      setNews(data);
    } catch (e) {
      console.error(e);
    }
    setLoading(false);
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">AI Intelligence Feed</h1>
            <p className="text-gray-500 mt-1">Real-time analysis from 20+ top sources.</p>
          </div>
          
          <div className="flex items-center gap-4">
             <button 
              onClick={loadNews} 
              className="p-2 text-gray-500 hover:bg-gray-200 rounded-full transition-colors"
              title="Refresh Feed"
            >
              <RefreshCw size={20} />
            </button>

            <form onSubmit={handleSearch} className="relative group">
              <Search className="absolute left-3 top-2.5 text-gray-400 group-focus-within:text-blue-500" size={18} />
              <input 
                type="text" 
                placeholder="Semantic Search (e.g. 'LLM Scaling')" 
                className="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-full w-80 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none shadow-sm transition-all"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </form>
          </div>
        </header>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-32 text-gray-400">
            <RefreshCw className="animate-spin mb-4" size={32} />
            <p>Analyzing global intelligence...</p>
          </div>
        ) : news.length === 0 ? (
          <div className="text-center py-20 text-gray-500">
            <p>No news found matching your criteria.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-6 pb-10">
            {news.map((item) => (
              <NewsCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}