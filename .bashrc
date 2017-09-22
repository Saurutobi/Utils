#source /etc/git-completion.bash
export GIT_SSH=/bin/ssh.exe
#set up winmerge as diff tool
export GIT_EXTERNAL_DIFF=windiff.sh
		#file at c/progfilesx86/git/bin/

export PATH=$PATH:/c/Program\ Files\ \(x86\)/Git/bin:/c/Program\ Files\ \(x86\)/KDiff3:


#startup stuff
echo "Going to lbkstudios-main Repo";
echo "";
cd /c/Git/lbkstudios-main;
echo "Fetching";
echo "";
git fetch;
echo "Backing out";
cd ..;
echo "Going to Hermes Repo";
echo "";
cd /c/Git/Hermes;
echo "Fetching";
echo "";
git fetch;
echo "Backing out";
cd ..;

# set shortcuts
alias ls='ls -p'
alias add='git add'
alias amend='git commit --all --amend; status'
alias show='git remote show origin'
alias fetch='git fetch'
alias show_branches='git branch'
alias status='git status;echo " ";show_unpushed;'
alias clean='git clean'
alias stash='git stash'
alias pstash='git stash pop'
alias ci='git commit --all -m '
alias merge='git merge '
alias mergetool='git mergetool'
alias help='git help'
alias squash='git rebase -i HEAD~3'
alias deploy_otw='deploy_messaging; deploy_validation; deploy_transformation; deploy_bulkload; deploy_scheduling'
alias diff_work='git status;echo " ";show_unpushed;git difftool --dir-diff HEAD &'
alias resource='source ~/.bashrc'

#Shows unsubmitted commits
function show_unpushed
{
	echo "Showing unpushed Commits";
	git log origin/$(get_branch)..HEAD --pretty=format:"%Cred%h%Creset-%C(bold blue)<%an> %Cgreen(%ar)%Creset : %s";
}

function co
{
	git checkout "$@";
}

# pull branch from origin
function pull
{
	branch=$(get_branch "$@");
	git pull origin $branch
}

# push branch 
function push 
{
	branch=$(get_branch "$@");
	git push origin $branch
}

# push branch 
function force_push 
{
	branch=$(get_branch "$@");
	git push -f origin $branch
}

#hard reset current branch to latest local commit(wipes out working dir changes)
function reset_hard
{
	git reset --hard;
}

#hard reset current branch to latest origin commit(wipes out local commits and working dir changes)
function update_branch
{
	git fetch;
	branch=$(get_branch);
	git reset --hard origin/$branch;
}

#Check local&remote for commit hash/branch and displays each branch found that contain those items
function contains
{
	echo "Local:";
	git branch --contains "$@";
	echo "Remote:"
	git branch -r --contains "$@";
}

# diff 2 branches
# default 2nd branch is the current branch
# diff_branch <branch_name> <branch_name>
function diff_branch()
{
	branch=$(get_branch_name "$2");  
	echo "Compare $1 to $branch"
	git difftool --dir-diff $1..$branch &
}

# create a new branch from current branch
# call with branch_current <branch name>
function branch_current()
{ 
	update_branch;
	branch=$@;
	curr=$(get_branch);
	echo "creating $branch";
	echo "fetch $curr";
	git fetch origin $curr;
	echo "branch from $curr";
	git checkout -b $branch $curr; 
	echo "push branch remotely";
	git push origin $branch;
	git branch -vv;
}

# delete branch locally and remotely
# call with nuke_branch <branch name>
function nuke_branch()
{ 
	branch=$@;
	echo "deleting local branch";
	git branch -D $branch; 
	echo "deleting remote branch";
	git push origin --delete $branch;
	echo "show current branches";
	git branch;
}

#delete branch locally
#call with delete_branch <branch name>
function delete_branch()
{
	branch=$@;
	echo "deleting local branch";
	git branch -D $branch; 
	echo "show current branches";
	git branch;
}

function show_custom()
{
	echo "Aliases ... "
	alias
	echo "Functions ... "
	set | grep -A 1000 "branch" |grep \(\)
}

function get_branch 
{
	git rev-parse --abbrev-ref HEAD 2> /dev/null
}

# Generate a wrapper completion function (completer) for an alias
# based on the command and the given arguments, if there is a
# completer for the command, and set the wrapper as the completer for
# the alias.
function wrap_alias()
{
	[[ "$#" == 3 ]] || return 1

	local alias_name="$1"
	local aliased_command="$2"
	local alias_arguments="$3"
	local num_alias_arguments=$(echo "$alias_arguments" | wc -w)

	# The completion currently being used for the aliased command.
	local completion=$(complete -p $aliased_command 2> /dev/null)

	# Only a completer based on a function can be wrapped so look for -F
	# in the current completion. This check will also catch commands
	# with no completer for which $completion will be empty.
	echo $completion | grep -q -- -F || return 0

	local namespace=alias_completion::

	# Extract the name of the completion function from a string that
	# looks like: something -F function_name something
	# First strip the beginning of the string up to the function name by
	# removing "* -F " from the front.
	local completion_function=${completion##* -F }
	# Then strip " *" from the end, leaving only the function name.
	completion_function=${completion_function%% *}

	# Try to prevent an infinite loop by not wrapping a function
	# generated by this function. This can happen when the user runs
	# this twice for an alias like ls='ls --color=auto' or alias l='ls'
	# and alias ls='l foo'
	[[ "${completion_function#$namespace}" != $completion_function ]] && return 0

	local wrapper_name="${namespace}${alias_name}"

	eval "
		function ${wrapper_name}()
		{
			(( COMP_CWORD += $num_alias_arguments ))
			args=( \"${alias_arguments}\" )
			COMP_WORDS=( $aliased_command \${args[@]} \${COMP_WORDS[@]:1} )
			$completion_function
		}
	"

	# To create the new completion we use the old one with two
	# replacements:
	# 1) Replace the function with the wrapper.
	local new_completion=${completion/-F * /-F $wrapper_name }
	# 2) Replace the command being completed with the alias.
	new_completion="${new_completion% *} $alias_name"

	eval "$new_completion"
}

# For each defined alias, extract the necessary elements and use them
# to call wrap_alias.
eval "$(alias -p | grep -v '[";|&]' | sed -e 's/alias \([^=][^=]*\)='\''\([^ ][^ ]*\) *\(.*\)'\''/wrap_alias \1 \2 '\''\3'\'' /')"

unset wrap_alias