#! /bin/zsh

files=$(egrep '^[^/]+$' /usr/local/texlive/2021/texmf-dist/ls-R | sort | uniq)
rm -f t-d.txt
touch t-d.txt
foreach filename (${(f)files})
    kpsewhich $filename && echo $filename >> t-d.txt
end
sort t-d.txt | uniq > texmf-dist.txt
rm -f t-d.txt
