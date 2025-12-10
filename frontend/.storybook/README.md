# Storybook Configuration

## Setup

This Storybook configuration is set up for Next.js 14.2 with i18n support.

### Dependencies

#### webpack 5.101.2
**Required for Next.js 14.2 compatibility**

Next.js 14.2+ uses webpack 5.98.0, which has a breaking change in the `.tap()` method implementation. Storybook 8.0.9 requires webpack 5.101.2+. Installing webpack 5.101.2 explicitly resolves this compatibility issue.

**Error without webpack 5.101.2:**
```
ERROR in main
Module not found: TypeError: Cannot read properties of undefined (reading 'tap')
```

**Reference:**
- [Storybook Issue #32301](https://github.com/storybookjs/storybook/issues/32301)

## Running Storybook

```bash
npm run storybook        # Start dev server on port 6006
npm run build-storybook  # Build static Storybook
npm run chromatic        # Deploy to Chromatic
```

## i18n Support

Storybook is configured with i18next integration for the `tradeSafety` namespace. Use the locale switcher in the toolbar to test different languages (en, ko, ja, zh, es, id).
