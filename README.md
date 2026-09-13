# LISACom 1.7

A serial communications tool for the Apple Lisa Office System. LISACom is a
native LOS desktop tool: it opens as a window on the Office System desktop,
drives Serial B, dials BBSes through a WiFi modem, and moves files in both
directions -- XMODEM, YMODEM with CRC-16, YMODEM batch receive, and YMODEM
send with exact file sizes. It knows which disk it is working on, hangs up
like a modem expects, and renders live BBS sessions, including CP437
box art approximated in ASCII, on a 1983 machine's own screen. Written in
Lisa Pascal with the Workshop 3.0 toolchain; runs under Lisa Office System
3.1 on real hardware (developed and verified on a Lisa 2/10 and a LisaFPGA).
See CHANGELOG.md for what changed since 1.1.

## Thanks

This tool exists because other people did the hard parts first and shared
them.

**Alex Anderson-McLeod** (alexthecat123) -- his LOS Minesweeper is the
teaching example this tool's desktop integration was learned from, his LOS
Compilation Base image supplied the Workshop environment the tool is built
in, and Apple's own ICONEDIT icon editor was recovered from that same
image. His LisaFPGA and ESProFile made nightly testing practical.

**Tom Stepleton** -- his lisabbs (public domain) provided LIBPORT and
LIBXFER, the working reference for Lisa serial programming and the YMODEM
packet logic, and his documentation pointers unlocked the Workshop .TEXT
page format and the DC42 checksum quirks. He also corrected an early wrong
conclusion about Workshop keyboard handling, publicly and helpfully.

**James MacPhail (sigma7)** -- corrections and hardware wisdom.

**The LisaList2 community**, **bitsavers.org** for the Apple manuals, the
**Computer History Museum** for releasing the Lisa Office System source,
and **Vertrauen BBS** (vert.synchro.net), which unknowingly served as the
test range.

Errors are mine, not theirs.

## Requirements

- Apple Lisa running Lisa Office System 3.x (developed on 3.1)
- Serial B configured once in Preferences -> Connect Devices
  (Serial B Connector = Serial Cable); LISACom mounts the port itself
  each session
- A serial device on Serial B. Developed against a WiRSa WiFi modem
  (DCE, straight-through cable, bare CR command endings, hardware flow
  control disabled with AT&K0 then AT&W)
- For transfers with a PC: any terminal program with XMODEM/YMODEM,
  such as Tera Term

## The five files of an installed tool

LISACom installs as tool number 419306. A complete installation is five
files on the boot volume:

    {T419306}Obj           the program
    {T419306}PHRASE        alerts and menus, built by the Alert tool
    {T419306}ICON          the icon file (see Icons below)
    {T419306}ICON.BACKUP   spare copy of the icon
    {t419306}icon2         second icon file (lowercase t and icon2)

A sixth file, `{T419306}data segment`, is created by the OS at run time.

Never drag a tool's icon to the Wastebasket: LOS deletes the tool's whole
absorbed file set with it, including the invisible phrase file.

## Using LISACom

Open the LISACom icon on the desktop. The window shows an 80x24 text pane
(font 8, fixed width). The welcome banner reports the version, the line
settings and the *working volume* (see below). Any key stops a transfer in
progress.

### The working volume

LISACom keeps one *working volume*: the disk that receives land on and that
List Files, the Send browse list and Delete a File look at. It starts as the
volume LISACom is running from, so a copy on the boot disk works on the boot
disk and a copy on an external disk works there.

XModem -> Use Volume ... lists the mounted volumes it can find and their
free blocks:

    Mounted volumes:
    1  -#12-  1984 free blocks  (this tool's volume)
    2  -#2#1-  13062 free blocks
    3  -LOWER-  728 free blocks
    4  -UPPER-  1984 free blocks  (same free count as 1 - probably the same disk)
    Use which number (RETURN cancels):

Pick a number and everything follows it until you pick again. Entry 1 is
always the tool's own volume. -LOWER- is a floppy in the drive. On a Lisa
2/10 the internal disk answers to both -#12- and -UPPER-, hence the note.
Desktop names ("ProFile", "Disk") are not shown; the free-block count is
the clue. Bookmarks do not follow the working volume: they stay with the
tool.

### The Baud menu

Sets the line speed: 1200 through 38400. The speed takes effect when the
port next opens, and the pane reminds you to match it on the other end.
38400 works reliably on Serial B for PC transfers; BBS sessions through
the WiRSa run at whatever speed the line was opened at, so set Baud
*before* dialing.

### Terminal

XModem -> Terminal opens a live terminal on Serial B.

- Apple-. or Apple-Q exits (the line stays open; Hang Up closes it)
- Apple-E toggles local echo
- Apple-L toggles whether RETURN sends CR+LF or CR only
- Backspace/DEL sending is configurable the same way

The terminal behaves like a real 80-column display: lines longer than 80
columns truncate rather than wrap. ANSI escape sequences are filtered,
including the OSC/DCS strings modern boards send. Characters above ASCII
(CP437 -- the box-drawing and shading art BBSes use) are approximated:
lines become - | + =, shading becomes . % #, accented letters fold to
their base letter. During heavy output the pane repaints in whole-screen
steps rather than scrolling line by line; this is what lets a 5 MHz
machine keep up with the wire without dropping data.

### Dial and Bookmarks

XModem -> Dial lists your bookmarks by number; pick one and LISACom opens
the line, sends the INIT string (if any), waits for the modem to answer
(OK or ERROR both count), sends the dial command, and drops you in the
terminal connected. If a line is already open, LISACom hangs up first
(see Hang Up) so the dial string cannot land in the old session.

Bookmarks live in a file named BBSLIST.TEXT on the same volume as the
LISACom tool, one entry per line:

    BAUD 9600
    NAME 8-Bit Boyz|ATDT bbs.8bitboyz.com:23|fun board
    NAME Vertrauen|ATDT vert.synchro.net:23

BAUD sets the default speed, INIT (optional) is sent before each dial,
and each NAME line is name | dial command | optional note. The Bookmarks
menu can add, remove, and list entries from the desktop; the file is read
once when LISACom opens. With no BBSLIST.TEXT at all, one built-in entry is
offered: LISA BBS (The Apple Lisa BBS, theapplelisabbs.duckdns.org:1983).
A starter BBSLIST.TEXT with eleven boards ships with this release; put it
beside the tool.

Note that duplicating LISACom onto another disk copies the tool's own
files only -- BBSLIST.TEXT is an ordinary file and stays where it was.

### Hang Up

XModem -> Hang Up disconnects the way a modem expects: a second of
silence, +++, a second of silence, ATH, then the modem's reply (OK, then
NO CARRIER with the call time) and the port closes. About three seconds.
A WiFi modem such as the WiRSa keeps its connection to the board until it
sees this; closing the Lisa's port alone does not hang up.

### BBS session tips

Modern boards detect LISACom as an 80x24 US-ASCII dumb terminal and serve
their plain-text menus -- sparse but complete. On Synchronet boards, a
one-time visit to Default user config improves life noticeably: Screen
Pause OFF (LISACom keeps its own 64-line scrollback), Spinning Cursor OFF
(it litters a dumb terminal with stray characters), and Default Download
Protocol set to Ymodem so batch downloads skip the prompt.

### Receiving files

**Receive a File ... (XMODEM)** -- classic XMODEM checksum receive.
Prompts for the Lisa filename to create; a bare name lands on the working
volume.

**Receive via YMODEM ...** -- YMODEM with CRC-16, 128-byte and 1K blocks.
The sender supplies the filename and exact size; press RETURN at the
Save-as prompt to accept the sender's name, or type a name to override it
(the typed name applies to the first file only). A bare name lands on
the working volume; a full -vol-name path is used as typed; a path typed
without its leading hyphen (#2#1-NAME.PIX) is corrected. The pane shows
where the file went: "receiving into -#2#1-11.PIX". Start the send on the
other end -- plain YMODEM, not YMODEM-G -- and LISACom syncs. When the
receive ends during a BBS session the pane reminds you that the line is
still open and XModem -> Terminal resumes it.

YMODEM receive is a **batch** receive: if the sender queues several
files, every file is received, each closed at its own end-of-file, and
the session finishes with a count. This is how BBS batch downloads work:
tag the files, pick YMODEM at the protocol menu, one download.

Received filenames are made Lisa-safe automatically: path prefixes are
stripped, a Lisa catalog name may contain only one period (anything after
a second one folds to _), and characters LOS does not allow -- including
-, which is the LOS pathname delimiter -- become _.

Received files land at their exact size. For build sources, the two-step
habit is recommended: receive to a scratch name, then File-Mgr Copy to
the destination, so a dead transfer cannot damage the only copy.

### Sending files

**Send a File ... (XMODEM)** -- XMODEM checksum send. Prompts for a
filename, or RETURN browses the working volume with a paged picker sized
to the window (a number sends that file, Q stops). A bare name is looked
up on the working volume; a full -vol-name path sends from anywhere; a
bare -vol- (for example -#2#1-) browses that volume for this one send.

**Send via YMODEM ...** -- same picker, but the file goes with its name
and its exact byte count in the YMODEM header, so the receiver truncates
away the transfer padding and lands the file at its true size. The name
in the header is the bare file name, never the -vol- path, and / in Lisa
filenames is sent as _ for the PC's benefit. On the PC:
File -> Transfer -> YMODEM -> Receive in Tera Term (set the transfer
folder first under Additional settings so you know where files land).

### List and Delete

List Files shows the working volume's catalog under a "Volume -#2#1-:
N free blocks" line; Delete a File removes one after confirmation (files
with braces in their names -- tool and desktop files -- are refused).
Both list up to 100 entries. Clear Screen empties the pane.

## Building from source

Four files build the tool:

    LMX/MAIN.TEXT       the program
    LMX/GLOBALS.TEXT    shared state, menu constants, the text pane unit
    LMX/ALERTS.TEXT     alert text and menu definitions (Alert tool input)
    LMX/MAKE.TEXT       the Workshop exec that compiles, links and installs

Menus are matched by position, so GLOBALS and ALERTS must always change
together; a build that mixes versions will either fail to compile or
dispatch menu items wrongly -- the classic symptom is Clear Screen
listing files to delete. Send all three, every build; a source that
happens to be lying on the Lisa is not guaranteed to be current.

Two file-format rules matter when sources travel by YMODEM:

1. Workshop .TEXT files are **paged**: a 1024-byte header page, then
   1024-byte pages in which no line crosses a page boundary. A raw text
   file will not compile. Run fmt_text.py (on the PC) over the source
   and send its output.
2. Line endings are **bare CR** (0x0D). LF anywhere renders as illegal
   characters in the Editor and breaks the compile.

The build itself, on the Lisa:

1. Save & Put Away any running LISACom. (A Set-Aside tool is restored
   after the rebuild as the *old* program, still showing the old version.)
2. Receive the formatted sources with LISACom straight onto their LMX/
   names (type LMX/MAIN.TEXT at the Save-as prompt), or receive to scratch
   names and File-Mgr Copy them over. Check sizes and timestamps with
   L LMX/= before compiling.
3. Empty the Wastebasket. Never drag the old LISACom there: MAKE replaces
   the program in place, and the icon files exist only as part of the
   installed tool.
4. From the Workshop main menu: R then <LMX/MAKE (the leading < is
   required). The exec compiles all three, links, stages the files, runs
   the Alert tool, and re-registers the tool with InstallTool.
5. L LMX/= again: LMX.OBJ, the linked program, must carry a new
   timestamp. The exec rolls past compile *and* link errors and installs
   whatever LMX.OBJ is there, so an old timestamp means the old program
   was just reinstalled. The About box is the final check.
6. Boot the Office System and launch the tool fresh.

MAKE only rewrites {T419306}Obj and {T419306}PHRASE; the icon files
survive every rebuild.

The program's global data sits a few hundred bytes under the linker's
32K limit ("*** Error - More than 32K of globals ***"). The 16 KB alert
heap, the 64-line scrollback, the 100-entry browse list and the bookmark
arrays are the big items; any new global has to be paid for with a cut,
and the linker's "Common data" figure is the number to watch.

One hard-won limit: the serial driver's typeahead buffer is 1024 bytes
and that is a real ceiling on a Lisa 2/10 -- configuring it larger kills
serial receive outright. LISACom lives within it by draining the port in
large gulps and painting once per gulp.

## Icons

Tool icons are 1024-byte files holding a Mac-style font strike: four
48x32 cells (Document Icon, Tool Icon, and their masks). Do not build
them by hand -- Apple's own **ICONEDIT** (recoverable from the LOS
Compilation Base image; copy to ICONEDIT.OBJ and run with R ICONEDIT
in the Workshop) edits them natively, previews all the Reg/Hilite/Ghost
states, and writes a correct file.

The one rule ICONEDIT will not enforce for you: the **mask must be the
solid filled silhouette** of the icon, painted by hand in the Mask pane.
"Data to Mask" copies the line art instead of filling it, which makes
the icon vanish when clicked. Watch the Hilite preview while painting:
correct is your art in reverse video.

A malformed icon file is not cosmetic. One caused Level 7 bus errors and
corrupted copies whenever the Filer serialized the tool to a floppy.

## Distributing on floppy

`LISACOM_1_7.dc42` in this repository is the 1.7 distribution floppy:
LISACom 1.7 and the starter BBSLIST.TEXT, written on a Lisa 2/10 (MD5
918b46ae67befd0cea9f0a93c8fb6d5d). `LISACOM_1_7_ATKINSONPOINT_1_1.dc42`
is the combined floppy: LISACom 1.7, Atkinsonpoint 1.1 (LISA Slide Show)
its nine-picture starter show and the starter BBSLIST.TEXT (MD5 5e690df510db43a54ca55a09ec603a27); it is also
the image in the AtkinsonPoint repository. (The earlier
`LISAComV1_1_AtkinsonPoint_v1_1_Image.dc42` combined LISACom 1.1 with
Atkinsonpoint 1.1 and remains available.) After duplicating the tool to
your disk, copy BBSLIST.TEXT beside it in the Workshop File Manager, or
simply add bookmarks from the desktop -- the file is created on first Add.

With correct icons, the tool duplicates to a floppy normally (Duplicate
is the copy; dragging is a move), runs from the floppy, and duplicates
onto another volume's drive -- including a volume that previously had
LISACom installed. The "Lisa will have to shut down the tool before it
can be copied" prompt is normal LOS behavior.

One practical note from testing: floppies written by a real Lisa proved
reliable every time. Floppies written through a LisaFPGA's floppy port
intermittently lost blocks during sustained writes (an issue under
investigation with that project); if your writer is an FPGA, verify the
disk image before passing it on.

## Troubleshooting

- **Endless x<x< garbage in the terminal** -- baud mismatch, or a
  wedged serial path after switching the port between devices. Match
  speeds first; if garbage persists at every speed, power-cycle the
  serial hardware chain and reopen the port.
- **MAKE_FILE ecode 1282 on receive** -- the destination name contains a
  hyphen. - is the LOS pathname delimiter and is not legal in catalog
  names (this code is absent from the published OS error tables; its
  documented siblings are 1023 and 1171). LISACom substitutes _
  automatically for sender-supplied names; typed names are your own
  responsibility.
- **Compiler reports Error 15 / Error 41 with garbage as line 1** -- the
  source file is missing its page format or carries LF line endings. See
  Building from source.
- **A tool copied to floppy will not run and the drive stalls** -- check
  the icon file first. See Icons.
- **Clear Screen shows a list of files to delete** (or any menu item does
  the wrong thing) -- ALERTS.TEXT and GLOBALS.TEXT on the Lisa are from
  different versions. Rebuild with all three sources from one release.
- **About still shows the old version after a rebuild** -- either the
  tool was Set Aside rather than Put Away before the build (launch it
  fresh), or the link failed and MAKE reinstalled the old LMX.OBJ (check
  its timestamp; see Building from source).
- **Dialing a bookmark types ATDT into the board you are already on** --
  you are running a version before 1.7, which could not hang up a WiFi
  modem. Log off the board first, or update.
- **A received file is not in List Files** -- it went to the working
  volume; check the "receiving into" line and Use Volume.

## History

LISACom grew out of a July 2026 project to run new software natively
under the Lisa Office System, starting from Alex Anderson-McLeod's LOS
Minesweeper as the worked example. It began life as "LISA XModem Util",
a Workshop program that replaced a floppy-shuttle workflow for moving
source code. By 1.0 it was a desktop tool that dialed real BBSes; 1.1
added YMODEM batch receive, YMODEM send, CP437 art, and a terminal
rearchitected so a 2 KB menu burst can never outrun the machine again.
Everything in this README was verified on a Lisa 2/10 and a LisaFPGA in
August 2026, including live sessions against Vertrauen and a verified
byte-exact BBS -> Lisa -> PC file round trip. 1.2 through 1.7 (September
2026) came out of building the LOS Installer and The Apple Lisa BBS: files
that landed on the wrong disk, a hang-up that only closed the Lisa's port,
and no way to see or choose a disk became the working-volume model, a real
modem hang-up, and bookmarks that live beside the tool. Each of those
releases was tested on the 2/10 against the live board before the next
was started.

Bugs and ideas: post to LisaList2, or call The Apple Lisa BBS
(telnet theapplelisabbs.duckdns.org 1983).
