# Releasing LISACom and publishing to The Apple Lisa BBS

Working notes from the 1.7 release (September 2026). Read this before cutting
the next release. It covers both GitHub repositories and the BBS file areas.
It is also the memory for Claude Code sessions that help with a release.

## The two repositories

| Repository | Holds | Layout on `main` |
| --- | --- | --- |
| GyroPilot/Apple-LISACom | LISACom tool, sources, release floppies | Release files at the root, Pascal sources and helper scripts in `sources/` |
| GyroPilot/AtkinsonPoint | LISA Slide Show (Atkinsonpoint), PIX packs, combined floppy | Everything flat at the root |

Apple-LISACom root: `README.md`, `CHANGELOG.md`, `SOURCES.txt`, `BBSLIST.TEXT`,
`LISA_INSTALL.TXT`, `FLOPPY_CHECKLIST.txt`, the release `.dc42` images.
Apple-LISACom `sources/`: `LMX-MAIN.TEXT`, `LMX-GLOBALS.TEXT`, `LMX-ALERTS.TEXT`,
`LMX-MAKE.TEXT`, the `LMX*17.TEXT` Lisa-formatted copies, `fix_dc42.py`,
`fmt_text.py`.

Old release images are kept, not deleted. The 1.1 combined image
`LISAComV1_1_AtkinsonPoint_v1_1_Image.dc42` stays in Apple-LISACom.

The combined floppy (LISACom + Atkinsonpoint + starter slides + BBSLIST.TEXT)
is committed to BOTH repositories, byte for byte the same file.

## Release kit

A release arrives as a zip named `lisacom_<ver>_release.zip` containing the
README, CHANGELOG, SOURCES.txt, BBSLIST.TEXT, LISA_INSTALL.TXT,
FLOPPY_CHECKLIST.txt, FILES_BBS_LINES.txt, ANNOUNCE_LisaList2.txt, the
`.dc42` images and a `sources/` folder. `FILES_BBS_LINES.txt` holds the exact
description lines for the BBS file areas.

## Cutting a release on GitHub

1. Copy the kit files into the layout above, replacing the previous LMX
   sources. Keep the older images and `fmt_text.py`.
2. Commit directly to `main` (no pull request is used in these repositories).
   Commit message style: `LISACom 1.7: working volume, real modem hang-up,
   bookmarks beside the tool`.
3. Push `main`.
4. Tag the release `v<ver>` (with the leading v, for example `v1.7`) on the
   head of `main`, and push the tag.
5. Copy the combined `.dc42` into AtkinsonPoint's root, commit to `main`
   there as well, push. No tag in AtkinsonPoint.

### Tags cannot be pushed from a Claude Code web session

The session's GitHub credential can push branches but a tag push is refused
with HTTP 403. Create the tag from a PC clone instead (PowerShell or Git
Bash on Windows):

```
cd $HOME
git clone https://github.com/GyroPilot/Apple-LISACom.git   # first time only
cd Apple-LISACom
git fetch origin main
git tag v1.7 origin/main
git push origin v1.7
```

Or make a release at https://github.com/GyroPilot/Apple-LISACom/releases/new
and type the new tag name there; publishing creates the tag.

To move a tag that was put on the wrong commit:

```
git tag -f v1.7 origin/main
git push --force origin v1.7
```

To delete a stray tag: `git push origin :refs/tags/<name>`.

## Publishing to The Apple Lisa BBS

The board is Synchronet on a Raspberry Pi, reachable as
`theapplelisabbs.duckdns.org` (telnet port 1983 for callers, SSH for admin).
Admin login is done with Tera Term. Synchronet lives under `/sbbs` and the
file-area directories are owned by the admin login user, NOT by a user named
`sbbs` (there is no such user; `chown sbbs:sbbs` fails).

File areas used for releases:

| DIRCODE | Directory | What goes there |
| --- | --- | --- |
| IMG_RELEASES | `/sbbs/dirs/images/releases/` | Release `.dc42` images |
| SW_SOURCE | `/sbbs/dirs/software/source/` | `LISACOM_<ver>_SRC.zip` |
| SW_TOOLS | `/sbbs/dirs/software/tools/` | `BBSLIST.TEXT`, `LISA_INSTALL.TXT` |

### Step 1: get the files onto the Pi (Tera Term)

With the SSH session open in Tera Term: File > SSH SCP..., "From:" pick the
file on the PC, leave "To:" empty, Send. One file per Send. Dragging a file
from Explorer onto the Tera Term window and choosing SCP does the same. Files
land in the login user's home directory.

Do not run `scp` or `cd C:\...` inside the Pi shell; those are PC commands.

### Step 2: move into the file areas and fix ownership

`sudo` asks for the login user's own password; nothing is echoed while typing.

```
ls -l ~/LISACOM_1_7*.dc42 ~/BBSLIST.TEXT          # confirm they arrived
sudo cp ~/LISACOM_1_7.dc42 ~/LISACOM_1_7_ATKINSONPOINT_1_1.dc42 /sbbs/dirs/images/releases/
sudo cp ~/BBSLIST.TEXT /sbbs/dirs/software/tools/
ls -l /sbbs/dirs/images/releases/ | head           # see who owns the older files
sudo chown <owner>:<owner> /sbbs/dirs/images/releases/LISACOM_1_7*.dc42 /sbbs/dirs/software/tools/BBSLIST.TEXT
```

`<owner>` is whatever the older files in that directory show (the admin login
user). Files copied with `sudo cp` arrive as root and must be chowned.

### Step 3: describe and import

Append the lines from the kit's `FILES_BBS_LINES.txt` to `FILES.BBS` in each
directory, then import. Run as the login user, no `sudo -u`.

```
cd /sbbs/dirs/images/releases
cat >> FILES.BBS <<'EOT'
LISACOM_1_7_ATKINSONPOINT_1_1.dc42  LISACom 1.7 + LISA Slide Show 1.1 + 9 starter slides on one floppy - the combined release disk
LISACOM_1_7.dc42        LISACom 1.7 - Lisa terminal + XMODEM/YMODEM tool. Working volume, real hang-up, bookmarks beside the tool. LOS 3.x, tool 419306
EOT
/sbbs/exec/jsexec addfiles.js IMG_RELEASES -from=Lisaadmin -update FILES.BBS

cd /sbbs/dirs/software/tools
cat >> FILES.BBS <<'EOT'
BBSLIST.TEXT            LISACom bookmark file - 11 boards, LISA BBS first. Save beside LISACom (RETURN at Save as)
EOT
/sbbs/exec/jsexec addfiles.js SW_TOOLS -from=Lisaadmin -update FILES.BBS
```

Then call the board and check Floppy Images > Releases and Software > Tools.

File names on the BBS and the Lisa: underscores, one period
(`LISACOM_1_7.dc42`). See `FLOPPY_CHECKLIST.txt` for what must be on the
floppy and how to verify the image, and `LISA_INSTALL.TXT` for the text that
callers download.

## 1.7 release record

| Item | Value |
| --- | --- |
| Apple-LISACom release commit | b930000 "LISACom 1.7: working volume, real modem hang-up, bookmarks beside the tool" |
| Apple-LISACom layout commit | 04229c1 "LISACom 1.7 release kit: sources/ layout, formatted .TEXT files, install notes" |
| Tag `v1.7` | on 04229c1 (moved there from b930000; the interim tag `1.7` was deleted) |
| AtkinsonPoint commit | bc6ee1d "Combined floppy: LISACom 1.7 + Atkinsonpoint 1.1" |
| `LISACOM_1_7.dc42` MD5 | 918b46ae67befd0cea9f0a93c8fb6d5d |
| `LISACOM_1_7_ATKINSONPOINT_1_1.dc42` MD5 | 5e690df510db43a54ca55a09ec603a27 |
| BBS | both images in IMG_RELEASES, BBSLIST.TEXT in SW_TOOLS |
