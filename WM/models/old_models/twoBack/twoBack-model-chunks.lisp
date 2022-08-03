;;; Declarative chunks for zero-back HCP WM model

;;;(add-dm 
;;;	(cue isa chunk)
;;;	(find isa chunk)
;;;	(parse isa chunk)
;;;	(encode isa chunk)
;;;	(compare isa chunk)
;;;	(retrieve isa chunk)
;;;	(stimulus isa chunk))
	
;;; create and set the initial goal
(add-dm (do-nback isa parse-item state find nback nil n2look nil lastitem nothing updatecount nil category nil end-update nil)
		(selfChunk isa self identity me))
		
(goal-focus do-nback)
