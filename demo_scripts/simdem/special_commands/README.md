# Special Commands

Some commands will be intercepted by SimDem and handled as special
commands. For example, we might interccept a command to open a browser
at a specific page and handle it differently in a headless CLI
environment to how it is handled in a Web UI environment.

In fact lets look at that use case as an example.

## Opening a Browser Tab

On linux the command `xdg-open` is the accepted way of opening a
browser, therefore it is the accepted way of having such a command in
SimDem script. However, this poses a problem, behoviour of this
command will be different in different UI environments.

For example, on a headliess CLI environment it will attempt to open
"lynx" or similar text based browsers. Since these are interactive
programs they will not work in SimDem. If running in a desktop
environment it will attempt to open the preferred browser.

SimDem will intercept this command and handle it appropriately. That
is, in a headless CLI environment it will convert the command to a
"curl -I" command, this at least allows us to ensure that there is a
resposne from the URL provided. When running in a Web UI it will open
a new browser tab (at least at the time of writing, we may decide to
integrate this with the Web UI at some point).

### In Action

The command block below contains the `xdg-open` command, depending on
whether you are running in the Web UI or the CLI you will see
different behaviour, as described above.

```
xdg-open http://bing.com
```
