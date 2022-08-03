;;; model to perform n-back condition of the Human Connectome Project working memory task


(clear-all)

(define-model nBack-HCP_WM

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
;	 :declarative-num-finsts 3
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


;;;COUNTING;;;

(P retrieve-number-fact
	=goal>
		state		retrieve-number-fact
		count		=count
	?retrieval>
		state		free
==>
	+retrieval>
		number		=count
	=goal>
		ISA			parse-item
		state		nfact-retrieved
)

(P wrong-number-fact-retrieved
	=goal>
		ISA			parse-item
		state		nfact-retrieved
		count 		=count
	=retrieval>
	  - number		=count
==>
	=goal>
		state		retrieve-number-fact
)

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
		state		retrieve-nback-stimulus
)

(P retrieve-nback-stimulus
	=goal>
		ISA			parse-item
		category	=category
		nback		=nback
		state		retrieve-nback-stimulus
	?imaginal>
		state		free
	?retrieval>
		state		free
	=imaginal>
		=nback		=nbackstim
	  - =nback		nothing	
==>
	=imaginal>
	+retrieval>
		category	=category
		item		=nbackstim		
	=goal>
		ISA			parse-item
		state		compare
)

(P no-nback-to-retrieve
	=goal>
		ISA			parse-item
		nback		=nback
		state		retrieve-nback-stimulus
	?imaginal>
		state		free
	?retrieval>
		state		free
	=imaginal>
	    =nback		nothing	
==>
	=imaginal>	
	=goal>
		ISA			parse-item
		state		compare
)

;;;RESPONSE;;;


(P respond-for-no-stimulus-window
	=goal>
		ISA			parse-item
		state		compare
	?manual>
		state		free
	?retrieval>
		buffer		empty
	  - state		busy
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
	=visual>
		item		=ID
	=retrieval>
		item		=ID
	?retrieval>
	  - state		busy
	?manual>
		state		free
==>
	!eval! (collect-imaginal-slots)
	=visual>
	=retrieval>
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
	=visual>
		item		=ID
	=retrieval>
	  - item		=ID
	?retrieval>
	  - state		busy
	?manual>
		state		free
==>
	!eval! (collect-imaginal-slots)
	=visual>
	=retrieval>
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
		count		one
		state		rehearse
)

(P initialize-stimulus-window-update
	=goal>
		count		nil
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
		count		one
		stage		updating
		state		retrieve-number-fact
)

(P retrieve-stimulus-for-window-update
	=goal>
		state		nfact-retrieved
		stage		updating
	  - lastitem  	nothing
		lastitem	=lastitem
		count 		=count
		category	=category
	=retrieval>
		number		=count
		next		=next-count
==>
	+retrieval>
;		:recently-retrieved t
; 		:mp-value	nil
		category	=category
		item		=lastitem
	=goal>
		count		=next-count
		state		update
)

(P update-window-with-retrieved-stimulus
	=goal>
		ISA			parse-item
		count		=count
		state		update
	?retrieval>
		state		free
	=retrieval>
		item		=update-stimulus
	=imaginal>
		=count 		=new-lastitem
==>
	=imaginal>
		=count 		=update-stimulus
	=goal>
		lastitem	=new-lastitem
		state		retrieve-number-fact
)

(P end-updating-nothing
	=goal>
		lastitem	nothing
		stage		updating
		state		retrieve-number-fact
	=visual>
		item		=new-lastitem
==>
	=goal>
		lastitem	=new-lastitem
		count		one
		state		rehearse
)

(P end-updating
	=goal>
		count		three
		stage		updating
		state		retrieve-number-fact
	=visual>
		item		=new-lastitem
==>
	=goal>
		lastitem	=new-lastitem
		count		one
		state		rehearse
)

;;;REHEARSAL;;;

(P rehearse-slot-item
	=goal>
		state		rehearse
		category	=category
		count		=count
	=imaginal>
	  - =count		nil
	  - =count		nothing
		=count		=rehearsal-item
	?retrieval>
		state		free
==>
	=imaginal>
	+retrieval>
		:mp-value	nil
		category	=category
		item		=rehearsal-item
	=goal>
		stage		rehearsal
		state		retrieve-number-fact
)

(P update-rehearsal-count
	=goal>
		state		nfact-retrieved
		stage		rehearsal
		count		=count
	=imaginal>
	=retrieval>
		number		=count
		next		=next-count
==>
	=imaginal>
	=goal>
		count		=next-count
		state		rehearse
)

(P reset-rehearsal-loop
	=goal>
		state		rehearse
		count		=count
	=imaginal>
		=count	nil
==>
	=imaginal>
	=goal>
		count		one
)

(P stop-rehearsal-nothing
	=goal>
		state		rehearse
		count		=count
	=imaginal>
		=count		nothing
==>
	=imaginal>
	=goal>
		count		nil
		stage		interact
		state		parse
)

(P break-rehearsal-loop
	=goal>
		stage		rehearsal
	?visual>
		scene-change t
	=visual>
	  - item 		nil
==>
	=visual>
	=goal>
		count		nil
		stage		interact
		state		parse
)

(P break-rehearsal-loop-on-cue
	=goal>
		stage		rehearsal
	?visual>
		scene-change t
	=visual>
		kind		cue
==>
	-imaginal>
	=visual>
	=goal>
		count		nil
		stage		interact
		state		parse
)

(P break-rehearsal-loop-on-fix
	=goal>
		stage		rehearsal
	?visual>
		scene-change t
	=visual>
		value		"fix"
==>
	=visual>
	=goal>
		count		nil
		stage		interact
		state		parse
)

;;;ACT-R COMMANDS;;;

(add-act-r-command "collect-response" 'collect-response)
(monitor-act-r-command "output-key" "collect-response")

) ;end model declaration






























