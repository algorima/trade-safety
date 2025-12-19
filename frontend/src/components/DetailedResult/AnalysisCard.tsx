import clsx from "clsx";

interface AnalysisCardProps {
  title?: string;
  icon?: React.ReactNode;
  variant?: "default" | "error" | "warning" | "success" | "info";
  children: React.ReactNode;
}

const variantStyles = {
  default: "border-base-300",
  error: "border-error bg-error/10",
  warning: "border-warning bg-warning/10",
  success: "border-success bg-success/10",
  info: "border-info bg-info/10",
};

export function AnalysisCard({
  title,
  icon,
  variant = "default",
  children,
}: AnalysisCardProps) {
  if (!children) return null;

  return (
    <div className={clsx("rounded-lg border p-6", variantStyles[variant])}>
      {title && (
        <h2 className="mb-2 flex items-center gap-2 font-bold">
          {title}
          {icon}
        </h2>
      )}
      {children}
    </div>
  );
}
