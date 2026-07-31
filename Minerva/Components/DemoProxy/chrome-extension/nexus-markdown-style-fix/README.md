# Nexus Markdown Style Fix

This local Chrome extension injects scoped CSS into the Nexus staging app to improve Mira markdown response presentation.

The extension targets only:

```text
https://nexus-cloud-web-stg.bsc.bscal.com/*
```

The CSS is scoped to `.results .vhtml`, which is where the Nexus page renders Mira markdown response HTML in the captured page source.

## Install in Chrome

1. Open Chrome.
2. Navigate to `chrome://extensions`.
3. Turn on `Developer mode` in the top-right corner.
4. Select `Load unpacked`.
5. Select this folder:

   ```text
   /Users/jjacks20/jjacks/Conversational-AI/Minerva/Components/DemoProxy/chrome-extension/nexus-markdown-style-fix
   ```

6. Confirm that `Nexus Markdown Style Fix` appears in the extensions list and is enabled.
7. Open or refresh Nexus:

   ```text
   https://nexus-cloud-web-stg.bsc.bscal.com/
   ```

8. Ask Mira a question that returns headings, bold text, lists, and tables.

## Verify It Is Working

1. In Nexus, right-click a rendered Mira response heading and select `Inspect`.
2. Confirm the selected element is inside a `.vhtml` container.
3. In the `Styles` or `Computed` panel, confirm styles from `nexus-markdown.css` are applied.

Expected visible changes:

- `h2`, `h3`, and `h4` response headings appear larger and bold.
- Paragraph spacing is tighter and more consistent.
- Lists retain bullets or numbers with readable spacing.
- Markdown tables have visible borders, padded cells, and header styling.

## Reload After CSS Changes

If `nexus-markdown.css` changes:

1. Go back to `chrome://extensions`.
2. Find `Nexus Markdown Style Fix`.
3. Select the reload icon on the extension card.
4. Refresh the Nexus page.

## Disable or Remove

To temporarily disable the styling, turn off the extension toggle in `chrome://extensions`.

To remove it, select `Remove` on the extension card.

## Notes

- No admin access or PowerShell usage is required when Chrome allows unpacked extensions.
- Enterprise-managed Chrome installations may block `Developer mode` or unpacked local extensions. That is a browser policy constraint, not an extension issue.
- This extension does not modify API traffic, credentials, or page JavaScript.
