import Image from "next/image";

import type { LinkPreviewData } from "@/types";

interface UrlPreviewCardProps {
  data: LinkPreviewData;
}

export function UrlPreviewCard({ data }: UrlPreviewCardProps) {
  const displayImages = data.images.slice(0, 3);
  const hasImages = displayImages.length > 0;

  return (
    <div className="relative border-l-4 border-base-300 bg-base-100 px-5 py-2">
      <div className="mb-3">
        <h3 className="mb-2 text-sm font-bold text-base-content">
          {data.title}
        </h3>
        <div className="flex items-center gap-2 text-sm text-base-content/60">
          <span>{data.author}</span>
          {data.date && <span>{data.date}</span>}
        </div>
      </div>

      {hasImages && (
        <div className="flex gap-2">
          {displayImages.map((imageUrl, index) => (
            <div
              key={`${imageUrl}-${index}`}
              className="relative size-14 overflow-hidden rounded bg-base-200"
            >
              <Image
                src={imageUrl}
                alt={`Image ${index + 1} from post by ${data.author}`}
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
