import Link from "next/link";
import { LayoutDashboard, Star, Settings, Activity } from "lucide-react";

export default function Sidebar() {
  return (
    <div className="w-64 h-screen bg-slate-900 text-white p-4 fixed left-0 top-0 flex flex-col shadow-xl z-10">
      <div className="flex items-center gap-2 mb-10 px-2">
        <Activity className="text-blue-500" />
        <h1 className="text-xl font-bold">AI News Engine</h1>
      </div>
      
      <nav className="space-y-2 flex-1">
        <Link href="/" className="flex items-center gap-3 p-3 hover:bg-slate-800 rounded-lg transition-colors text-slate-300 hover:text-white">
          <LayoutDashboard size={20} />
          <span>Dashboard</span>
        </Link>
        <Link href="/favorites" className="flex items-center gap-3 p-3 hover:bg-slate-800 rounded-lg transition-colors text-slate-300 hover:text-white">
          <Star size={20} />
          <span>Favorites</span>
        </Link>
      </nav>

      <div className="pt-4 border-t border-slate-800">
        <div className="flex items-center gap-3 p-3 hover:bg-slate-800 rounded-lg opacity-60 cursor-not-allowed">
          <Settings size={20} />
          <span>Settings</span>
        </div>
      </div>
    </div>
  );
}