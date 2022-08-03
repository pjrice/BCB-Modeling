;;; model to perform 0-back condition of the Human Connectome Project working memory task


(clear-all)

(define-model twoBack-HCP_WM

(sgp :v            		   nil
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
(chunk-type stimulus-window one two three)


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

(P parse-zb-cue-into-imaginal
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
		nback		=nback
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


(P retrieve-stimulus-window
	=goal>
		ISA			parse-item
		state		retrieve
		- nback		zero
		lastitem	=lastitem
	=imaginal>
		ISA			item
		kind		stimulus
		category	=category
	?retrieval>
		state		free
==>
	=imaginal>
	+retrieval>
		ISA			stimulus-window
		one			=lastitem
	=goal>
		state		compare
)

(P retrieve-zb-cue
	=goal>
		ISA         parse-item
		nback		zero
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

(P compare-no-stimulus-window-to-imaginal
	=goal>
		ISA			parse-item
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
		state		encode-stimulus-window
	
)

(P compare-stimulus-window-to-imaginal-match
	=goal>
		ISA			parse-item
		state		compare
		nback		=nbackval
	=imaginal>
		item		=ID
	=retrieval>
		=nbackval	=ID
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
		state		encode-stimulus-window	
)

(P compare-stimulus-window-to-imaginal-mismatch
	=goal>
		ISA			parse-item
		state		compare
		nback		=nbackval
	=imaginal>
		item		=ID
	=retrieval>
		- =nbackval	=ID
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
		state		encode-stimulus-window	
)

(P compare-retrieval-match
	=goal>
		ISA        parse-item
		nback		zero
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
		nback		zero
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

(P initialize-stimulus-window1
	=goal>
		ISA			parse-item
		state		encode-stimulus-window
		lastitem	nothing
	=imaginal>
		item		=ID
	?imaginal>
		state		free
	?retrieval>
		state		error
==>
	+imaginal>
		ISA			stimulus-window
		one			=ID
		two			nothing
		three		nothing
	=goal>
		lastitem	=ID
		state		rehearse
)

(P initialize-stimulus-window2
	=goal>
		ISA			parse-item
		state		encode-stimulus-window
	=imaginal>
		item		=ID
	?imaginal>
		state		free
	=retrieval>
		one			=lastitem
		two			nothing
		three		nothing
==>
	+imaginal>
		ISA			stimulus-window
		one			=ID
		two			=lastitem
		three		nothing
	=goal>
		lastitem	=ID
		state		rehearse
)

(P update-stimulus-window
	=goal>
		ISA			parse-item
		state		encode-stimulus-window
	=imaginal>
		item		=ID
	?imaginal>
		state		free
	=retrieval>
		one			=one-back
		- two 		nothing
		two			=two-back
==>
	+imaginal>
		ISA			stimulus-window
		one			=ID
		two			=one-back
		three		=two-back
	=goal>
		lastitem	=ID
		state		rehearse
)

(P rehearse-new-stimulus-window
	=goal>
		ISA			parse-item
		state		rehearse
	=imaginal>
		ISA			stimulus-window
		one			=item-one
		two			=item-two
		three		=item-three
	?visual>
		buffer		empty
	?retrieval>
		state		free
==>
	-imaginal>
	+retrieval>
		ISA			stimulus-window
		one			=item-one
		two			=item-two
		three		=item-three
	=goal>
		state		rehearse	
	
)

(P rehearse-new-stimulus-window-loop
	=goal>
		ISA			parse-item
		state		rehearse
	?imaginal>
		buffer		empty
	?retrieval>
		buffer		full
		state		free
	=retrieval>
		ISA			stimulus-window
		one			=first
		two			=second
		three		=third
	?visual>
		buffer		empty
==>
	+imaginal>
		ISA			stimulus-window
		one			=first
		two			=second
		three		=third
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

(P break-rehearsal-loop-during-fixation
	=goal>
		ISA			parse-item
		state		rehearse
	=visual>
		value		"fix"
==>
	=visual>
	=goal>
		state		parse
)


(spp interrupt-long-retrieval :at 0)
(add-act-r-command "collect-response" 'collect-response)
(monitor-act-r-command "output-key" "collect-response")

)
