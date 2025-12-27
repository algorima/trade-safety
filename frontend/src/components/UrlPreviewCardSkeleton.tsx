export function UrlPreviewCardSkeleton() {
  return (
    <div className="mx-4 mb-4 space-y-3 border-l-4 border-base-300 bg-base-100 pl-3">
      <div className="space-y-2">
        <div className="skeleton h-4 w-3/4"></div>
        <div className="flex items-center gap-2">
          <div className="skeleton h-3 w-20"></div>
          <div className="skeleton h-3 w-16"></div>
        </div>
      </div>
      <div className="grid grid-cols-3 gap-2">
        <div className="skeleton aspect-square"></div>
        <div className="skeleton aspect-square"></div>
        <div className="skeleton aspect-square"></div>
      </div>
    </div>
  );
}
