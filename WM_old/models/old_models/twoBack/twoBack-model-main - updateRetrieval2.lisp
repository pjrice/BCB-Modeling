;;; model to perform 2-back condition of the Human Connectome Project working memory task


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

(add-dm (one ISA number number one next two previous nil)
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
		category 	nil
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
	?visual>
		scene-change t
	=visual>
	  - item		nil
		category	=category
==>
	=visual>
	=goal>
		category	=category
		state		compare
)

(P parse-stim-presence
	=goal>
		ISA         parse-item
	  - lastitem	nothing
		state		parse
	?visual>
		scene-change t
	=visual>
	  - item		nil
	?imaginal>
		state		free
==>
	=visual>
	=goal>
		state		compare
)

;;;RESPONSE;;;

(P respond-for-no-stimulus-window
	=goal>
		ISA			parse-item
		state		compare
	?manual>
		state		free
	?imaginal>
		buffer		empty
==>
	!eval! (collect-imaginal-slots)
	+manual>
		ISA			motor-command
		cmd			punch
		hand		right
		finger		index
	=goal>
		state		initialize-update
	
)

(P compare-stimulus-window-to-imaginal-match
	=goal>
		ISA			parse-item
		state		compare
		nback		=nbackval
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
		state		initialize-update
)

(P compare-stimulus-window-to-imaginal-mismatch
	=goal>
		ISA			parse-item
		state		compare
		nback		=nbackval
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
		state		initialize-update
)

;;;UPDATING STIMULUS-WINDOW;;;

(P initialize-stimulus-window
	=goal>
		ISA			parse-item
		state		initialize-update
		category	=category
	=visual>
		item		=ID
	?imaginal>
		state		free
		buffer		empty
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
		state		initialize-update
	?imaginal>
		buffer		full
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
		state		update
)

(P wrong-number-fact-retrieved
	=goal>
		ISA			parse-item
		state		update
		updatecount =updatecount
	=retrieval>
	  - number		=updatecount
==>
	=goal>
		state		retrieve-number-fact
)

(P retrieve-stimulus-for-window-update
	=goal>
		ISA			parse-item
		state		update
		lastitem	=lastitem
		updatecount =updatecount
		category	=category
	=retrieval>
		number		=updatecount
		next		=next-update
==>
	+retrieval>
		category	=category
		item		=lastitem
	=goal>
		updatecount	=next-update
)

(P update-window-with-retrieved-stimulus
	=goal>
		ISA			parse-item
		updatecount	=updatecount
		state		update
	?retrieval>
		state		free
	=retrieval>
		item		=update-stimulus
	=imaginal>
		=updatecount =new-lastitem
==>
	=imaginal>
		=updatecount =update-stimulus
	=goal>
		lastitem	=new-lastitem
		state		retrieve-number-fact
)

(P break-update-loop-and-discard-old-item
	=goal>
		ISA			parse-item
		state		retrieve-number-fact
		updatecount	three					
	?visual>
		scene-change nil
	=visual>
		item		=ID
==>
	=goal>
		lastitem	=ID
		updatecount	one
		state		rehearse
)

(P break-update-loop-and-discard-old-item-in-ITI
	=goal>
		ISA			parse-item
		state		retrieve-number-fact
		updatecount	three
	=visual>
		value		"blank"
==>
	=visual>
	=goal>
		lastitem	nothing
		updatecount	nil
		state		rehearse
)

(P break-update-loop-and-discard-old-item-on-new-trial
	=goal>
		ISA			parse-item
		state		update
	?visual>
		scene-change t
	=visual>
	  - item		nil
==>
	=visual>
	=goal>
		lastitem	nothing
		updatecount	nil
		state		parse
)

;;;REHEARSAL;;;

(P initialize-rehearsal-loop
	=goal>
		category	=category
		updatecount	=updatecount
		state		rehearse
	?retrieval>
		buffer		empty
		state		free
	=imaginal>
		=updatecount =rehearsal-item
==>
	=imaginal>
	+retrieval
		category	=category
		item		=rehearsal-item
	=goal>
		state		retrieve-number-fact
)




(P rehearse-new-stimulus-window
	=goal>
		ISA			parse-item
		category	=category
		state		rehearse
	=imaginal>
		ISA			stimulus-window
		one			=item-one
		two			=item-two
		three		=item-three
	?retrieval>
		state		free
==>
	=imaginal>
	+retrieval>
		ISA			stimulus-window
		category	=category
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
	?retrieval>
		buffer		full
		state		free
	=retrieval>
		ISA			stimulus-window
		category	=category
		one			=item-one
		two			=item-two
		three		=item-three
==>
	+imaginal>
		category	=category
		one			=item-one
		two			=item-two
		three		=item-three
	=goal>
		lastitem	=item-one
		state		rehearse	
	
)

(P break-rehearsal-loop
	=goal>
		ISA			parse-item
		state		rehearse
	?visual>
		scene-change t
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
	?visual>
		scene-change t
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
	?visual>
		scene-change t
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






























