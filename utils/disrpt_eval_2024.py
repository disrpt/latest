"""
Script to evaluate segmentation f-score and perfect discourse unit segmentation proportion from two files. Two input formats are permitted:

  * One token per line, with ten columns, no sentence breaks (default *.tok format) - segmentation indicated in column 10
  * The same, but with blank lines between sentences (*.conll format)

Token columns follow the CoNLL-U format, with token IDs in the first column and pipe separated key=value pairs in the last column. 
Document boundaries are indicated by a comment: # newdoc_id = ...
The evaluation uses micro-averaged F-Scores per corpus (not document macro average).

Example:

# newdoc_id = GUM_bio_byron
1	Education	_	_	_	_	_	_	_	Seg=B-seg
2	and	_	_	_	_	_	_	_	_
3	early	_	_	_	_	_	_	_	_
4	loves	_	_	_	_	_	_	_	_
5	Byron	_	_	_	_	_	_	_	Seg=B-seg
6	received	_	_	_	_	_	_	_	_

Or:

# newdoc_id = GUM_bio_byron
# sent_id = GUM_bio_byron-1
# text = Education and early loves
1	Education	education	NOUN	NN	Number=Sing	0	root	_	Seg=B-seg
2	and	and	CCONJ	CC	_	4	cc	_	_
3	early	early	ADJ	JJ	Degree=Pos	4	amod	_	_
4	loves	love	NOUN	NNS	Number=Plur	1	conj	_	_

# sent_id = GUM_bio_byron-2
# text = Byron received his early formal education at Aberdeen Grammar School, and in August 1799 entered the school of Dr. William Glennie, in Dulwich. [17]
1	Byron	Byron	PROPN	NNP	Number=Sing	2	nsubj	_	Seg=B-seg
2	received	receive	VERB	VBD	Mood=Ind|Tense=Past|VerbForm=Fin	0	root	_	_

For PDTB-style corpora, we calculate exact span-wise f-scores for BIO encoding, without partial credit. In other words, 
predicting an incorrect span with partial overlap is the same as missing a gold span and predicting an incorrect span
somewhere else in the corpus. Note also that spans must begin with B-Conn - predicted spans beginning with I-Conn are ignored.
The file format for PDTB style corpora is similar, but with different labels:

1	Fidelity	Fidelity	PROPN	NNP	_	6	nsubj	_	_
2	,	,	PUNCT	,	_	6	punct	_	_
3	for	for	ADP	IN	_	4	case	_	Seg=B-Conn
4	example	example	NOUN	NN	_	6	obl	_	Conn=I-conn
5	,	,	PUNCT	,	_	6	punct	_	_
6	prepared	prepare	VERB	VBN	_	0	root	_	_
7	ads	ad	NOUN	NNS	_	6	obj	_	_

Arguments:
 * goldfile: shared task gold test data
 * predfile: same format, with predicted segments positions in column 10 - note **number of tokens must match**  
 * string_input: if specified, files are replaced by strings with file contents instead of file names
 * no_boundaries: specify to eval only intra-sentence EDUs
"""

""" TODO
- OK labels : en argument, pas en dur
- OK option sans ls débuts de phrases : cf script "BIO no B'
- OK imprimer les résultats + propre : sans le "o" bizarre
- OK faire 2 classes edu et connectives (conn: futur exp for eval connective extended vs head of connective)
- solution + propre pour la colonne des labels ?
- faire une classe Eval et transformer les 2 en Eval en sous-classes
"""

__author__ = "Amir Zeldes, Laura Rivière"
__license__ = "Apache 2.0"
__version__ = "2.0.0"

import io, os, sys, argparse
from sklearn.metrics import accuracy_score 

# MWE and ellips : no lab or "_"

class Evaluation:
	"""
	Generic class for evalution between 2 files.
	:load data, basic check, basic metrics, print results.
	"""
	def __init__(self, name):
		self.output = dict()
		self.name = name
		self.report = ""

		self.output['doc_name'] = self.name

	def get_data(self, infile, str_i=False):
		if str_i==False:
			data = io.open(infile, encoding="utf-8").read().strip().replace("\r", "")
		else:
			data = infile.strip()

		return data

	def check_tokens_number(self, g, p):
		"""
		Check same number of tokens in both files
		"""
		if len(g) != len(p):
			self.report += "\nFATAL: different number of tokens detected in gold and pred:\n"
			self.report += ">>>  In " + self.name + ": " + str(len(g)) + " gold tokens but " + str(len(p)) + " predicted tokens\n\n"
			sys.stderr.write(self.report)
			sys.exit(0)

	def check_identical_tokens(self, g, p):
		"""
		Check tokens are identical
		"""
		for i, tok in enumerate(g):
			if tok != p[i]:
				self.report += "\nWARN: token strings do not match in gold and pred:\n"
				self.report += ">>> First instance in " + self.name + " token " + str(i) + "\n"
				self.report += "Gold: " + tok + " but Pred: " + p[i] + "\n\n"
				sys.stderr.write(self.report)
				break

	def compute_PRF_metrics(self, tp, fp, fn):

		try:
			precision = tp / (float(tp) + fp)
		except Exception as e:
			precision = 0

		try:
			recall = tp / (float(tp) + fn)
		except Exception as e:
			recall = 0

		try:
			f_score = 2 * (precision * recall) / (precision + recall)
		except:
			f_score = 0
		
		self.output["gold_count"] = tp + fn
		self.output["pred_count"] = tp + fp
		self.output["prec"] = precision
		self.output["rec"] = recall
		self.output["f_score"] = f_score

	def compute_accuracy(self, g, p):
		"""
		Compute accuracy of predictions list of items, againtst gold list of items.
		"""
		self.output["accuracy"] = accuracy_score(g, p)
		self.output["gold_count"] = len(g)
		self.output["pred_count"] = len(p)

	 ###### acc classification report ????

	def print_results(self):
		for k in self.output.keys():
			print(f">> {k} : {self.output[k]}")


class RelationsEvaluation(Evaluation):
	"""
	Specific evaluaion class for relations classification.
	The evaluation uses the simple accuracy score per corpus. 
	:rels disrpt-style data.
	:default eval last column "label"
	:option eval relation type (pdtb: implicit, explicit...) column "rel_type"
	"""

	HEADER_24 = "doc\tunit1_toks\tunit2_toks\tunit1_txt\tunit2_txt\tu1_raw\tu2_raw\ts1_toks\ts2_toks\tunit1_sent\tunit2_sent\tdir\trel_type\torig_label\tlabel"
	HEADER = "doc\tunit1_toks\tunit2_toks\tunit1_txt\tunit2_txt\ts1_toks\ts2_toks\tunit1_sent\tunit2_sent\tdir\torig_label\tlabel"
	LABEL_ID = -1
	TYPE_ID = -3
	DISRPT_TYPES = ['Implicit', 'Explicit', 'AltLex', 'AltLexC', 'Hypophora']

	def __init__(self, name, gold_path, pred_path, str_i=False, rel_type=False):
		super().__init__(name)
		self.mode = "rel"
		self.g_path = gold_path
		self.p_path = pred_path
		self.opt_str_i = str_i
		self.opt_rel_t = rel_type


	def compute_scores(self):
		"""
		:param gold_file: Gold shared task file
		:param pred_file: File with predictions
		:param string_input: If True, files are replaced by strings with file contents (for import inside other scripts)
		:output: dictionary of scores for printing
		"""

		gold_units, gold_labels = self.parse_rels_data(self.g_path, self.opt_str_i, self.opt_rel_t)
		pred_units, pred_labels = self.parse_rels_data(self.p_path, self.opt_str_i, self.opt_rel_t)

		self.check_tokens_number(gold_labels, pred_labels)
		self.check_identical_tokens(gold_units, pred_units)


		self.compute_accuracy(gold_labels, pred_labels)

		if self.opt_rel_t == True:
			self.get_types_scores(gold_labels, pred_labels)

	def get_types_scores(self, g, p):
		"""
		This fonction is to obtain scores of predictions against gold labels, by types of relations.
		"""
	
		for t in self.DISRPT_TYPES:
			gold_t = []
			pred_t = []
			j = 0
			for i, _ in enumerate(g):
				if g[i] == t:
					j += 1
					gold_t.append(g[i])
					pred_t.append(p[i])

			self.output[f'gold_{t}'] = len(gold_t)
			self.output[f'{t}_accuracy'] = accuracy_score(gold_t, pred_t)



	def parse_rels_data(self, path, str_i, rel_t):
		"""
		Rels format from DISRPT = header, then one relation classification instance per line. 
		:LREC_2024_header = 15 columns.
		"""
		data = self.get_data(path, str_i)
		header = data.split("\n")[0]
		assert header == self.HEADER, "Unrecognized .rels header."
		column_ID = self.TYPE_ID if rel_t == True else self.LABEL_ID


		rels = data.split("\n")[1:]
		labels = [line.split("\t")[column_ID] for line in rels] ######## .lower()
		units = [" ".join(line.split("\t")[:3]) for line in rels]

		return units, labels
		

class ConnectivesEvaluation(Evaluation):
	"""
	Specific evaluation class for PDTB connectives detection.
	:parse conllu-style data
	:eval upon strict connectives spans
	"""
	LAB_CONN_B = "Conn=B-conn"		#"Seg=B-Conn" 	#
	LAB_CONN_I = "Conn=I-conn"		#"Seg=I-Conn" 	#
	LAB_CONN_O = "Conn=O"			#"_"			

	def __init__(self, name, gold_path, pred_path, str_i=False):
		super().__init__(name)
		self.mode = "conn"
		self.seg_type = "connective spans"
		self.g_path = gold_path
		self.p_path = pred_path
		self.opt_str_i = str_i

		self.output['seg_type'] = self.seg_type

	def compute_scores(self):
		"""
		:param gold_file: Gold shared task file
		:param pred_file: File with predictions
		:param string_input: If True, files are replaced by strings with file contents (for import inside other scripts)
		:output: dictionary of scores for printing
		"""
		gold_tokens, gold_labels, gold_spans = self.parse_conn_data(self.g_path, self.opt_str_i)
		pred_tokens, pred_labels, pred_spans = self.parse_conn_data(self.p_path, self.opt_str_i)

		self.output['tok_count'] = len(gold_tokens)

		self.check_tokens_number(gold_tokens, pred_tokens)
		self.check_identical_tokens(gold_tokens, pred_tokens)
		tp, fp, fn = self.compare_spans(gold_spans, pred_spans)
		self.compute_PRF_metrics(tp, fp, fn)

	def compare_spans(self, gold_spans, pred_spans):
		"""
		Compare exact spans.
		"""

		true_positive = 0
		false_positive = 0
		false_negative = 0

		for span in gold_spans: # not verified
			if span in pred_spans:
				true_positive +=1
			else:
				false_negative +=1
		for span in pred_spans:
			if span not in gold_spans:
				false_positive += 1

		return true_positive, false_positive, false_negative

	def parse_conn_data(self, path, str_i): 
		"""
		LABEL = in last column
		"""
		data = self.get_data(path, str_i)
		tokens = []
		labels = []
		spans = []
		counter = 0
		span_start = -1
		span_end = -1
		for line in data.split("\n"): # this loop is same than version 1
			if line.startswith("#") or line=="":
				continue
			else:
				fields = line.split("\t") # Token
				label = fields[-1]
				if "-" in fields[0] or "." in fields[0]: # Multi-Word Expression or Ellips : No pred shall be there....
					continue
				elif self.LAB_CONN_B in label:
					if span_start > -1: # add span
						if span_end == -1:
							span_end = span_start
						spans.append((span_start,span_end))
						span_end = -1
					label = self.LAB_CONN_B
					span_start = counter
				elif self.LAB_CONN_I in label:
					label = self.LAB_CONN_I
					span_end = counter
				else:
					label = "_"
					if span_start > -1:  # Add span
						if span_end == -1:
							span_end = span_start
						spans.append((span_start,span_end))
						span_start = -1
						span_end = -1

				tokens.append(fields[1])
				labels.append(label)
				counter +=1
		
		if span_start > -1 and span_end > -1:  # Add last span
			spans.append((span_start,span_end))

		if not self.LAB_CONN_B in labels:
			exit(f"Unrecognized labels. Expecting: {self.LAB_CONN_B}, {self.LAB_CONN_I}, {self.LAB_CONN_O}...")
			
		return tokens, labels, spans


class EDUsEvaluation(Evaluation):
	"""
	Specific evaluation class for EDUs segmentation.
	:parse conllu-style data
	:eval upon first token identification
	"""
	LAB_SEG_B = "Seg=B-seg"		#"BeginSeg=Yes"
	LAB_SEG_I = "Seg=O"			#"_" 

	def __init__(self, name, gold_path, pred_path, str_i=False, no_b=False):
		super().__init__(name)
		self.mode = "edu"
		self.seg_type = "EDUs"
		self.g_path = gold_path
		self.p_path = pred_path
		self.opt_str_i = str_i
		self.no_b = True if "conllu" in gold_path.split(os.sep)[-1] and no_b==True else False # relevant only in conllu

		self.output['seg_type'] = self.seg_type

	def compute_scores(self):
		"""
		:param gold_file: Gold shared task file
		:param pred_file: File with predictions
		:param string_input: If True, files are replaced by strings with file contents (for import inside other scripts)
		:param no_b: If True, for conllu files, for EDU files, compute scores of edu_start only for edu_start != sentence_start
		:return: dictionary of scores for printing
		"""
		gold_tokens, gold_labels, gold_spans = self.parse_edu_data(self.g_path, self.opt_str_i, self.no_b)
		pred_tokens, pred_labels, pred_spans = self.parse_edu_data(self.p_path, self.opt_str_i, self.no_b)

		self.output['tok_count'] = len(gold_tokens)

		self.check_tokens_number(gold_tokens, pred_tokens)
		self.check_identical_tokens(gold_tokens, pred_tokens)
		tp, fp, fn = self.compare_labels(gold_labels, pred_labels)
		self.compute_PRF_metrics(tp, fp, fn)

	def compare_labels(self, gold_labels, pred_labels):

		true_positive = 0
		false_positive = 0
		false_negative = 0

		for i, gold_label in enumerate(gold_labels): # not verified
			pred_label = pred_labels[i]
			if gold_label == pred_label:
				if gold_label == "_":
					continue
				else:
					true_positive += 1
			else:
				if pred_label == "_":
					false_negative += 1
				else:
					if gold_label == "_":
						false_positive += 1
					else:  # I-Conn/B-Conn mismatch ?
						false_positive +=1
			
		return true_positive, false_positive, false_negative

	def parse_edu_data(self, path, str_i, no_b):
		"""
		LABEL = in last column
		"""
		data = self.get_data(path, str_i)
		tokens = []
		labels = []
		spans = []
		counter = 0
		span_start = -1
		span_end = -1
		for line in data.split("\n"): # this loop is same than version 1
			if line.startswith("#") or line=="":
				continue
			else:
				fields = line.split("\t") # Token
				label = fields[-1]
				if "-" in fields[0] or "." in fields[0]: # Multi-Word Expression or Ellips : No pred shall be there....
					continue
				elif no_b==True and fields[0]=="1":
					label = "_"
				elif self.LAB_SEG_B in label:
					label = self.LAB_SEG_B
				else:
					label = "_" # 🚩
					if span_start > -1:  # Add span
						if span_end == -1:
							span_end = span_start
						spans.append((span_start,span_end))
						span_start = -1
						span_end = -1

				tokens.append(fields[1])
				labels.append(label)
				counter +=1

		if span_start > -1 and span_end > -1:  # Add last span
			spans.append((span_start,span_end))

		if not self.LAB_SEG_B in labels:
			exit(f"Unrecognized labels. Expecting: {self.LAB_SEG_B}, {self.LAB_SEG_I}...")

		return tokens, labels, spans



if __name__ == "__main__":

	p = argparse.ArgumentParser()
	p.add_argument("-g", "--goldfile",help="Shared task gold file in .tok or .conll format.")
	p.add_argument("-p", "--predfile",help="Corresponding file with system predictions.")
	p.add_argument("-s","--string_input",action="store_true",help="Whether inputs are file names or strings.")
	p.add_argument("-nb", "--no_boundary_edu", default=False, action='store_true', help="Does not count EDU that starts at beginning of sentence.")
	p.add_argument("-rt", "--rel_type", default=False, action='store_true', help="Eval relations types instead of label.")
					


	opts = p.parse_args()

	name = opts.goldfile.split(os.sep)[-1] if os.path.isfile(opts.goldfile) else opts.goldfile[0:20] + "..."


	if name.endswith(".rels"):
		my_eval = RelationsEvaluation(name, opts.goldfile, opts.predfile, opts.string_input, opts.rel_type)
	else:
		if "pdtb" in name:
			my_eval = ConnectivesEvaluation(name, opts.goldfile, opts.predfile, opts.string_input)
		else:
			my_eval = EDUsEvaluation(name, opts.goldfile, opts.predfile, opts.string_input, opts.no_boundary_edu)

	my_eval.compute_scores()
	my_eval.print_results()

