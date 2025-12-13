"use client";

import { useEffect, useState } from "react";
import { fetchNews, searchNews, NewsItem, getCategories, getDashboardStats, DashboardStats } from "@/lib/api";
import NewsCard from "@/components/ui/NewsCard";
import Sidebar from "@/components/ui/Sidebar";
import StatsCard from "@/components/ui/StatsCard";
import CategoryFilter from "@/components/ui/CategoryFilter";
import { Search, RefreshCw, TrendingUp, Database, Target } from "lucide-react";

export default function Dashboard() {
  const [news, setNews] = useState<NewsItem[]>([]);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [stats, setStats] = useState<DashboardStats>({ total_news: 0, total_sources: 0, avg_impact_score: 0 });

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    setLoading(true);
    try {
      const [newsData, categoriesData, statsData] = await Promise.all([
        fetchNews(),
        getCategories(),
        getDashboardStats()
      ]);
      setNews(newsData);
      setCategories(categoriesData);
      setStats(statsData);
    } catch (e) {
      console.error(e);
      setError("Failed to load data");
    }
    setLoading(false);
  };

  const loadNews = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchNews(0, selectedCategory);
      setNews(data);
    } catch (e) {
      console.error(e);
      setError("Failed to load news");
    }
    setLoading(false);
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = query ? await searchNews(query) : await fetchNews(0, selectedCategory);
      setNews(data);
    } catch (e) {
      console.error(e);
      setError("Search failed");
    }
    setLoading(false);
  };

  const handleCategoryChange = async (category: string) => {
    setSelectedCategory(category);
    setLoading(true);
    setError(null);
    try {
      const data = await fetchNews(0, category === "all" ? undefined : category);
      setNews(data);
    } catch (e) {
      console.error(e);
      setError("Failed to filter by category");
    }
    setLoading(false);
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="ml-64 flex-1 p-8">
        {/* Header */}
        <header className="mb-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 tracking-tight">AI Intelligence Feed</h1>
              <p className="text-gray-500 mt-1">Real-time analysis powered by HuggingFace models</p>
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
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <StatsCard 
              title="Total Articles" 
              value={stats.total_news}
              icon={Database}
              color="bg-blue-100 text-blue-600"
            />
            <StatsCard 
              title="Active Sources" 
              value={stats.total_sources}
              icon={TrendingUp}
              color="bg-green-100 text-green-600"
            />
            <StatsCard 
              title="Avg Impact Score" 
              value={stats.avg_impact_score}
              icon={Target}
              color="bg-purple-100 text-purple-600"
            />
          </div>

          {/* Category Filter */}
          <CategoryFilter 
            categories={categories}
            selected={selectedCategory}
            onChange={handleCategoryChange}
          />
        </header>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-4">
            {error}
          </div>
        )}

        {/* News Grid */}
        {loading ? (
          <div className="flex flex-col items-center justify-center py-32 text-gray-400">
            <RefreshCw className="animate-spin mb-4" size={32} />
            <p>Analyzing global intelligence...</p>
          </div>
        ) : news.length === 0 ? (
          <div className="text-center py-20 border-2 border-dashed border-gray-200 rounded-xl">
            <p className="text-gray-500 text-lg">No news found matching your criteria.</p>
            <p className="text-gray-400 text-sm mt-2">Try adjusting your filters or search query.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 pb-10">
            {news.map((item) => (
              <NewsCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}