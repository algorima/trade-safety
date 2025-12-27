import Image from "next/image";

export interface LinkPreviewData {
  title: string;
  author: string;
  date: string | null;
  images: string[];
  url: string;
  content: string;
}

interface UrlPreviewCardProps {
  data: LinkPreviewData;
}

export function UrlPreviewCard({ data }: UrlPreviewCardProps) {
  const displayImages = data.images.slice(0, 3);
  const hasImages = displayImages.length > 0;

  return (
    <div className="relative border-l-4 border-base-300 bg-base-100 pl-3">
      <div className="mb-3">
        <h3 className="mb-2 text-sm font-bold text-base-content">
          {data.title}
        </h3>
        <div className="flex items-center gap-2 text-xs text-base-content/60">
          <span>{data.author}</span>
          {data.date && <span>{data.date}</span>}
        </div>
      </div>

      {hasImages && (
        <div className="grid grid-cols-3 gap-2">
          {displayImages.map((imageUrl, index) => (
            <div
              key={imageUrl}
              className="relative aspect-square overflow-hidden rounded bg-base-200"
            >
              <Image
                src={imageUrl}
                alt={`Preview ${index + 1}`}
                fill
                className="object-cover"
              />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
