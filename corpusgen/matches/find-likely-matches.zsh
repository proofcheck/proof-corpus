#!/usr/bin/env zsh

foreach outer (/Users/stone/texes/*)
    foreach inner ($outer/*)
        grep -l -R '\\begin{proof' $inner > /dev/null 2>/dev/null && grep -l -R '^\\begin{document}' $inner | grep -v .sty | grep -v .cls
    end
end
