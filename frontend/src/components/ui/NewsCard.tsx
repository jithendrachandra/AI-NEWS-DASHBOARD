"use client";

import { useState } from "react";
import { NewsItem, toggleFavorite } from "@/lib/api";
import { Heart, Send, ExternalLink } from "lucide-react";
import BroadcastModal from "./BroadcastModal";

interface Props {
  item: NewsItem;
  onFavoriteChange?: (id: number, isFavorited: boolean) => void;
}

export default function NewsCard({ item, onFavoriteChange }: Props) {
  const [isFavorited, setIsFavorited] = useState<boolean>(
    item.is_favorited ?? false
  );
  const [savingFav, setSavingFav] = useState(false);

  const [isBroadcastOpen, setIsBroadcastOpen] = useState(false);

  const handleFavoriteClick = async () => {
    if (savingFav) return;
    setSavingFav(true);
    try {
      const res = await toggleFavorite(item.id);
      const newState = Boolean(res.is_favorited);
      setIsFavorited(newState);
      onFavoriteChange?.(item.id, newState);
    } catch (e) {
      console.error("Favorite toggle failed", e);
    }
    setSavingFav(false);
  };

  const openBroadcastModal = () => {
    setIsBroadcastOpen(true);
  };

  const closeBroadcastModal = () => {
    setIsBroadcastOpen(false);
  };

  return (
    <>
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 flex flex-col justify-between">
        {/* Top content: tags, title, summary */}
        <div>
          <h2 className="font-semibold text-gray-900 mb-2 line-clamp-2">
            {item.title}
          </h2>
          <p className="text-gray-600 text-sm line-clamp-4">{item.summary}</p>
        </div>

        {/* Footer actions */}
        <div className="mt-4 flex items-center justify-between">
          {/* Left: Broadcast button (opens modal) */}
          <button
            onClick={openBroadcastModal}
            className="flex items-center justify-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded-full transition-colors"
          >
            <Send size={14} />
            Broadcast
          </button>

          {/* Right: View link + Favorite */}
          <div className="flex items-center gap-2">
            {/* View article link */}
            <a
              href={item.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 px-3 py-1 rounded-full text-sm border border-gray-200 text-gray-600 hover:bg-gray-50 transition-colors"
            >
              <ExternalLink size={14} />
              View
            </a>

            {/* Favorite toggle */}
            <button
              onClick={handleFavoriteClick}
              disabled={savingFav}
              className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm border transition-colors ${
                isFavorited
                  ? "bg-pink-50 text-pink-600 border-pink-200"
                  : "bg-white text-gray-500 border-gray-200 hover:bg-gray-50"
              }`}
            >
              <Heart
                size={14}
                className={isFavorited ? "fill-pink-500 text-pink-500" : ""}
              />
              {isFavorited ? "Favorited" : "Favorite"}
            </button>
          </div>
        </div>
      </div>

      {/* Broadcast modal */}
      <BroadcastModal
        isOpen={isBroadcastOpen}
        onClose={closeBroadcastModal}
        newsId={item.id}
        newsTitle={item.title}
      />
    </>
  );
}
