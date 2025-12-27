interface SectionContentProps {
  title: string;
  content: string;
}

export function SectionContent({ title, content }: SectionContentProps) {
  return (
    <div className="text-neutral">
      <h3 className="mb-1 break-keep text-lg font-semibold">{title}</h3>
      <p className="break-keep">{content}</p>
    </div>
  );
}
