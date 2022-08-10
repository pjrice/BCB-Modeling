;;; model to perform 0-back condition of the Human Connectome Project working memory task


(clear-all)

(define-model twoBack-HCP_WM

(sgp :v            		   t
	 :trace-detail 		   high
	 :auto-attend  		   t
	 :mp           		   1
	 :esc		   		   t
	 :bll				   0.5
	 :mas				   1.0
	 :ans                  0.2
	 ;:ga				   1.0
	 ;:imaginal-activation  1.0
	 :nsji				   nil
	 ;:nsji					t
	 :sji-hook             linear-activation-spread
	 :retrieved-chunk-hook record-retrieved-chunk
	 ;:lf		   		   0.5
	 ;:imaginal-delay	   0.2
)

;;; declare chunk-types for:
;;; a chunk to represent the task goal 
;;; chunks to represent cues and stimuli
;;; a chunk to represent "the self" - for the interrupt-long-retrieval production
(chunk-type parse-item state nback target)
(chunk-type item kind category item)
(chunk-type self identity)

;;; declare stimulus and cue chunk-types for visicon-update in the device
(chunk-type (stimulus
             (:include visual-object))
            category item kind)
(chunk-type (cue (:include stimulus))
            nback)

;;; declare stimulus-window chunk-type for storing rehearsal window stimulus information		
(chunk-type stimulus-window item kind nback)

;;; declare blank chunk-type for ITI
(chunk-type (blank (:include visual-object))
			test)

;;; declare chunk-types for counting; straight from tutorial			
(chunk-type number number next)

;;; add counting chunk-types to declarative memory; straight from tutorial
(add-dm
 (one ISA number number one next two)
 (two ISA number number two next three))
 
 ;;; set number chunk reference-counts to arbitrarily high value to make them available
(sdp one :reference-count 100)
(sdp two :reference-count 100)



;;;PARSING;;;

(p find-something
   	=goal>
		ISA         parse-item
		state       find
	?visual>
		state       free
		buffer      empty
    ?visual-location>
        buffer      empty
==>
	+visual-location>
		- kind		nil
	=goal>
		state		parse
)

(P parse-nb-cue-into-imaginal
	=goal>
		ISA         parse-item
		state		parse
	=visual>
		nback		=nback
		category	nil
		item		nil
	?imaginal>
		state		free
==>
	@imaginal>
		=visual
	=visual>
	=goal>
		state		retrieve
		lastitem	nothing
		updatecount	nil
		nback		=nback
)

(P wait-after-cue
	=goal>
		ISA			parse-item
		state		retrieve
	=imaginal>
		ISA			item
		kind		cue
	?visual>
		buffer		full
==>
	-visual>
	=goal>
		state		parse
)

(P parse-stim-into-imaginal
	=goal>
		ISA         parse-item
		state		parse
	=visual>
		kind		=kind
		nback		nil 
		category	=category
		item		=stimulus
	?imaginal>
		state		free
==>
	@imaginal>
		=visual
	=visual>
	=goal>
		state		retrieve
		updatecount	nil
)

;;;RETRIEVAL;;;

(P retrieve-stimulus-window
	=goal>
		ISA			parse-item
		state		retrieve
		- nback		zero
		nback		=nbackval
	=imaginal>
		ISA			item
	  - kind		cue
		kind		=kind
	?retrieval>
		state		free
==>
	=imaginal>
	+retrieval>						;;;here the 'item' slot of the chunk in imaginal buffer could also be specified; but, would require declaring similarities between all stimulus chunks. Category could also be specified; same similarity issue
		ISA			stimulus-window		
	  - kind		cue             ;;;is there a better way to NOT retrieve a cue chunk?
		kind		=kind
		nback		=nbackval
	=goal>
		state		compare
)

;;;RESPONSE;;;

(P compare-no-stimulus-window-to-imaginal      ;;;this will probably only fire on one of the first 1-3 trials (depending on nback) of the task now; otherwise, some stimulus-window chunk with an 'nback' slot will exist to be retrieved. Specifying category/item in the retrieval request could change that
	=goal>
		ISA			parse-item
		- nback		zero
		state		compare
	?retrieval>
		state		error
	?manual>
		state		free
==>
	-visual>
	+manual>
		ISA			motor-command
		cmd			punch
		hand		left
		finger		index
	=goal>
		state		initialize-updatecount
)

(P compare-stimulus-window-to-imaginal-match
	=goal>
		ISA			parse-item
		state		compare
	=imaginal>
		item		=ID
	=retrieval>
		item		=ID
	?manual>
		state		free
	?visual>
		buffer		full
==>
	-visual>
	=imaginal>
	=retrieval>
	+manual>
		ISA			motor-command
		cmd			punch
		hand		left
		finger		index
	=goal>
		state		initialize-updatecount	
)

(P compare-stimulus-window-to-imaginal-mismatch
	=goal>
		ISA			parse-item
		state		compare
		nback		=nbackval
	=imaginal>
		item		=ID
	=retrieval>
		- item		=ID
	?manual>
		state		free
	?visual>
		buffer		full
==>
	-visual>
	=imaginal>
	=retrieval>
	+manual>
		ISA			motor-command
		cmd			punch
		hand		right
		finger		index
	=goal>
		state		initialize-updatecount
)

;;;UPDATING STIMULUS-WINDOW;;;

(p initialize-updatecount
	=goal>
		ISA			parse-item
		updatecount	nil
		state		initialize-updatecount
==>
	=goal>
		ISA			parse-item
		updatecount	one
		state		update-stimulus-window
)

(P update-stimulus-window
	=goal>
		ISA			parse-item
		updatecount	=updatecount
		state		update-stimulus-window
	=imaginal>
		item		=ID
		kind		=kind
	?imaginal>
		state		free 
==>
	+imaginal>
		ISA			stimulus-window
		item		=ID
		kind		=kind
		nback		=updatecount
	=goal>
		lastitem	=ID
		state		increment-updatecount
)

(P increment-updatecount1
	=goal>
		ISA			parse-item
		nback		=nbackval
	  - updatecount	=nbackval
	    updatecount	=updatecount
		state		increment-updatecount
==>
	+retrieval>
		number      =updatecount
	=goal>
		ISA         parse-item
		state		get-new-updatecount
)

(P increment-updatecount-and-retrieve-previous
	=goal>
		ISA			parse-item
		updatecount	=updatecount
		state		get-new-updatecount
	=retrieval>
		ISA			number
		next		=new-updatecount
==>
	+retrieval>
		ISA			stimulus-window
		kind		stimulus							
		nback		=updatecount
	=goal>
		ISA			parse-item
		updatecount	=new-updatecount
		state		update-stimulus-window-from-retrieval
)

(P update-stimulus-window-from-retrieval
	=goal>
		ISA			parse-item
		updatecount	=updatecount
		state		update-stimulus-window-from-retrieval
	=retrieval>
		item		=item
		kind		=kind
	?imaginal>
		state		free
==>
	+imaginal>
		item		=item
		kind		=kind
		nback		=updatecount
	=goal>
		ISA			parse-item
		state		increment-updatecount
)

(P stop-updatecount
	=goal>
		ISA         parse-item
		nback		=nbackval
		updatecount	=nbackval
		state		increment-updatecount
==>
	=goal>
		ISA			parse-item
		state		rehearse
)

;;;REHEARSAL;;;

(P rehearse-stimulus-window
	=goal>
		ISA			parse-item
		state		rehearse
	=imaginal>
		ISA			stimulus-window
		item		=item
		nback		=nback
	?visual>
		buffer		empty
	?retrieval>
		state		free
==>
	-imaginal>
	+retrieval>
		ISA			stimulus-window
		item		=item
		nback		=nback
	=goal>
		state		rehearse	
	
)

(P rehearse-stimulus-window-loop
	=goal>
		ISA			parse-item
		state		rehearse
	?imaginal>
		buffer		empty
	?retrieval>
		buffer		full
		state		free
	=retrieval>
	?visual>
		buffer		empty
==>
	@imaginal>
		=retrieval
	=goal>
		state		rehearse	
	
)

(P break-rehearsal-loop
	=goal>
		ISA			parse-item
		state		rehearse
	=visual>
		- item		nil
==>
	=visual>
	=goal>
		state		parse
)


(add-act-r-command "collect-response" 'collect-response)
(monitor-act-r-command "output-key" "collect-response")

)
