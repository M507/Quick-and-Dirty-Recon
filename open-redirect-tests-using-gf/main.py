"""
echo is a command that outputs the strings it is being passed as arguments. 
What to Waybackurls? Accept line-delimited domains on stdin,
fetch known URLs from the Wayback Machine for .domain.com and output them on stdout.
Httpx? is a fast and multi-purpose HTTP. 
GF? A wrapper around grep to avoid typing common patterns and anew Append lines from stdin to a file,
but only if they don't already appear in the file. Outputs new lines to stdout too, removes duplicates.
"""

# echo "domain" | waybackurls | httpx -silent -timeout 2 -threads 100 | gf redirect | anew
