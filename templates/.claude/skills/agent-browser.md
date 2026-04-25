---
name: agent-browser
description: "Test web applications using Chrome DevTools MCP — navigate, fill forms, verify content"
---

# Browser Testing Skill

## When to Use

When you need to interact with a web application in the browser — filling forms, clicking buttons, verifying page content, checking for errors. Use this skill for manual validation (Level 4 of the validation pyramid).

## Prerequisites

- Chrome DevTools MCP server running and configured
- Target application running locally (default: `http://localhost:3000`)

## Process

### 1. Navigate

Use the Chrome DevTools MCP to navigate to the target URL.

```
Navigate to http://localhost:3000
```

### 2. Inspect

Take a screenshot or snapshot of the page to understand the current state before interacting.

```
Take a screenshot of the current page
```

### 3. Interact

Fill form fields, click buttons, submit forms using the MCP tools:

- **Fill fields:** Target by label text, placeholder, or CSS selector
- **Click buttons:** Target by button text or CSS selector
- **Wait:** Allow time for page transitions or async operations

### 4. Verify

After each interaction:

- Take a screenshot to confirm visual state
- Check the browser console for JavaScript errors
- Verify expected content appears on the page
- Check network requests completed successfully

## Example: Testing an RSVP Form

```
1. Navigate to http://localhost:3000/rsvp
2. Take a screenshot — verify the form is visible
3. Fill in "Name" field with "Jane Doe"
4. Fill in "Email" field with "jane@example.com"
5. Fill in "Number of Guests" field with "2"
6. Click the "Submit RSVP" button
7. Take a screenshot — verify confirmation message appears
8. Navigate to http://localhost:3000/attendees
9. Take a screenshot — verify "Jane Doe" appears in the attendee list
```

## Error Handling

- **Page doesn't load:** Check that the server is running (`npm start` or equivalent)
- **Form submission fails:** Check browser console for error messages
- **Element not found:** Take a screenshot to see the actual page state — the selector may be wrong
- **Timeout:** The page may still be loading — wait and retry once
- **MCP not available:** Fall back to manual testing steps (curl for API, browser instructions for UI)

## Tips

- Always take a screenshot BEFORE and AFTER interactions for comparison
- Check the console after every page load — errors there often explain UI issues
- If a form has validation, test with both valid and invalid data
- Test the happy path first, then edge cases
