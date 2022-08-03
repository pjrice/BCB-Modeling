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

(defun test-read-imaginal-slots1 (&optional (expected '(a b c)))
  "Tests if the function works; prints 'T' if so"
  (define-model test)
  (chunk-type window one two three)
  (add-dm (a isa chunk)
          (b isa chunk)
          (c isa chunk)
          (im-test isa window one a two b three c))
  (set-buffer-chunk 'imaginal 'im-test)
  (print (equal (read-imaginal-slots)
                expected))
  (delete-model test))

(defun test-read-imaginal-slots2 (&optional (expected '(nil nil nil)))
  "Tests if the function works when no chunk is present"
  (define-model test)
  (print (equal (read-imaginal-slots)
                expected))
  (delete-model test))
