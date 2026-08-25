# LISACom 1.1

A serial communications tool for the Apple Lisa Office System. LISACom is a
native LOS desktop tool: it opens as a window on the Office System desktop,
drives Serial B, dials BBSes through a WiFi modem, and moves files in both
directions -- XMODEM, YMODEM with CRC-16, YMODEM batch receive, and YMODEM
send with exact file sizes. It renders live BBS sessions, including CP437
box art approximated in ASCII, on a 1983 machine's own screen. Written in
Lisa Pascal with the Workshop 3.0 toolchain; runs under Lisa Office System
3.1 on real hardware (developed and verified on a Lisa 2/10 and a LisaFPGA).

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
(font 8, fixed width). The welcome banner reports the version and current
line settings. Any key stops a transfer in progress.

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
terminal connected.

Bookmarks live in a file named BBSLIST.TEXT on the boot volume, one entry
per line:

    BAUD 9600
    NAME 8-Bit Boyz|ATDT bbs.8bitboyz.com:23|fun board
    NAME Vertrauen|ATDT vert.synchro.net:23

BAUD sets the default speed, INIT (optional) is sent before each dial,
and each NAME line is name | dial command | optional note. The Bookmarks
menu can add, remove, and list entries from the desktop.

### BBS session tips

Modern boards detect LISACom as an 80x24 US-ASCII dumb terminal and serve
their plain-text menus -- sparse but complete. On Synchronet boards, a
one-time visit to Default user config improves life noticeably: Screen
Pause OFF (LISACom keeps its own 64-line scrollback), Spinning Cursor OFF
(it litters a dumb terminal with stray characters), and Default Download
Protocol set to Ymodem so batch downloads skip the prompt.

### Receiving files

**Receive a File ... (XMODEM)** -- classic XMODEM checksum receive.
Prompts for the Lisa filename to create.

**Receive via YMODEM ...** -- YMODEM with CRC-16, 128-byte and 1K blocks.
The sender supplies the filename and exact size; press RETURN at the
Save-as prompt to accept the sender's name, or type a name to override it
(the typed name applies to the first file only). Start the send on the
other end -- plain YMODEM, not YMODEM-G -- and LISACom syncs.

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
filename, or RETURN browses the disk catalog with a paged picker sized
to the window (a number sends that file, Q stops).

**Send via YMODEM ...** -- same picker, but the file goes with its name
and its exact byte count in the YMODEM header, so the receiver truncates
away the transfer padding and lands the file at its true size. / in
Lisa filenames is sent as _ for the PC's benefit. On the PC:
File -> Transfer -> YMODEM -> Receive in Tera Term (set the transfer
folder first under Additional settings so you know where files land).

### List and Delete

List Files shows the boot volume catalog with free space; Delete a File
removes one after confirmation. Clear Screen empties the pane.

## Building from source

Three source files build the tool:

    LMX/MAIN.TEXT       the program
    LMX/GLOBALS.TEXT    shared state, menu constants, the text pane unit
    LMX/ALERTS.TEXT     alert text and menu definitions (Alert tool input)

Menus are matched by position, so GLOBALS and ALERTS must always change
together; a build that mixes versions will either fail to compile or
dispatch menu items wrongly. When in doubt, send all three.

Two file-format rules matter when sources travel by YMODEM:

1. Workshop .TEXT files are **paged**: a 1024-byte header page, then
   1024-byte pages in which no line crosses a page boundary. A raw text
   file will not compile. Run fmt_text.py (on the PC) over the source
   and send its output.
2. Line endings are **bare CR** (0x0D). LF anywhere renders as illegal
   characters in the Editor and breaks the compile.

The build itself, on the Lisa:

1. Receive the formatted source(s) with LISACom, then File-Mgr Copy each
   to its LMX/ slot
2. From the Workshop main menu: R then <LMX/MAKE (the leading < is
   required). The exec compiles all three, links, stages the files, runs
   the Alert tool, and re-registers the tool with InstallTool
3. Boot the Office System

MAKE only rewrites {T419306}Obj and {T419306}PHRASE; the icon files
survive every rebuild.

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
byte-exact BBS -> Lisa -> PC file round trip.

Bugs and ideas: post to LisaList2.
