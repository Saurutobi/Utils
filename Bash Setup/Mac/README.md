MAC is a pretty big pain, here's a few setup items:
install kdiff3

Run `ln -s /Applications/kdiff3.app/Contents/MacOS/kdiff3 /usr/local/bin/kdiff3`
Then `git config --global merge.tool kdiff3`


maybe this stuff needs to be done
git config --add merge.tool kdiff3
git config --add mergetool.kdiff3.path /Applications/kdiff3.app/Contents/MacOS/kdiff3 
git config --add mergetool.kdiff3.trustExitCode false
git config --add diff.guitool kdiff3
git config --add difftool.kdiff3.path /Applications/kdiff3.app/Contents/MacOS/kdiff3 
git config --add difftool.kdiff3.trustExitCode false