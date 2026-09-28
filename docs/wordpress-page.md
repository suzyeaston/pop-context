# WordPress page handoff

## Recommended page

Create a normal WordPress **Page**:

- **Title:** `POP//CONTEXT`
- **Slug:** `pop-context`
- **Public URL:** `https://www.suzyeaston.ca/pop-context/`

The app remains independently deployed through GitHub Pages:

`https://suzyeaston.github.io/pop-context/`

WordPress becomes the shell and clean portfolio URL.

## Block to use

Add **one Custom HTML block** and paste the entire contents of:

`docs/wordpress-embed.html`

## Deployment path

```text
GitHub repo
   ↓ push main
GitHub Actions
   ↓
GitHub Pages
   ↓ iframe
suzyeaston.ca/pop-context/
```

## WordPress checklist

1. Pages → Add New
2. Title: `POP//CONTEXT`
3. Set slug to `pop-context`
4. Choose a full-width / no-sidebar template if your theme offers one
5. Add one **Custom HTML** block
6. Paste `docs/wordpress-embed.html`
7. Preview
8. Publish

Every later push to `main` updates GitHub Pages automatically, so WordPress does not need to be edited for each release.
