MAC is a pretty big pain, here's a few setup items:
install kdiff3

Run `ln -s /Applications/kdiff3.app/Contents/MacOS/kdiff3 /usr/local/bin/kdiff3`
Then `git config --global merge.tool kdiff3`