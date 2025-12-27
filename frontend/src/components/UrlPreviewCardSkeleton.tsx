export function UrlPreviewCardSkeleton() {
  return (
    <div className="relative border-l-4 border-base-300 bg-base-100 px-5 py-2">
      <div className="mb-3">
        <div className="skeleton mb-2 h-4 w-3/4"></div>
        <div className="flex items-center gap-2">
          <div className="skeleton h-3 w-20"></div>
          <div className="skeleton h-3 w-16"></div>
        </div>
      </div>
      <div className="flex gap-2">
        <div className="skeleton size-14 rounded"></div>
        <div className="skeleton size-14 rounded"></div>
        <div className="skeleton size-14 rounded"></div>
      </div>
    </div>
  );
}
