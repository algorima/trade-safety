/**
 * ColorBox component represents a color box with a background color and text.
 * @param {string} color - The color class for the background.
 * @param {string} textColor - The color class for the text.
 * @param {string} children - The text content of the color box.
 */
function ColorBox({
  color,
  textColor,
  children,
}: {
  color: string;
  textColor: string;
  children: string;
}) {
  return (
    <div
      className={`flex size-40 items-center justify-center rounded text-xl font-bold ${color} ${textColor}`}
    >
      {children}
    </div>
  );
}

/**
 * Colors component showcases the color palette used in the design system.
 * It includes all available colors from the daisyUI theme.
 */
export function Colors() {
  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-4">
        <ColorBox color="bg-primary" textColor="text-primary-content">
          Primary
        </ColorBox>
        <ColorBox color="bg-secondary" textColor="text-secondary-content">
          Secondary
        </ColorBox>
        <ColorBox color="bg-neutral" textColor="text-neutral-content">
          Neutral
        </ColorBox>
      </div>
      <div className="flex flex-wrap gap-4">
        <ColorBox color="bg-base-100" textColor="text-base-content">
          Base 100
        </ColorBox>
        <ColorBox color="bg-base-200" textColor="text-base-content">
          Base 200
        </ColorBox>
        <ColorBox color="bg-base-300" textColor="text-base-content">
          Base 300
        </ColorBox>
      </div>
      <div className="flex flex-wrap gap-4">
        <ColorBox color="bg-info" textColor="text-info-content">
          Info
        </ColorBox>
        <ColorBox color="bg-success" textColor="text-success-content">
          Success
        </ColorBox>
        <ColorBox color="bg-warning" textColor="text-warning-content">
          Warning
        </ColorBox>
        <ColorBox color="bg-error" textColor="text-error-content">
          Error
        </ColorBox>
      </div>
    </div>
  );
}
