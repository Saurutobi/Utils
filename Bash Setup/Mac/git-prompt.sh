#Set colour variables
Grey="\[\e[1;30m\]"
Purple="\[\e[0;35m\]"
Cyan="\[\e[0;36m\]"
LightGreen="\[\e[1;32m\]"
LightRed="\[\e[1;31m\]"
Default="\[\e[0m\]"

branch_name()
{
	branch=$(git symbolic-ref  --short HEAD 2> /dev/null);
	echo "($branch)";
}

#hostname(\h)(can user(\u))
#working directory(\w)
#time(\t)
PS1="$LightRed+-[$Purple\h $LightGreen\$(branch_name) $Cyan\w$LightRed] @ \t\n$LightRed+->$Default ";