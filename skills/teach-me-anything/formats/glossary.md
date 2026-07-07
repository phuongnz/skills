# Glossary format

The **glossary** is the workspace's shared vocabulary — the canonical name and meaning for every term the topic uses. Once it exists, every lesson holds to it, so the whole workspace speaks one language. It is the most-reopened reference in the workspace.

This is the Markdown that goes inside the `<script type="text/markdown">` block of `glossary.html`.

## Shape

```markdown
# Glossary: <topic>

### <Term>
<A plain, direct definition — what it is, in one or two sentences. Define precisely;
save any metaphor for the intuition around it, never for the definition itself.>
_See also:_ <related terms> · _First met in:_ <lesson link, if any>

### <Term>
...
```

## Rules

- **One canonical name per idea.** If the field uses several, pick one for the workspace, note the others as aliases, and use the canonical one everywhere.
- **Define, don't explain.** A glossary entry pins down what a term *is*. Keep worked intuition and metaphor in the lessons.
- Add a term the first time a lesson needs it, and link the lesson to the entry.
- Keep entries alphabetical or grouped by theme — whatever makes lookup fastest for this topic.
- When a definition changes, update it here first; the lessons defer to the glossary, not the other way round.
