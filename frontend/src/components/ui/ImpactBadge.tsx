export default function ImpactBadge({ score }: { score: number }) {
  let colorClass = "bg-gray-100 text-gray-600 border-gray-200";
  
  if (score >= 80) colorClass = "bg-red-50 text-red-700 border-red-200";
  else if (score >= 60) colorClass = "bg-orange-50 text-orange-700 border-orange-200";
  else if (score >= 40) colorClass = "bg-blue-50 text-blue-700 border-blue-200";
  else colorClass = "bg-green-50 text-green-700 border-green-200";

  return (
    <span className={`px-2 py-0.5 rounded-md text-[10px] uppercase font-bold border tracking-wider ${colorClass}`}>
      Impact {score}
    </span>
  );
}