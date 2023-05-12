# ISLPA-and-WSLPA
## introduce：
This project contains two algorithms, namely ISLPA and WSLPA, which are both improved based on the label propagation algorithm SLPA,They are used to discover overlapping communities in complex networks.
ISLPA considers the importance and similarity of nodes, uses ascending degree sequence as tag update sequence, and uses Jaccard similarity as the basis for secondary selection, thus eliminating nested communities.
WSLPA is an extension of SLPA algorithm in weighted network. PageRank ascending order is used as the node update sequence, and labels are selected by adding weights according to labels, thus eliminating the communities contained in nesting.

## using
I encapsulate methods and properties in a class, and using methods is also very simple, just enter`<s = ISLPA(G,Iterations,threshold)>` ,then `<res = s.excute()>`,WSLPA is similar.




