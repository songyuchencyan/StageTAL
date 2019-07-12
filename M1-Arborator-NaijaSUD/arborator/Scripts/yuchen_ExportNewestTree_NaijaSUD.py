from database import SQL
import conll


def reorder(trees, outfile):	# 重新排序conll树，可重命名所有sent_id
	"""
	Reorders the trees based on the nr sentencefeature, adds updated text and sentence_id.
	Once this is done, the trees are written to a new file.

	input: List(Tree), Str
	does: Writes <outfile>
	output: None
	"""
	prefix = "_".join(trees[0].sentencefeatures.get("sent_id").split("_")[:-1])
	sortable = sorted(list([(int(t.sentencefeatures.get("nr")), t) for t in trees]))
	new_trees = list()
	for nr, tree in sortable:

		# adding metadatas	应该是重命名sent_id,从0开始
		tree.sentencefeatures["text"] = tree.sentence()
		tree.sentencefeatures["sent_id"] = prefix+"_"+str(nr-1)

		# removing useless metadata
		del tree.sentencefeatures["nr"]
		new_trees.append(tree)
	conll.trees2conllFile(new_trees, outfile)



if __name__ == "__main__":

	## Open project database

	sql = SQL("NaijaSUD")	# 输入project名字
	db,cursor=sql.open()

	## Use 2 functions :
	# - exportLastBestAnnotations in lib/database.py -> writes a file with trees and their rank
	# - reorder in lib/yuchen.py -> reorder trees based on their rank, write a file with the output

	users, c = sql.exportLastBestAnnotations(115,"P_ABJ_GWA_06_Ugo-lifestory_PRO")	# 输入textid和text name，可通过链接https://arborator.ilpga.fr/editor.cgi?project=NaijaSUD&textid=74&opensentence=1看到textid
	print(users, c)
	fpath = "E:/TAL/Stage/arborator/projects/NaijaSUD/export/P_ABJ_GWA_06_Ugo.lifestory_PRO.most.recent.trees.with.feats.conllu"	# 输入导出的文件所在路径
	trees = conll.conllFile2trees(fpath)	# 重新排序conll树，重命名sent_id
	reorder(trees, fpath+"_reordered")   