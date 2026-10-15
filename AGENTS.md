# Repository instructions

## Primary workspace

The primary checkout is `D:\ChatGPTLocalProjects\3DMap`. Use this directory for all development, Git changes, application launches, and generated project artifacts. Set the working directory explicitly when the chat is still attached to a different folder.

Do not develop or run this project from the C: drive Codex worktree, and do not create another worktree unless the user explicitly requests one. Create any needed feature branch in the primary checkout, preserving existing local changes.

## Commits and remote updates

After completing each requested set of changes, create a Git commit before reporting completion. Use Conventional Commits format: `<type>[optional scope]: <description>` (for example, `feat: add interactive building explorer`). Keep each commit focused on the completed change.

After each requested set of changes, push the completed commit to `origin` on the current branch before reporting completion. If the branch has no upstream, set it with `git push --set-upstream origin <branch>`. Never force-push or rewrite remote history, and do not include unrelated changes in the push.
