function Math(el)
 if el.mathtype == "DisplayMath" and FORMAT:match("latex") then
  return pandoc.RawInline("latex", "\\begin{center}\\fitmath{" .. el.text .. "}\\end{center}")
 end
end
