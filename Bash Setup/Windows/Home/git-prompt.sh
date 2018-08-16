#Set colour variables
Grey="\[\e[1;30m\]"
Purple="\[\e[0;35m\]"
Cyan="\[\e[0;36m\]"
LightGreen="\[\e[1;32m\]"
LightRed="\[\e[1;31m\]"
Default="\[\e[0m\]"

if test -z "$WINELOADERNOEXEC"
then
	GIT_EXEC_PATH="$(git --exec-path 2>/dev/null)"
	COMPLETION_PATH="${GIT_EXEC_PATH%/libexec/git-core}"
	COMPLETION_PATH="${COMPLETION_PATH%/lib/git-core}"
	COMPLETION_PATH="$COMPLETION_PATH/share/git/completion"
	if test -f "$COMPLETION_PATH/git-prompt.sh"
	then
		. "$COMPLETION_PATH/git-completion.bash"
		. "$COMPLETION_PATH/git-prompt.sh"
		branch_name=' `__git_ps1`'	#branch name
	fi
fi

#hostname(\h)(can user(\u))
#working directory(\w)
#time(\t)
PS1="$LightRed+-[$Purple\h$LightGreen$branch_name $Cyan\w$LightRed] @ \t\n$LightRed+->$Default ";

MSYS2_PS1="$PS1"               # for detection by MSYS2 SDK's bash.basrc