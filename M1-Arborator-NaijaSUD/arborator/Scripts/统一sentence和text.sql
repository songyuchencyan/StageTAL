update sentencefeatures
set value=
	(select sentences.sentence from sentences where sentences.rowid=sentencefeatures.sentenceid)
where attr="text"
and sentencefeatures.sentenceid in (select rowid from sentences);


