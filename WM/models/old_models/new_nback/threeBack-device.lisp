;;; device developed by Patrick Rice 2020
;;;
;;; this device interfaces with ACT-R and presents a version the Human Connectome Project (HCP) working memory (WM) task
;;;
;;; the text strings of the cue/stimuli images are presented on the window for simplicity
;;;
;;; HCP N-back task: - 8 blocks, 10 trials each. half of blocks are 0-back, other half are 2-back; four 15s fixation blocks. The first fix block occurs after the second block, and fix blocks occur every two blocks (so, the run ends with a fix block)
;;;					 - 2.5s cue at start of block (either 0-back exemplar or 2-back cue)
;;;					 - in each block, 2 trials are targets, 2-3 trials are non-target lures (repeated items in the wrong n-back position,either 1-back or 3-back; or in the case of 0-back, repeated non-target stimuli)
;;;					 - on each trial, stimulus presented for 2 seconds, then 500ms ITI
;;;					 - A full block is 27.5 seconds; a full session is (8*27.5)+(4*15) = 280 seconds ~ 4.7 mins
;;;
;;; only zero-back blocks are included in this version of the device

;;; ------------------------------------------------------------------
;;; N-BACK TASK PARAMETERS
;;; ------------------------------------------------------------------

;;; flag for ending the task
(defparameter *task-over* nil)

;;; timing of presentation
(defconstant +cueTime+ 2.5)
(defconstant +stimTime+ 2)
(defconstant +itiTime+ 0.5)
(defconstant +fixTime+ 15)

;;; window to present on
(defparameter *window* nil)

;;; parameters to track whether response has occurred
(defparameter *numTrials* 0)
(defparameter *numResponses* 0)

;;; list to store responses
(defparameter *responses* '())

;;; list to store response times
(defparameter *respTimes* '())

;;; list to store model chunk retrievals
(defparameter *retrievedChunks* '())

;;; list to store model imaginal buffer chunk on response
(defparameter *imaginalChunks* '())


;;; ------------------------------------------------------------------
;;; N-BACK TASK DATA STRUCTURES
;;; ------------------------------------------------------------------

;;; list of blocks that a fixation period occurs after
(defparameter *fix-blocks* '(1 3)
)

;;; each participant saw two sessions, and the order of presented stimuli was equivalent
;;; across participants, within session. So, hardcoded lists of stimuli
(defparameter *task-stimuli* '(( 
							  ((three nil nil) (body BP_006_BP2_BA.png) (body BP_001_BP1_BA.png) (body BP_005_BP19_BA.png) (body BP_006_BP2_BA.png) (body BP_005_BP19_BA.png) (body BP_003_BP16_BA.png) (body BP_001_BP1_BA.png) (body BP_004_BP18_BA.png) (body BP_003_BP16_BA.png) (body BP_004_BP18_BA.png))
							  ((three nil nil) (tool TO_002_TOOL2_BA.png) (tool TO_004_TOOL4_BA.png) (tool TO_002_TOOL2_BA.png) (tool TO_001_TOOL1_BA.png) (tool TO_004_TOOL4_BA.png) (tool TO_001_TOOL1_BA.png) (tool TO_006_TOOL6_BA.png) (tool TO_005_TOOL5_BA.png) (tool TO_003_TOOL3_BA.png) (tool TO_006_TOOL6_BA.png))
							  ((three nil nil) (face FC_008_F4.png) (face FC_012_F6.png) (face FC_008_F4.png) (face FC_008_F4.png) (face FC_010_F5.png) (face FC_007_M4.png) (face FC_009_M5.png) (face FC_010_F5.png) (face FC_011_M6.png) (face FC_010_F5.png))
							  ((three nil nil) (place PL_009_92037.png) (place PL_010_92038.png) (place PL_009_92037.png) (place PL_007_92026.png) (place PL_010_92038.png) (place PL_007_92026.png) (place PL_008_92033.png) (place PL_011_92044.png) (place PL_009_92037.png) (place PL_008_92033.png))
							 ) ;;; end session 1
							 ( 
							  ((three nil nil) (tool TO_018_TOOL18_BA.png) (tool TO_013_TOOL13_BA.png) (tool TO_014_TOOL14_BA.png) (tool TO_018_TOOL18_BA.png) (tool TO_016_TOOL16_BA.png) (tool TO_018_TOOL18_BA.png) (tool TO_018_TOOL18_BA.png) (tool TO_017_TOOL17_BA.png) (tool TO_015_TOOL15_BA.png) (tool TO_017_TOOL17_BA.png))
							  ((three nil nil) (face FC_017_M9.png) (face FC_016_F8.png) (face FC_017_M9.png) (face FC_017_M9.png) (face FC_015_M8.png) (face FC_018_F9.png) (face FC_014_F7.png) (face FC_015_M8.png) (face FC_014_F7.png) (face FC_013_M7.png))
							  ((three nil nil) (body BP_024_H3-T_BA.png) (body BP_025_H5-T_BA.png) (body BP_023_H25-T_BA.png) (body BP_024_H3-T_BA.png) (body BP_023_H25-T_BA.png) (body BP_023_H25-T_BA.png) (body BP_020_H17-T_BA.png) (body BP_019_H14-T_BA.png) (body BP_022_H24-T_BA.png) (body BP_019_H14-T_BA.png))
							  ((three nil nil) (place PL_016_SCENE_02.png) (place PL_015_SCENE_01.png) (place PL_020_SCENE_06.png) (place PL_019_SCENE_05.png) (place PL_020_SCENE_06.png) (place PL_019_SCENE_05.png) (place PL_017_SCENE_03.png) (place PL_020_SCENE_06.png) (place PL_016_SCENE_02.png) (place PL_017_SCENE_03.png))
							 ) ;;; end session 2
							)
)


;;; ------------------------------------------------------------------
;;; UTILITY FUNCTIONS
;;; ------------------------------------------------------------------


;;; This fuction collects the values of the the slots named 'one',
;;; 'two', and 'three' from the chunk currently in the imaginal buffer.
;;; If the chunk has no slots or there is no chunk, '(nil nil nil) is
;;; returned.
;;;

(defun read-imaginal-slots (&optional (slots '(one two three)))
  "Reads the contents of the imaginal buffer and returns them as a list"
  (let ((nwindow (first (no-output (buffer-chunk-fct '(imaginal))))))
    (if nwindow
        (mapcar #'(lambda (x)
                    (chunk-slot-value-fct nwindow x))
                slots)
        '(nil nil nil))))

(defun collect-imaginal-slots ()
	(push (read-imaginal-slots) *imaginalChunks*)
)

;;; retrieved-chunk-hook function
;;; has to handle retrieved chunks and fails
(defparameter chunk nil)
(defmethod record-retrieved-chunk (chunk)
	"Adds the value of the kind slot of the chunk input argument to the list *retrievedChunks*"
	(if (chunk-p-fct chunk)
		(push chunk *retrievedChunks*) ;;; pushes the name of the retrieved chunk to the list
		(push "failedRetrieval" *retrievedChunks*)
	)
	
)


;;;flat and linear :sji-hook equations
;;; provided by Andrea Stocco, 12/3/2020; thanks Andrea!
;;; updated by Andrea Stocco 12/4/2020 to return 0 for non-chunk slot values
(defun flat-activation-spread (source target)
  "Returns 1 if S == T or if S %in% T; 0 otherwise"
  (if (and (chunk-p-fct source)
	   (chunk-p-fct target))
      (if (or (eq-chunks-fct source target)
	      (member source (mapcar #'(lambda (x)
					 (chunk-slot-value-fct target x))
				     (chunk-filled-slots-list-fct target))
		      :test #'eq-chunks-fct))
	  1
	  0)
      0))

(defun linear-activation-spread (source target)
  "Returns 1 if S == T, of 1 X every S %in% T; 0 otherwise"
  (if (and (chunk-p-fct source)
	   (chunk-p-fct target))

      (if (eq-chunks-fct source target)
	  1
	  (let ((target-values (mapcar #'(lambda (x)
					   (chunk-slot-value-fct target x))
				       (chunk-filled-slots-list-fct target))))
	    (reduce #'+ (mapcar #'(lambda (x)
				    (if (eq-chunks-fct source x)
					1
					0))
				target-values))))
      0))

;;; function to end the task when it's over
(defun task-over (time)
	(or *task-over* (> time 1000000000))
)

;;; function to record model responses
;(defun collect-response (model key)
;	(declare (ignore model))
;	(push (mp-time) *respTimes*)
;	(push (format nil "~a" key) *responses*)
;	(incf *numResponses*)
;)

;;;; function to record when a model fails to respond
;(defun collect-no-response ()
;	(push nil *respTimes*)
;	(push nil *responses*)
;	(incf *numResponses*)
;)

(defun collect-response (model key)
	(declare (ignore model))
	(push (mp-time) *respTimes*)
	(push (format nil "~a" key) *responses*)
	(incf *numResponses*)
)

;;;; function to record when a model fails to respond
(defun collect-no-response ()
	(push nil *respTimes*)
	(push nil *responses*)
	(incf *numResponses*)
)

;;; function to combine cue timing, response timing, and response identity lists into a single list
(defun combine-lists (resp respTime retrievedChunks)
	(let ((combinedList '()))
		(loop for i in resp
			  for j in respTime
			  for k in retrievedChunks
			do (push (list i j k) combinedList))
		(nreverse combinedList)
	)
)

;;; function to write model responses and response times to file
(defun writeData (data fName)

	(with-open-file (out fName :direction :output :external-format :ascii)
		(dolist (segment data)
			(format out "~{~a~^, ~}~%" segment)
		)

	)

)

;;; visicon update function
(defun update-visicon (sesNum blkNum tNum tPhase)

	;;; updates the ACT-R visicon with the block's cue, the trial's stimulus, the trial's ITI, or one of the fixation periods
	;;; task-stimuli is a list of list of lists; a list of the two sessions, which are each lists of the session's 8 blocks, which are each lists of the block's 1 cue + 10 trials
	;;; sesNum indexes the session
	;;; blkNum indexes the block
	;;; tNum indexes the trial
	;;; tPhase determines whether we are presenting a stimulus (either cue or trial stim)
	;;; the time that the screen is presented for is handled by the schedule-event-relative call in the 'next' method below

	;;; remove everything before we put something new on - there are no "evolving" features in the task
	(delete-all-visicon-features)

	;;; puts a cue into the visicon
	(when (equal tNum 0)
		(let
			((nbackVal  (nth 0 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		     (cat    (nth 1 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		     (stim   (nth 2 (nth tNum (nth blkNum (nth sesNum *task-stimuli*))))))

			(add-visicon-features `(isa (visual-location cue)
										screen-x 200
										screen-y 200
										nback (nil ,nbackVal)
										category (nil ,cat)
										item (nil ,stim)
                                        kind (nil cue)
                                        )
			)
		)
	)

	;;; puts a stimulus into the visicon
	(when (and (> tNum 0)
			   (equal tPhase 'stimulus)
		  )
		(let
			((cat    (nth 0 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		     (stim   (nth 1 (nth tNum (nth blkNum (nth sesNum *task-stimuli*))))))

			(add-visicon-features `(isa (visual-location stimulus)
										screen-x 200
										screen-y 200
										category (nil ,cat)
										item (nil ,stim)
                                        kind (nil stimulus)
								   )
			)
		)
	)
	
	;;; presents a "blank" screen during the ITI
	(when (equal tPhase 'ITI)
		(add-visicon-features '(isa (visual-location blank)
									screen-x 200
									screen-y 200
									width 200
									height 200
									value "blank"
							   )
		)
	)

	;;; puts a fixation cross into the visicon
	(when (equal tPhase 'fix)
		(add-visicon-features '(isa (visual-location oval)
									screen-x 200
									screen-y 200
									width 200
									height 200
									value (oval "fix")

							   )

		)
	)

)

;;; task display function
(defun display-taskScreen (sesNum blkNum tNum tPhase)

	;;; displays the block's cue, the trial's stimulus, the trial's ITI, or one of the fixation periods
	;;; task-stimuli is a list of list of lists; a list of the two sessions, which are each lists of the session's 8 blocks, which are each lists of the block's 1 cue + 10 trials
	;;; sesNum indexes the session
	;;; blkNum indexes the block
	;;; tNum indexes the trial
	;;; tPhase determines whether we are presenting a stimulus (either cue or trial stim)
	;;; the time that the screen is presented for is handled by the schedule-event-relative call in the 'next' method below

	;;; for ITIs, the window is cleared and nothing is put on it for the duration of the ITI
	(clear-exp-window *window*)

	;;; displays the block's cue
	(when (equal tNum 0)
      (let
          ((nback  (nth 0 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		   (cat    (nth 1 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		   (stim   (nth 2 (nth tNum (nth blkNum (nth sesNum *task-stimuli*))))))

		  (add-text-to-exp-window  *window* nback :x 200 :y 100 :color 'black)
		  (add-text-to-exp-window  *window* cat :x 200 :y 200 :color 'black)
          (add-text-to-exp-window  *window* stim :x 200 :y 300 :color 'black)
        )
     )

	;;; displays the trial's stimulus
	(when (and (> tNum 0)
			   (equal tPhase 'stimulus)
		  )
      (let
          ((cat  (nth 0 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		   (stim (nth 1 (nth tNum (nth blkNum (nth sesNum *task-stimuli*)))))
		  )
		(add-text-to-exp-window  *window* cat :x 200 :y 200 :color 'black)
        (add-text-to-exp-window  *window* stim :x 200 :y 300 :color 'black)
        )
     )

	;;; displays a fixation period
	(when (equal tPhase 'fix)
      (add-line-to-exp-window *window*  (list 150 200) (list 250 200))
      (add-line-to-exp-window *window*  (list 200 150) (list 200 250))
	)
)

;;; updating functions

;;; function to update the session value
(defun update-ses (task session blkNum tNum tPhase)

	;;; when the fixation period after the last block of the first session has been presented:
	;;; - set the task-session of the task to 1
	(when (and (equal session 0)
			   (equal blkNum 3)
			   (equal tNum 10)
			   (equal tPhase 'fix)
		  )
		  (setf (task-session task) 1)
	)

	;;; when the fixation period after the last block of the second session has been presented:
	;;; - set the 'task-over' flag to true
	(when (and (equal session 1)
			   (equal blkNum 3)
			   (equal tNum 10)
			   (equal tPhase 'fix)
		  )
		  (setf *task-over* t)
	)
)

;;; function to update the block value
(defun update-blk (task blkNum tNum tPhase)

	;;; special case: every two blocks, a fixation period is presented
	;;; here we want to update the tPhase to 'fix'
	;;; when the block number is a member of the 'fix-blocks' list, and the ITI of the last trial of the block has been presented:
	;;; - set the trial-phase of the task to fix
	(when (and (member blkNum *fix-blocks*)
			   (equal tNum 10)
			   (equal tPhase 'ITI)
		  )
		  (setf (trial-phase task) 'fix)
	)

	;;; when transitioning between blocks, within a session, there are two cases: a fix was presented or it wasn't

	;;; case 1:
	;;; when the ITI of the last trial of a block that isn't a fix-block has been presented:
	;;; - increment the block number
	(when (and (not (member blkNum *fix-blocks*))
			   (equal tNum 10)
			   (equal tPhase 'ITI)
		  )
		  (setf (session-block task) (+ blkNum 1))
	)

	;;; case 2:
	;;; when the fixation period after a fix-block that isn't the last block of a session has been presented:
	;;; - increment the block number
	(when (and (not (equal blkNum 3))
			   (equal tNum 10)
			   (equal tPhase 'fix)
		  )
		  (setf (session-block task) (+ blkNum 1))
	)

	;;; when the fixation period after the last block of the session has been presented:
	;;; - set the block number back to 0
	(when (and (equal blkNum 3)
			   (equal tNum 10)
			   (equal tPhase 'fix)
		  )
		  (setf (session-block task) 0)
	)
)

;;; function to update the trial number and trial phase values
(defun update-tNumPhase (task blkNum tNum tPhase)

	;;; when the cue has been presented:
	;;; - increment the trial number (no ITI for the cue)
	(when (and (equal tNum 0)
			   (equal tPhase 'stimulus)
		  )
		  (setf (bt-index task) (+ tNum 1))
	)

	;;; when a trial's stimulus has been presented:
	;;; set the trial-phase of the task to 'ITI'
	(when (and (> tNum 0)
			   (equal tPhase 'stimulus)
		  )
		  (setf (trial-phase task) 'ITI)
	)

	;;; when an ITI has been presented, but not the last one of a block:
	;;; - set the trial-phase of the task to 'stimulus'
	;;; - increment the trial number
	(when (and (< tNum 10)
			   (equal tPhase 'ITI)
		  )
		  (setf (trial-phase task) 'stimulus)
		  (setf (bt-index task) (+ tNum 1))
	)

	;;; when transitioning between blocks, within a session, there are two cases: a fix was presented or it wasn't

	;;; case 1:
	;;; when the last ITI of a block that isn't a fix-block has been presented:
	;;; - set the trial-phase of the task to 'stimulus'
	;;; - set the bt-index of the task to 0 (indexes the cue of a block of trials)
	(when (and (not (member blkNum *fix-blocks*))
			   (equal tNum 10)
			   (equal tPhase 'ITI)
		  )
		  (setf (trial-phase task) 'stimulus)
		  (setf (bt-index task) 0)
	)

	;;; case 2:
	;;; when the fixation after a fix-block has been presented:
	;;; - set the trial-phase of the task to 'stimulus'
	;;; - set the bt-index of the task to 0 (indexes the cue of a block of trials)
	(when (and (member blkNum *fix-blocks*)
			   (equal tNum 10)
			   (equal tPhase 'fix)
		  )
		  (setf (trial-phase task) 'stimulus)
		  (setf (bt-index task) 0)
	)
)

;;; ------------------------------------------------------------------
;;; N-BACK TASK OBJECT
;;; ------------------------------------------------------------------

(defclass nback-task ()
	((task-session   :accessor task-session ;;;tracks what session we are in
			         :initform nil)
	 (session-block  :accessor session-block ;;;tracks what block we are in
					 :initform nil)
	 (bt-index       :accessor bt-index ;;;indexes what trial in the block we're on
					 :initform nil)
	 (trial-phase    :accessor trial-phase ;;;represents what phase of the current trial that we're on
			         :initform nil))
	(:documentation  "A manager for the N-Back task")
)

(defmethod init ((task nback-task))
	(setf (task-session task) 0)
	(setf (session-block task) 0)
	(setf (bt-index task) 0)
	(setf (trial-phase task) 'stimulus)
)

;;;method to step task to next trial
(defmethod next ((task nback-task))
	(let ((ses (task-session task))
		  (blkNum (session-block task))
		  (tNum (bt-index task))
		  (tPhase (trial-phase task))
          (dispTime nil))
      (when (equal tPhase 'ITI)
        (setf dispTime +itiTime+))
      (when (equal tPhase 'fix)
        (setf dispTime +fixTime+))
      (when (equal tNum 0)
        (setf dispTime +cueTime+))
      (when (and (> tNum 0)
                 (equal tPhase 'stimulus))
        (setf dispTime +stimTime+))
	  (when (and (equal blkNum 3)
				 (equal tNum 10)
				 (equal tPhase 'fix))
		(setf dispTime 86400))

	  ;;; update the model's visicon with the current task information
	  (update-visicon ses blkNum tNum tPhase)
	  
	  ;;; just as a new stimulus is being presented, check to make sure that the number of trials that have occurred (not including the to-be-presented stimulus)
	  ;;; is equal to the number of recorded responses. If not, throw a warning message
	  (when (and (> tNum 0)
			   (equal tPhase 'stimulus)
			)
	  		(when (not (equal *numTrials* *numResponses*))
	  			  (print "Warning: Number of trials and number of responses not equal!")
				  (print *numTrials*)
				  (print *numResponses*)
	  		)
			(incf *numTrials*)
	  )
	  
	  ;;;(display-taskScreen ses blkNum tNum tPhase) ;;; puts the current display on the task window
	  (schedule-event-relative dispTime 'next :params (list task)) ;;; schedules the next 'next' method call to occur at the time the current task display should expire
      (update-ses task ses blkNum tNum tPhase) ;;; updates the session when necessary
      (update-blk task blkNum tNum tPhase) ;;; updates the block when necessary
      (update-tNumPhase task blkNum tNum tPhase) ;;; updates the trial number and phase when necessary
      )
)

(defparameter *task* nil)
(defun runTaskFromPython ()

	(setf *task-over* nil)
	(setf *responses* '())
	(setf *respTimes* '())
	(setf *retrievedChunks* '())
	(setf *imaginalChunks* '())
	(setf *numResponses* 0)
	(setf *numTrials* 0)
	(load "Z:\\gp\\ACTR-WM\\code\\models\\new_nBack\\nBack-model-chunks.lisp")
	;;;(load "/home/pjrice/gp/ACTR-WM/code/models/new_nBack/nBack-model-chunks.lisp")
	(install-device '("motor" "keyboard"))
	(setf *task* (make-instance 'nback-task))
	(init *task*)
	(schedule-event-now 'next :params (list *task*))
	(run-until-condition 'task-over)
)
(add-act-r-command "runTaskFromPython" 'runTaskFromPython)

;;; function to output the combined response info list to python
;;; added as an actr command here and then called with actr.call_command('print-resp')
(defun print-resp ()
	(print (combine-lists *responses* *respTimes* *retrievedChunks*))
)
(add-act-r-command "print-resp" 'print-resp)

(defun print-imaginal-chunks ()
	(print *imaginalChunks*)
)
(add-act-r-command "print-imaginal-chunks" 'print-imaginal-chunks)

(defun call-clear-all ()
	(clear-all)
)
(add-act-r-command "call-clear-all" 'call-clear-all)



