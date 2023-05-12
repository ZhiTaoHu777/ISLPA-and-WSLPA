# ISLPA-and-WSLPA
## introduce：
This project contains two algorithms, namely ISLPA and WSLPA, which are both improved based on the label propagation algorithm SLPA,They are used to discover overlapping communities in complex networks.
ISLPA considers the importance and similarity of nodes, uses ascending degree sequence as tag update sequence, and uses Jaccard similarity as the basis for secondary selection, thus eliminating nested communities.
WSLPA is an extension of SLPA algorithm in weighted network. PageRank ascending order is used as the node update sequence, and labels are selected by adding weights according to labels, thus eliminating the communities contained in nesting.



## using
I encapsulate methods and properties in a class, and using methods is also very simple, just enter`<s = ISLPA(G,Iterations,threshold)>` ,then `<res = s.excute()>`,WSLPA is similar.
I wrote some tool classes, including data import, evaluation and drawing, for your convenience. They are in the util folder.
The evaluation methods include overlapping standardized mutual information NMI of MacDaid, and extended modularity EQ of shen. If you need to use it, you must quote the corresponding references.
It is worth mentioning that the division of overlapping communities drawn by the drawing program is very effective, and the intuitive network division diagram I spent a lot of time figuring out can be used in your paper.

## reference
if you use SLPA_v0, please cite:
>Xie J, Szymanski B K. Towards linear time overlapping community detection in social networks[C]//Pacific-Asia Conference on Knowledge Discovery and Data Mining. Springer, Berlin, Heidelberg, 2012: 25-36.
if you use ISLPA, please cite:""
if you use WSLPA, Please cite:""

if you use extended Modularity,please cite：
> Shen H, Cheng X, Cai K, et al. Detect overlapping and hierarchical community structure in networks[J]. Physica A: Statistical Mechanics and its Applications, 2009, 388(8): 1706-1712.
if you use overlapping nmi,Please refer to https://github.com/aaronmcdaid/Overlapping-NMI the reference mentioned, and thank the author *Remy Cazabet for contributing the code.









