# Notes for Claude Code sessions

- Read `RELEASING.md` first for any release, tag, or BBS publishing task.
- Commit release work directly to `main`; this repository does not use pull
  requests. Do not rewrite `main` history without being asked.
- Layout on `main`: release files (README, CHANGELOG, SOURCES.txt,
  BBSLIST.TEXT, LISA_INSTALL.TXT, FLOPPY_CHECKLIST.txt, `.dc42` images) at
  the root; Pascal sources and helper scripts under `sources/`.
- Keep old release images and `sources/fmt_text.py`; never delete them
  during a release.
- Tags are `v<ver>` on the head of `main`. Tag pushes fail with 403 from a
  Claude Code web session, so hand the user the PC commands in
  `RELEASING.md` instead of retrying.
- The combined LISACom + Atkinsonpoint floppy is committed to both this
  repository and GyroPilot/AtkinsonPoint as the same file.
