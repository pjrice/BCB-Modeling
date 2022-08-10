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
(chunk-type stimulus-window one two three)


;;; declare blank chunk-type for ITI
(chunk-type (blank (:include visual-object))
			test)
			
;;; declare chunk-types for counting; straight from tutorial			
(chunk-type number number next previous)

;;; add counting chunk-types to declarative memory; straight from tutorial
(add-dm
 (one ISA number number one next two previous nil)
 (two ISA number number two next three previous one)
 (three ISA number number three next four previous two))
 
 ;;; set number chunk reference-counts to arbitrarily high value to make them available
(sdp one :reference-count 100)
(sdp two :reference-count 100)
(sdp three :reference-count 100)



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
		updatecount nil
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

;;;RETRIEVAL;;;

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
;;;RESPONSE;;;

(P compare-no-stimulus-window-to-imaginal
	=goal>
		ISA			parse-item
		state		compare
	?retrieval>
		state		error
	?manual>
		state		free
==>
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
		- =nbackval	=ID
	?manual>
		state		free
	?visual>
		buffer		full
==>
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
		updatecount	three
		state		encode-stimulus-window
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
	-visual>
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
	-visual>
	+imaginal>
		ISA			stimulus-window
		one			=ID
		two			=lastitem
		three		nothing
	=goal>
		lastitem	=ID
		state		rehearse
)

(P encode-old-stimulus-window
	=goal>
		ISA			parse-item
		state		encode-stimulus-window
		updatecount =updatecount
	?imaginal>
		state		free
	=imaginal>
	=retrieval>
	  -	two			nothing
==>
	=retrieval>
	@imaginal>
		=retrieval
	=goal>
		state		update-stimulus-window3
)

(P update-stimulus-window3
	=goal>
		ISA			parse-item
		state		update-stimulus-window3
		updatecount =updatecount
	?imaginal>
		state		free
	=imaginal>
	=retrieval>
		- two 		nothing
		two			=new-three
==>
	=imaginal>
		=updatecount =new-three
	=goal>
		state		decrement-updatecount
)

(P decrement-updatecount
	=goal>
		ISA			parse-item
	  - updatecount	one
	    updatecount	=updatecount
		state		decrement-updatecount
==>
	+retrieval>
		number      =updatecount
	=goal>
		ISA         parse-item
		state		get-new-updatecount
)

(P decrement-updatecount-retrieval-error
	=goal>
		ISA			parse-item
		state		get-new-updatecount
	  - updatecount two
	=retrieval>
		previous	nil
==>
	=goal>
		ISA			parse-item
		state		decrement-updatecount
)

(P update-updatecount
	=goal>
		ISA			parse-item
		updatecount =prev-updatecount
		state		get-new-updatecount
	=retrieval>
		previous	=new-updatecount
==>
	=goal>
		ISA			parse-item
		prevupdate  =prev-updatecount
		updatecount =new-updatecount
		state		update-stimulus-window
)

(P update-stimulus-window2
	=goal>
		ISA			parse-item
		state		update-stimulus-window
		updatecount =updatecount
		lastitem	=new-two
	=imaginal>
==>
	=imaginal>
		=updatecount =new-two
	=goal>
		lastitem	nil
		state		decrement-updatecount
)

(P update-stimulus-window1
	=goal>
		ISA			parse-item
		state		update-stimulus-window
		updatecount =updatecount
		lastitem	nil
	=visual>
		item		=new-one
	=imaginal>
==>
	=imaginal>
		=updatecount =new-one
	=goal>
		lastitem	=new-one
		state		rehearse
)

;;;REHEARSAL;;;

(P rehearse-new-stimulus-window
	=goal>
		ISA			parse-item
		state		rehearse
	=imaginal>
		ISA			stimulus-window
		one			=item-one
		two			=item-two
		three		=item-three
	?retrieval>
		state		free
	?visual>
		buffer		empty
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

(P break-rehearsal-loop-on-cue
	=goal>
		ISA			parse-item
		state		rehearse
	=visual>
		kind		cue
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
