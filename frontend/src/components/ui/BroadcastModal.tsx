"use client";

import { useState } from "react";
import { X, Share2, Linkedin, Mail, MessageSquare } from "lucide-react";
import { broadcastNews } from "@/lib/api";

interface BroadcastModalProps {
  isOpen: boolean;
  onClose: () => void;
  newsId: number;
  newsTitle: string;
}

export default function BroadcastModal({ isOpen, onClose, newsId, newsTitle }: BroadcastModalProps) {
  const [platform, setPlatform] = useState("linkedin");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");

  if (!isOpen) return null;

  const handleBroadcast = async () => {
    setLoading(true);
    setStatus("idle");
    try {
      await broadcastNews(newsId, platform);
      setStatus("success");
      setTimeout(() => {
        onClose();
        setStatus("idle");
      }, 1500); // Close after 1.5s on success
    } catch (error) {
      console.error(error);
      setStatus("error");
    }
    setLoading(false);
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 backdrop-blur-sm">
      <div className="bg-white rounded-xl w-full max-w-md p-6 shadow-2xl transform transition-all scale-100">
        
        {/* Header */}
        <div className="flex justify-between items-center mb-6 border-b border-gray-100 pb-4">
          <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
            <Share2 className="text-blue-600" size={20} />
            Broadcast Intelligence
          </h3>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600 transition-colors">
            <X size={24} />
          </button>
        </div>

        {/* Content */}
        <div className="mb-6">
          <p className="text-sm text-gray-500 mb-2">Selected Article:</p>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg text-sm font-medium text-slate-800 line-clamp-2">
            {newsTitle}
          </div>
        </div>

        {/* Platform Selection */}
        <div className="grid grid-cols-3 gap-3 mb-8">
          <button
            onClick={() => setPlatform("linkedin")}
            className={`flex flex-col items-center gap-2 p-3 rounded-xl border transition-all ${
              platform === "linkedin" ? "border-blue-600 bg-blue-50 text-blue-700" : "border-gray-200 hover:border-blue-300"
            }`}
          >
            <Linkedin size={24} />
            <span className="text-xs font-semibold">LinkedIn</span>
          </button>
          
          <button
            onClick={() => setPlatform("email")}
            className={`flex flex-col items-center gap-2 p-3 rounded-xl border transition-all ${
              platform === "email" ? "border-blue-600 bg-blue-50 text-blue-700" : "border-gray-200 hover:border-blue-300"
            }`}
          >
            <Mail size={24} />
            <span className="text-xs font-semibold">Email</span>
          </button>
          
          <button
            onClick={() => setPlatform("whatsapp")}
            className={`flex flex-col items-center gap-2 p-3 rounded-xl border transition-all ${
              platform === "whatsapp" ? "border-blue-600 bg-blue-50 text-blue-700" : "border-gray-200 hover:border-blue-300"
            }`}
          >
            <MessageSquare size={24} />
            <span className="text-xs font-semibold">WhatsApp</span>
          </button>
        </div>

        {/* Actions */}
        <div className="flex gap-3">
          <button
            onClick={onClose}
            className="flex-1 py-2.5 border border-gray-300 text-gray-700 rounded-lg font-medium hover:bg-gray-50 transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleBroadcast}
            disabled={loading || status === "success"}
            className={`flex-1 py-2.5 rounded-lg font-medium text-white transition-all flex items-center justify-center gap-2 ${
              status === "success" 
                ? "bg-green-600 hover:bg-green-700" 
                : "bg-blue-600 hover:bg-blue-700"
            } disabled:opacity-70 disabled:cursor-not-allowed`}
          >
            {loading ? (
              <span className="animate-pulse">Sending...</span>
            ) : status === "success" ? (
              "Sent Successfully!"
            ) : status === "error" ? (
              "Failed. Retry?"
            ) : (
              "Broadcast Now"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}