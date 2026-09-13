# LISACom changelog

## 1.7 -- 13 September 2026
Verified on a Lisa 2/10 (Office System 3.1, WiRSa WiFi modem, The Apple Lisa
BBS) and a LisaFPGA.  Everything since 1.1 is in this release.

**Working volume (1.6)** -- XModem > Use Volume ... lists the mounted volumes
it can find, with free blocks, and you pick one.  Receives, List Files, the
Send browse list and Delete a File then use that volume.  It starts as the
volume LISACom runs from.  The welcome banner names it.  A volume that
answers to two names (a 2/10's internal disk is both -#12- and -UPPER-) is
tagged "probably the same disk".

**Hang Up really hangs up (1.7)** -- Hang Up, and Dial's hang-up-before-
redial, send the Hayes escape (+++ with guard times, then ATH) and show the
modem's reply before closing the port.  Before this, only the Lisa's port
closed and a WiFi modem stayed connected to the board.

**Files go where you can find them (1.2, 1.3, 1.4, 1.5)** -- a received file
is saved on the working volume, not the boot prefix, and the pane says where
("receiving into -#2#1-11.PIX").  A Save-as name typed as #2#1-NAME (missing
its leading hyphen) is accepted.  List Files, browse and Delete act on the
working volume with the full path -- Delete previously acted on the boot
disk whatever it listed.  A name typed at File to send is looked up on the
working volume; a bare -vol- there browses that volume for one send.

**Bookmarks (1.2, 1.5)** -- BBSLIST.TEXT is read and written beside the tool
(its own volume); with no file at all, a built-in LISA BBS entry is offered.
Dialing a bookmark while a line is open hangs up first.

**YMODEM header (1.4)** -- the file name sent to the PC is the bare name,
never the -vol- path.

**After a receive (1.2)** -- the pane says how to get back: "The line is
still open: XModem menu > Terminal resumes the BBS session."

**Build notes** -- the tool's global data sits a few hundred bytes under the
linker's 32K limit; the browse list is 100 entries (was 130) to pay for the
volume list.  See README, Building from source.

## 1.1 -- 25 August 2026
YMODEM batch receive, YMODEM send with exact sizes, CP437 art, model-first
terminal.  Combined floppy with Atkinsonpoint 1.1.

## 1.0 -- August 2026
First desktop-tool release: terminal, dial, XMODEM, bookmarks.
