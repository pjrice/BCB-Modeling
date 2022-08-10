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
	 :ga				   1.0
	 :imaginal-activation  1.0
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
(chunk-type stimulus-window one two three category)


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
(sdp one :reference-count 10000)
(sdp two :reference-count 10000)
(sdp three :reference-count 10000)



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

(P parse-nb-cue-info
	=goal>
		ISA         parse-item
		state		parse
	=visual>
		nback		=nback
		category	nil
		item		nil

==>
	=visual>
	=goal>
		state		retrieve
		lastitem	nothing
		nback		=nback
)

(P wait-after-cue
	=goal>
		ISA			parse-item
		state		retrieve
	?visual>
		buffer		full
	=visual>
		kind		cue
==>
	-imaginal>
	-retrieval>
	=goal>
		state		parse
)

(P parse-stim-presence-update-goal-category
	=goal>
		ISA         parse-item
		lastitem	nothing
		state		parse
	=visual>
	  - item		nil
		nback		nil
		category	=category
==>
	@imaginal>
		=visual
	=visual>
	=goal>
		category	=category
		state		retrieve-nback-fact
)

(P parse-stim-presence
	=goal>
		ISA         parse-item
	  - lastitem	nothing
		state		parse
	=visual>
	  - item		nil
		nback		nil
==>
	@imaginal>
		=visual
	=visual>
	=goal>
		state		retrieve-nback-fact
)

(P retrieve-nback-fact
	=goal>
		ISA			parse-item
		state		retrieve-nback-fact
		nback		=nback
	?retrieval>
		state		free
==>
	+retrieval>
		number		=nback
	=goal>
		ISA			parse-item
		state		retrieve
)

;;;RETRIEVAL;;;

(P retrieve-stimulus-window
	=goal>
		ISA			parse-item
		state		retrieve
		category	=category
		lastitem	=lastitem
	=visual>
		kind		stimulus
;		item		=ID
	=retrieval>
		number		=nback
==>
	=visual>
	+retrieval>
		ISA			stimulus-window
		one			=lastitem
;	    =nback		=ID					;;;doesn't seem to break retrieval when "one" is mistakenly retrieved by retrieve-nback-fact and two different specifications for the "one" slot are passed
		category	=category
	=goal>
		n2look		=nback
		state		encode-stimulus-window
)

(P retrieve-stimulus-window-error
	=goal>
		ISA			parse-item
		state		encode-stimulus-window
	?retrieval>
		state		error
==>
	=goal>
		ISA			parse-item
		state		compare-error
)

(P encode-stimulus-window-to-imaginal
	=goal>
		ISA			parse-item
		category	=category
		state		encode-stimulus-window
	?retrieval>
		buffer		full
	=retrieval>
		category	=category
==>
	@imaginal>
		=retrieval
	=goal>
		ISA			parse-item
		state		compare
)

(P mistaken-block-stim-window-retrieved
	=goal>
		ISA			parse-item
		category	=category
		state		encode-stimulus-window
	?retrieval>
		buffer		full
	=retrieval>
	  - category	=category
==>
	=goal>
		ISA			parse-item
		state		compare-error
)

;;;RESPONSE;;;

(P respond-for-no-stimulus-window
	=goal>
		ISA			parse-item
		state		compare-error
	?manual>
		state		free
==>
	!eval! (collect-imaginal-slots)
	+manual>
		ISA			motor-command
		cmd			punch
		hand		left
		finger		index
	=goal>
		state		initialize-update
	
)

(P compare-stimulus-window-to-imaginal-match
	=goal>
		ISA			parse-item
		state		compare
		n2look		=nbackval
	=visual>
		item		=ID
	=imaginal>
		=nbackval	=ID
	?manual>
		state		free
==>
	!eval! (collect-imaginal-slots)
	=visual>
	=imaginal>
	+manual>
		ISA			motor-command
		cmd			punch
		hand		left
		finger		index
	=goal>
		n2look		nil
		state		initialize-update
)

(P compare-stimulus-window-to-imaginal-mismatch
	=goal>
		ISA			parse-item
		state		compare
		n2look		=nbackval
	=visual>
		item		=ID
	=imaginal>
	  - =nbackval	=ID
	?manual>
		state		free
==>
	!eval! (collect-imaginal-slots)
	=visual>
	=imaginal>
	+manual>
		ISA			motor-command
		cmd			punch
		hand		right
		finger		index
	=goal>
		n2look		nil
		state		initialize-update
)

;;;UPDATING STIMULUS-WINDOW;;;

(P initialize-stimulus-window
	=goal>
		ISA			parse-item
		state		initialize-update
		category	=category
		lastitem	nothing
	=visual>
		item		=ID
	?imaginal>
		state		free
==>
	-visual>
	+imaginal>
		ISA			stimulus-window
		one			=ID
		two			nothing
		three		nothing
		category	=category
	=goal>
		lastitem	=ID
		state		rehearse
)

(P initialize-stimulus-window-update
	=goal>
		ISA			parse-item
		updatecount	nil
	  - lastitem	nothing
		state		initialize-update
;	?retrieval>
;	  - state		error
	=visual>
		item		=ID
	=imaginal>
==>
	=visual>
	=imaginal>
		one			=ID
	=goal>
		ISA			parse-item
		updatecount	one
		state		retrieve-number-fact
)

(P retrieve-number-fact
	=goal>
		ISA			parse-item
		state		retrieve-number-fact
		updatecount	=updatecount
	?retrieval>
		state		free
==>
	+retrieval>
		number		=updatecount
	=goal>
		ISA			parse-item
		state		update-stimulus-window
)

(P update-stimulus-window
	=goal>
		ISA			parse-item
		state		update-stimulus-window
		updatecount =updatecount
		lastitem	=lastitem
	=retrieval>
		number		=updatecount
		next		=next-update
	=imaginal>
		=next-update =new-lastitem
==>
	=imaginal>
		=next-update =lastitem
	=goal>
		lastitem	=new-lastitem
		updatecount	=next-update
		state		retrieve-number-fact
)

(P wrong-number-fact-retrieved
	=goal>
		ISA			parse-item
		state		update-stimulus-window
		updatecount =updatecount
	=retrieval>
	  - number		=updatecount
==>
	=goal>
		state		retrieve-number-fact
)

(P break-update-loop-and-discard-old-item
	=goal>
		ISA			parse-item
		state		retrieve-number-fact
		updatecount	three					;;;if there was a production that fired in the cue period that figured out nback+1 and stored in goal buffer, the update mechanism could dynamically continue through the number of nbacks
	=visual>
		item		=ID
==>
	=goal>
		lastitem	=ID
		updatecount	nil
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
	-imaginal>
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
	-imaginal>
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
	-imaginal>
	=visual>
	=goal>
		state		parse
)

;;;ACT-R COMMANDS;;;

(add-act-r-command "collect-response" 'collect-response)
(monitor-act-r-command "output-key" "collect-response")

) ;end model declaration