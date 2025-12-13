const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export interface NewsItem {
  id: number;
  title: string;
  source_id: string;
  summary: string;
  url: string;
  published_at: string;
  impact_score: number;
  sentiment: string;
  category_cluster: string;
  view_count?: number;
  broadcast_count?: number;
}

export interface DashboardStats {
  total_news: number;
  total_sources: number;
  avg_impact_score: number;
}

export async function fetchNews(minImpact: number = 0, category?: string) {
  try {
    const params = new URLSearchParams({
      min_impact: minImpact.toString(),
      limit: "50"
    });
    
    if (category && category !== "all") {
      params.append("category", category);
    }
    
    const res = await fetch(`${API_URL}/news/?${params}`, {
      cache: "no-store",
    });
    
    if (!res.ok) throw new Error(`Error fetching news: ${res.statusText}`);
    return await res.json();
  } catch (error) {
    console.error("Fetch News Error:", error);
    return [];
  }
}

export async function searchNews(query: string) {
  try {
    const res = await fetch(`${API_URL}/news/search`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, limit: 20 }),
    });
    if (!res.ok) throw new Error("Search failed");
    return await res.json();
  } catch (error) {
    console.error("Search Error:", error);
    return [];
  }
}

export async function broadcastNews(id: number, platform: string) {
  const res = await fetch(`${API_URL}/broadcast/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ news_item_id: id, platform }),
  });
  return await res.json();
}

export async function toggleFavorite(id: number) {
  const res = await fetch(`${API_URL}/news/${id}/favorite`, {
    method: "POST",
  });
  return await res.json();
}

export async function getFavorites() {
  try {
    const res = await fetch(`${API_URL}/news/favorites`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch favorites");
    return await res.json();
  } catch (error) {
    console.error("Favorites Error:", error);
    return [];
  }
}

export async function getCategories() {
  try {
    const res = await fetch(`${API_URL}/news/categories/list`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch categories");
    return await res.json();
  } catch (error) {
    console.error("Categories Error:", error);
    return [];
  }
}

export async function getDashboardStats(): Promise<DashboardStats> {
  try {
    const res = await fetch(`${API_URL}/news/stats/dashboard`, {
      cache: "no-store",
    });
    if (!res.ok) throw new Error("Failed to fetch stats");
    return await res.json();
  } catch (error) {
    console.error("Stats Error:", error);
    return { total_news: 0, total_sources: 0, avg_impact_score: 0 };
  }
}