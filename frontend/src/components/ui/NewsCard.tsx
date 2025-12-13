"use client";

import { useState } from "react";
import { NewsItem } from "@/lib/api";
import ImpactBadge from "./ImpactBadge";
import BroadcastModal from "./BroadcastModal";
import { Share2, ExternalLink, Clock, Eye } from "lucide-react";
import { formatDistanceToNow } from "date-fns";

export default function NewsCard({ item }: { item: NewsItem }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const getSentimentColor = (sentiment: string) => {
    const s = sentiment?.toLowerCase() || "neutral";
    if (s.includes("positive")) return "text-green-600 bg-green-50 border-green-200";
    if (s.includes("negative")) return "text-red-600 bg-red-50 border-red-200";
    return "text-gray-600 bg-gray-50 border-gray-200";
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      "Research": "bg-purple-100 text-purple-700",
      "Product": "bg-blue-100 text-blue-700",
      "Business": "bg-green-100 text-green-700",
      "Policy": "bg-orange-100 text-orange-700",
      "General": "bg-gray-100 text-gray-700"
    };
    return colors[category] || colors["General"];
  };

  return (
    <>
      <div className="group bg-white border border-gray-200 rounded-xl p-5 hover:shadow-xl transition-all duration-300 flex flex-col h-full">
        {/* Header with badges */}
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center gap-2 flex-wrap">
            <ImpactBadge score={item.impact_score || 0} />
            <span className={`px-2 py-0.5 rounded-md text-[10px] font-semibold border ${getSentimentColor(item.sentiment)}`}>
              {item.sentiment || "Neutral"}
            </span>
          </div>
          <span className="text-xs text-gray-500 font-medium px-2 py-1 bg-gray-100 rounded">
            {item.source_id || "Unknown"}
          </span>
        </div>

        {/* Category Badge */}
        {item.category_cluster && (
          <div className="mb-2">
            <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-semibold ${getCategoryColor(item.category_cluster)}`}>
              {item.category_cluster}
            </span>
          </div>
        )}

        {/* Title */}
        <h3 className="font-bold text-gray-900 text-base mb-2 line-clamp-2 group-hover:text-blue-600 transition-colors">
          {item.title}
        </h3>

        {/* Summary */}
        <p className="text-sm text-gray-600 mb-3 line-clamp-3 flex-grow">
          {item.summary || "No summary available."}
        </p>

        {/* Metadata */}
        <div className="flex items-center justify-between gap-2 text-xs text-gray-500 mb-3">
          <div className="flex items-center gap-1">
            <Clock size={12} />
            <span>
              {item.published_at 
                ? formatDistanceToNow(new Date(item.published_at), { addSuffix: true })
                : "Unknown date"}
            </span>
          </div>
          {(item.view_count && item.view_count > 0) && (
            <div className="flex items-center gap-1">
              <Eye size={12} />
              <span>{item.view_count} views</span>
            </div>
          )}
        </div>

        {/* Footer Actions */}
        <div className="flex items-center gap-2 pt-4 border-t border-gray-100">
          <button 
            onClick={() => setIsModalOpen(true)}
            className="flex-1 flex items-center justify-center gap-2 text-xs font-medium bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Share2 size={14} /> Broadcast
          </button>
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-2 text-xs font-medium bg-gray-100 text-gray-700 py-2 px-3 rounded-lg hover:bg-gray-200 transition-colors"
          >
            <ExternalLink size={14} />
          </a>
        </div>
      </div>

      {/* Broadcast Modal */}
      <BroadcastModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        newsId={item.id} 
        newsTitle={item.title} 
      />
    </>
  );
}

