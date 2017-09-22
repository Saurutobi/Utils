#!/usr/bin/perl
use String::CamelCase qw(camelize decamelize wordsplit);

my $branchName = decamelize($ARGV[0]);

print lc($branchName);