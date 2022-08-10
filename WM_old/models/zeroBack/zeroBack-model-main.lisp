;;; model to perform 0-back condition of the Human Connectome Project working memory task


(clear-all)

(define-model zeroBack-HCP_WM

(sgp :v            		   nil
	 :trace-detail 		   high
	 :auto-attend  		   t
	 :mp           		   1
	 :esc		   		   t
	 :bll				   nil
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

;;; declare blank chunk-type for ITI
(chunk-type (blank (:include visual-object))
			test)
			
;;; set the similarity of the cue and stimulus chunks
;;; how to do this from python?
;(set-similarities (cue stimulus -0.1))


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

(P parse-cue-into-imaginal
	=goal>
		ISA         parse-item
		state		parse
	=visual>
		kind		=kind
		nback		=nback
		category	=category
		item		=cue
	?imaginal>
		state		free
==>
	@imaginal>
		=visual
	=visual>
	=goal>
		state		retrieve
		nback		=nback	
		target		=kind
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


(P retrieve-cue
	=goal>
		ISA         parse-item
		state       retrieve
	=imaginal>
		ISA         item
		kind		stimulus
		category    =category
	?retrieval>
		state       free
==>
	=imaginal>
	+retrieval>
		ISA         item
		kind		cue
		category    =category
	=goal>
		state       compare
)

(P interrupt-long-retrieval
	=goal>
		ISA         parse-item
		state		compare
	=visual>
		value		"blank"
	?retrieval>
		state		busy
==>
	!eval! (collect-no-response)
	-imaginal>
	+retrieval>
		:rt-value	10
		:mp-value	nil
		ISA			self
		identity	other        ; maybe change this to nil (which would test for the absence of the slot)
	=goal>
		state		parse
)

(P compare-retrieval-fail
	=goal>
		ISA         parse-item
		state       compare
	?retrieval>
		state       error
==>
	!eval! (collect-no-response)
	-visual>
	-imaginal>
	=goal>
		state       parse
)

(P compare-retrieval-match
	=goal>
		ISA        parse-item
		state      compare
	=imaginal>
		item       =ID
	=retrieval>
		item       =ID
	?manual>
		state	   free
	?visual>
		buffer	   full
==>
	-visual>
	+manual>
		ISA        motor-command
		cmd		   punch
		hand	   left
		finger	   index
	=goal>
		state      parse
)

(P compare-retrieval-mismatch
	=goal>
		ISA        parse-item
		state      compare
	=imaginal>
		item       =ID
	=retrieval>
		- item     =ID
	?manual>
		state	   free
	?visual>
		buffer	   full
==>
	-visual>
	+manual>
		ISA        motor-command
		cmd		   punch
		hand	   right
		finger	   index
	=goal>
		state      parse
)

(spp interrupt-long-retrieval :at 0)
(add-act-r-command "collect-response" 'collect-response)
(monitor-act-r-command "output-key" "collect-response")

)
