# wechat-tools

These are a few tools for using WeChat from the command line. Based on the Unix philosophy, each tool is simple and only does one thing:

* **Wefiledaemon** can run in the background and automatically download files sent to you via WeChat to a specified directory
* **Wsend** sends a file to a user
* **Wmsg** sends a message to a user

You'll need the [itchat library](http://itchat.readthedocs.io/) to make things work.

If you want an interactive WeChat client on the command line, check [WeChat Terminal](https://www.npmjs.com/package/node-wechat-terminal). 

I don't plan building any interactivity into the above tools beyond what is strictly necessary, but might take a stab at building an ncurses client at some point
