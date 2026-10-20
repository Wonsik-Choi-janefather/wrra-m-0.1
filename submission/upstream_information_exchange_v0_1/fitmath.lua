function Math(el)
 if el.mathtype == "DisplayMath" and FORMAT:match("latex") then
  return pandoc.RawInline("latex", "\\begin{center}\\fitmath{" .. el.text .. "}\\end{center}")
 end
end

function Code(el)
 if FORMAT:match("latex") and #el.text > 30 and not el.text:match("[{}]") then
  return pandoc.RawInline("latex", "\\path{" .. el.text .. "}")
 end
end
